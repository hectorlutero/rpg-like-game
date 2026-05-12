import os
import pygame
import pytest
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World, Position
from src.ui.scenes import GameContext, SceneManager
from src.ui.combat_scene import CombatScene
from src.models.combat import CombatManager

# Configure Pygame to use a dummy video driver for headless testing
os.environ['SDL_VIDEODRIVER'] = 'dummy'

class UITester:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.world = World([[0]*10 for _ in range(10)])
        self.player = Character("Hero", Warrior())
        self.context = GameContext(self.player, self.world)
        self.manager = SceneManager(self.context)

    def post_key(self, key):
        event = pygame.event.Event(pygame.KEYDOWN, {'key': key})
        self.manager.handle_event(event)
        self.manager.update(0.1)
    
    def wait_for_player_turn(self, timeout_steps=1000):
        """Advances time until it's the player's turn or timeout."""
        for _ in range(timeout_steps):
            if self.manager.active_scene.combat_manager.is_waiting_for_input:
                return True
            self.manager.update(0.1)
        return False

def test_combat_ui_flow_automated():
    tester = UITester()
    
    # Setup Enemy
    enemy = Character("Slime", Warrior(), level=1)
    enemy.hp = 20
    
    # Loot table
    loot_table = {"Poção de Vida": 1.0}
    
    cm = CombatManager(tester.context.party, [enemy], gold_reward=50, xp_reward=100, loot_table=loot_table)
    scene = CombatScene(tester.manager, cm, Position(100, 100))
    tester.manager.push(scene)
    
    # 1. Wait for first turn (usually player if faster)
    assert tester.wait_for_player_turn()
    assert cm.active_entity == tester.player
    
    # 2. Select Attack (First option) and confirm
    tester.post_key(pygame.K_SPACE)
    
    # Check if enemy was hit (Warrior has 10 Strength, Slime has 0 defense -> 10 damage)
    assert enemy.hp <= 10
    
    # 3. Wait for Enemy Turn and then back to Player Turn
    # We wait until the player is ready again. The enemy will act automatically during update.
    assert tester.wait_for_player_turn()
    
    # Check if player was hit (Slime hit back)
    assert tester.player.hp < tester.player.max_hp
    
    # 4. Finish him!
    tester.post_key(pygame.K_SPACE)
    
    # Enemy should be dead (20 HP total, 2 hits of 10)
    # CombatScene should pop itself and award loot
    
    # Important: In CombatScene._execute_combat_action, if victory is detected, it pops.
    # We might need one more update to trigger the pop if it's in the next frame, 
    # but currently it pops immediately in the action execution.
    
    assert tester.manager.active_scene != scene
    assert tester.player.gold == 50
    # Level up resets XP to 0 if amount >= 100
    assert tester.player.level == 2
    assert tester.player.xp == 0
    assert "Poção de Vida" in tester.player.inventory.items
    
    pygame.quit()
