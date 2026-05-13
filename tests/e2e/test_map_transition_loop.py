import pytest
import pygame
import os
import json
import logging

# Configure logging for E2E visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Setup Pygame for tests - Absolute requirement BEFORE scene imports
pygame.init()
if not pygame.font.get_init():
    pygame.font.init()
pygame.display.set_mode((1,1), pygame.HIDDEN)

# Deferred imports to ensure pygame is ready
def test_village_to_forest_transition_e2e():
    from src.core.registry import EntityRegistry
    from src.core.state import GlobalState
    from src.core.orchestrator import WorldOrchestrator
    from src.models.character import Character
    from src.models.classes import Warrior
    from src.ui.scenes import GameContext, SceneManager
    from src.ui.exploration_scene import ExplorationScene
    from src.models.persistence import SaveManager

    logger.info("Starting E2E Test: Village -> Forest")
    
    # 1. Setup real dependencies
    registry = EntityRegistry("data/entities.json")
    global_state = GlobalState()
    orchestrator = WorldOrchestrator(registry, global_state)
    
    player = Character("Hero", Warrior())
    world = orchestrator.load_map("data/maps/starting_village.json")
    
    context = GameContext(player, world)
    context.orchestrator = orchestrator
    context.save_manager = SaveManager("savegame_test.json")
    context.global_state = global_state
    
    manager = SceneManager(context)
    scene = ExplorationScene(manager, None, None)
    manager.push(scene)
    
    logger.info("Initial map loaded.")

    # 2. Position player near portal in starting_village.json (portal is at 24, 10)
    player.position.x = 24 * 32 + 16
    player.position.y = 10 * 32 + 16
    
    # 3. Trigger transition (On Step)
    scene._check_on_step_triggers()
    scene.update(0.016) # Process the request
    
    logger.info("Step-on trigger activated. Fade Out started.")
    assert scene.fade_target == 255
    assert scene.pending_transition is not None
    assert scene.pending_transition.target_map == "forest.json"
    
    # 4. Advance time to Fade Peak
    scene.update(0.6) # Wait 600ms
    logger.info("Fade reached peak. Map swap executing...")
    
    assert scene.fade_alpha == 255
    assert context.world.grid[10][0] == 0 
    
    # Check player positioning
    expected_px = 1 * 32 + 16
    expected_py = 10 * 32 + 16
    assert context.player.position.x == expected_px
    assert context.player.position.y == expected_py
    
    # 5. Verify Auto-save
    assert os.path.exists("savegame_test.json")
    with open("savegame_test.json", "r") as f:
        save_data = json.load(f)
        assert save_data["position"]["x"] == expected_px
        
    # 6. Complete Fade In
    scene.update(0.6)
    assert scene.fade_alpha == 0
    
    # Cleanup
    if os.path.exists("savegame_test.json"):
        os.remove("savegame_test.json")

def test_forest_to_village_return_e2e():
    from src.core.registry import EntityRegistry
    from src.core.state import GlobalState
    from src.core.orchestrator import WorldOrchestrator
    from src.models.character import Character
    from src.models.classes import Warrior
    from src.ui.scenes import GameContext, SceneManager
    from src.ui.exploration_scene import ExplorationScene
    from src.models.persistence import SaveManager

    logger.info("Starting E2E Test: Forest -> Village (Return)")
    
    # Setup
    registry = EntityRegistry("data/entities.json")
    global_state = GlobalState()
    orchestrator = WorldOrchestrator(registry, global_state)
    player = Character("Hero", Warrior())
    world = orchestrator.load_map("data/maps/forest.json")
    context = GameContext(player, world)
    context.orchestrator = orchestrator
    context.save_manager = SaveManager("savegame_test.json")
    manager = SceneManager(context)
    scene = ExplorationScene(manager, None, None)
    manager.push(scene)
    
    # Portal in forest is at (0, 10)
    player.position.x = 0 * 32 + 16
    player.position.y = 10 * 32 + 16
    
    scene._check_on_step_triggers()
    scene.update(0.016)
    assert scene.fade_target == 255
    
    scene.update(0.6)
    # Check return to village
    assert context.world.grid[10][0] == 1 
    assert context.player.position.x == 23 * 32 + 16
    assert context.player.position.y == 10 * 32 + 16
    
    # Cleanup
    if os.path.exists("savegame_test.json"):
        os.remove("savegame_test.json")
