import unittest
from src.models.character import Character
from src.models.classes import Mage, Warrior
from src.models.status import StatusManager
from src.models.items import Equipment

class TestStatusSystem(unittest.TestCase):
    def setUp(self):
        self.attacker = Character("Mage", Mage()) # Base INT ~27
        self.defender = Character("Warrior", Warrior()) # Base INT ~4

    def test_calculate_chance_with_int_difference(self):
        # 50 + (27 - 4) = 73
        chance = StatusManager.calculate_chance(self.attacker, self.defender, 50, 'poison')
        self.assertEqual(chance, 73)

    def test_calculate_chance_with_resistance(self):
        # Create an item with resistance
        ring = Equipment("Anti-Poison Ring", "Protects against poison", "accessory")
        ring.resistances = {'poison': 0.5} # 50% resistance
        
        self.defender.equip_item(ring)
        
        # (50 + (27 - 4)) * (1 - 0.5) = 73 * 0.5 = 36.5 -> 36
        chance = StatusManager.calculate_chance(self.attacker, self.defender, 50, 'poison')
        self.assertEqual(chance, 36)

    def test_apply_status_success(self):
        # Forced success by high chance or lucky roll
        self.attacker.base_stats['inteligencia'] = 1000
        success, msg = StatusManager.apply_status(self.attacker, self.defender, 'poison', 50, 3, 10)
        self.assertTrue(success)
        self.assertIn('poison', self.defender.status_effects)
        self.assertEqual(self.defender.status_effects['poison']['duration'], 3)

    def test_poison_tick_reduces_hp_and_duration(self):
        self.defender.status_effects['poison'] = {'duration': 2, 'potency': 10}
        initial_hp = self.defender.hp
        
        logs = StatusManager.process_tick(self.defender)
        
        self.assertEqual(self.defender.hp, initial_hp - 10)
        self.assertEqual(self.defender.status_effects['poison']['duration'], 1)
        self.assertTrue(any("sofreu 10 de dano" in log for log in logs))

    def test_status_expiration(self):
        self.defender.status_effects['poison'] = {'duration': 1, 'potency': 10}
        
        StatusManager.process_tick(self.defender)
        
        self.assertNotIn('poison', self.defender.status_effects)

    def test_paralysis_detection(self):
        self.assertFalse(StatusManager.is_paralyzed(self.defender))
        self.defender.status_effects['paralysis'] = {'duration': 2}
        self.assertTrue(StatusManager.is_paralyzed(self.defender))

    def test_paralysis_no_longer_freezes_atb(self):
        from src.models.combat import CombatManager
        cm = CombatManager([self.defender], [])
        
        # Apply paralysis
        self.defender.status_effects['paralysis'] = {'duration': 2}
        
        # Tick combat manager
        cm.update(1.0)
        
        # Meter should GROW now (agility * 2.0 * dt)
        agility = self.defender.get_attribute('agilidade')
        self.assertEqual(cm.atb_states[self.defender], agility * 2.0 * 1.0)

    def test_combat_manager_processes_status_on_turn(self):
        from src.models.combat import CombatManager
        cm = CombatManager([self.defender], [])
        
        # Setup poison
        self.defender.status_effects['poison'] = {'duration': 2, 'potency': 5}
        initial_hp = self.defender.hp
        
        # Force ATB to 100
        cm.atb_states[self.defender] = 100.0
        
        # Update should trigger turn and status tick
        cm.update(0)
        
        self.assertEqual(self.defender.hp, initial_hp - 5)
        self.assertTrue(any("sofreu 5 de dano" in log for log in cm.battle_log))

    def test_wait_action_resets_atb(self):
        from src.models.combat import CombatManager
        cm = CombatManager([self.defender], [])
        cm.atb_states[self.defender] = 100.0
        
        cm.execute_action(self.defender, "Wait", self.defender)
        
        self.assertEqual(cm.atb_states[self.defender], 0.0)
        self.assertTrue(any("esperou" in log for log in cm.battle_log))

    def test_paralysis_restricts_actions_in_combat_scene(self):
        # We need a minimal pygame setup for CombatScene
        import pygame
        pygame.init()
        pygame.font.init()
        
        from src.models.combat import CombatManager
        from src.ui.combat_scene import CombatScene
        from src.ui.scenes import SceneManager, GameContext
        from src.models.world import World
        
        world = World([[0]])
        context = GameContext(self.defender, world)
        manager = SceneManager(context)
        cm = CombatManager([self.defender], [self.attacker])
        scene = CombatScene(manager, cm, None)
        
        # Apply paralysis
        self.defender.status_effects['paralysis'] = {'duration': 2}
        cm.active_entity = self.defender
        
        # Mock selection as "Attack"
        scene.selector.set_options(["Attack", "Item", "Wait"])
        scene.selector.index = 0 # Attack
        
        # Confirming selection should fail (logged message, no action)
        scene._confirm_selection()
        self.assertTrue(any("paralisado e só pode usar Itens ou Esperar" in log for log in cm.battle_log))
        
        # Mock selection as "Wait"
        scene.selector.index = 2 # Wait
        scene._confirm_selection()
        self.assertTrue(any("esperou" in log for log in cm.battle_log))
        self.assertEqual(cm.atb_states[self.defender], 0.0)

if __name__ == '__main__':
    unittest.main()
