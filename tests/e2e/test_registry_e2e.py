import os
import pygame
import pytest
from tests.e2e.ui_tester import UITester
from src.core.registry import EntityRegistry
from src.ui.exploration_scene import ExplorationScene

def test_registry_e2e_chest_interaction():
    """E2E test: Spawn a chest from registry and interact with it in-game."""
    # 1. Setup
    tester = UITester()
    
    # Use the real data/entities.json
    registry = EntityRegistry("data/entities.json")
    
    # 2. Spawn a chest via registry into the world at tile (2, 2)
    # tile (2, 2) pixels: x=64..96, y=64..96
    chest_id = "e2e_chest"
    chest = registry.spawn_to_map("chest_basic", tester.world, 2, 2, gold=999, chest_id=chest_id)
    
    # 3. Start Exploration Scene
    scene = ExplorationScene(tester.manager, None, None)
    tester.manager.push(scene)
    
    # 4. Position player to face the chest
    # Player tile (2, 3) pixels: x=64..96, y=96..128
    # Center of tile (2, 3) is (80, 112)
    tester.player.position.x = 80
    tester.player.position.y = 112
    tester.player.facing_direction = "N" # Facing North towards (2, 2)
    
    # 5. Interact (Press E)
    tester.post_key(pygame.K_e)
    
    # 6. Verify Interaction is active
    # The interaction manager should have detected the chest
    assert scene.interaction_manager.is_active
    
    # 7. Confirm interaction (Press Space/Enter)
    tester.post_key(pygame.K_SPACE)
    
    # 8. Verify the outcome
    # Chest should have given 999 gold to the player
    assert tester.player.gold >= 999
    
    # 9. Verify chest state (it should be open)
    assert chest.is_open
    
    # 10. Interact again - should say it's empty
    tester.post_key(pygame.K_e)
    assert scene.interaction_manager.is_active
    # If we could capture text, we'd check for "O baú está vazio."
