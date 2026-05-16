import pytest
import pygame
import os
import json
from src.ui.scenes import SceneManager, GameContext
from src.ui.title_scene import TitleScene
from src.ui.exploration_scene import ExplorationScene
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World
from src.models.persistence import SaveManager
from src.core.orchestrator import WorldOrchestrator
from src.core.registry import EntityRegistry

@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()

@pytest.fixture
def title_setup():
    # Setup registry and orchestrator
    if not os.path.exists("data/entities.json"):
        os.makedirs("data", exist_ok=True)
        with open("data/entities.json", "w") as f: json.dump({}, f)
    
    registry = EntityRegistry("data/entities.json")
    save_manager = SaveManager("test_save")
    context = GameContext(Character("Test", Warrior()), World([[0]]))
    context.save_manager = save_manager
    context.orchestrator = WorldOrchestrator(registry, None)
    manager = SceneManager(context)
    title_scene = TitleScene(manager)
    manager.push(title_scene)
    return title_scene, manager, context

def test_title_initial_state(title_setup):
    title_scene, _, _ = title_setup
    assert title_scene.state == "MAIN"
    assert title_scene.selector.current_item == "Novo Jogo"

def test_title_navigation(title_setup):
    title_scene, _, context = title_setup
    
    # Mock event for DOWN key
    class MockEvent:
        def __init__(self, key): 
            self.type = pygame.KEYDOWN
            self.key = key
    
    # Simulate DOWN key (action: DOWN)
    # Note: handle_event uses context.inputs.is_action_just_pressed
    # which checks pygame.key.get_pressed() and event.key
    # We can just call selector.next() directly to test logic if mocking inputs is hard
    # but let's try calling handle_event with a real-looking event.
    
    title_scene.handle_event(MockEvent(pygame.K_DOWN))
    # Depending on InputManager mapping, K_DOWN should be DOWN action.
    assert title_scene.selector.index == 1
    assert title_scene.selector.current_item == "Carregar Jogo"

def test_new_game_starts_exploration(title_setup):
    title_scene, manager, context = title_setup
    
    # Ensure map exists
    os.makedirs("data/maps", exist_ok=True)
    with open("data/maps/starting_village.json", "w") as f:
        json.dump({"grid": [[0]], "tileset": "village"}, f)

    title_scene._start_new_game()
    assert isinstance(manager.active_scene, ExplorationScene)
    assert context.play_time == 0.0
    assert context.player.name == "Herói"

def test_load_menu_empty(title_setup):
    title_scene, _, _ = title_setup
    title_scene._refresh_load_menu()
    assert title_scene.load_selector.options == ["Nenhum jogo salvo"]
    assert title_scene.save_slots == [None]

def test_load_menu_with_save(title_setup):
    title_scene, _, context = title_setup
    
    # Create a dummy save
    context.player.level = 5
    context.world.map_name = "test_map"
    context.save_manager.save_game(context, slot=1)
    
    title_scene._refresh_load_menu()
    assert len(title_scene.load_selector.options) >= 1
    assert 1 in title_scene.save_slots
    
    # Cleanup
    if os.path.exists("test_save_1.json"):
        os.remove("test_save_1.json")
    if os.path.exists("test_save.json"):
        os.remove("test_save.json")
