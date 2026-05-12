import unittest
from src.models.character import Character
from src.models.classes import Rogue
from src.models.status import StatusManager
from src.models.stats import Modifier, ModifierType

class TestStatusAttributeIntegration(unittest.TestCase):
    def test_status_effect_modifies_attribute(self):
        """Applying a status should add an attribute modifier."""
        hero = Character("Rogue", Rogue())
        base_agi = hero.get_attribute('agilidade')
        
        # We need to decide how to link status to modifiers.
        # Let's say we have a mapping or the StatusManager handles it.
        # For this test, we expect applying 'slow' to reduce agility by 20%.
        
        # Manually apply for now to test the interface we want
        hero.add_temporary_modifier('agilidade', Modifier(-0.2, ModifierType.PERCENT, source="slow"))
        
        self.assertEqual(hero.get_attribute('agilidade'), int(base_agi * 0.8))
        
        # Remove by source
        hero.remove_temporary_modifiers_from_source("slow")
        self.assertEqual(hero.get_attribute('agilidade'), base_agi)

    def test_status_manager_integration(self):
        """StatusManager.apply_status should automatically add modifiers if defined."""
        # This will be our RED test for the next step
        hero = Character("Hero", Rogue())
        attacker = Character("Enemy", Rogue())
        attacker.base_stats['inteligencia'] = 100
        
        base_agi = hero.get_attribute('agilidade')
        
        # Applying 'paralysis' should reduce agility by 50% (as a design choice)
        StatusManager.apply_status(attacker, hero, 'paralysis', 100, 3)
        
        self.assertIn('paralysis', hero.status_effects)
        # Expect reduction
        self.assertEqual(hero.get_attribute('agilidade'), int(base_agi * 0.5))
        
        # Tick until expiration
        StatusManager.process_tick(hero) # 3 -> 2
        StatusManager.process_tick(hero) # 2 -> 1
        StatusManager.process_tick(hero) # 1 -> 0 (removed)
        
        self.assertNotIn('paralysis', hero.status_effects)
        self.assertEqual(hero.get_attribute('agilidade'), base_agi)

if __name__ == "__main__":
    unittest.main()
