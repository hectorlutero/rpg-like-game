import pytest
import pygame
from src.ui.scenes import SceneManager, GameContext
from src.ui.credits_scene import CreditsScene
from src.ui.game_over_scene import GameOverScene
from src.ui.title_scene import TitleScene
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World
from src.ui.combat_scene import CombatScene

@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()

@pytest.fixture
def scene_setup():
    context = GameContext(Character("Test", Warrior()), World([[0]]))
    manager = SceneManager(context)
    return manager, context

def test_credits_scene_scrolling(scene_setup):
    manager, _ = scene_setup
    scene = CreditsScene(manager)
    initial_y = scene.scroll_y
    
    # Update for 1 second
    scene.update(1.0)
    assert scene.scroll_y == initial_y - scene.scroll_speed
    assert not scene.exiting

def test_credits_scene_exit_on_input(scene_setup):
    manager, context = scene_setup
    scene = CreditsScene(manager)
    
    class MockEvent:
        def __init__(self, key): 
            self.type = pygame.KEYDOWN
            self.key = key
            
    # Simulate CONFIRM
    scene.handle_event(MockEvent(pygame.K_SPACE))
    assert scene.exiting
    assert scene.fade_target == 255
    
    # Update until transition
    scene.fade_alpha = 255
    scene.update(0.1)
    assert isinstance(manager.active_scene, TitleScene)

def test_game_over_scene_initial_state(scene_setup):
    manager, _ = scene_setup
    scene = GameOverScene(manager)
    assert scene.selector.current_item == "Tentar Novamente"
    assert scene.juice.trauma > 0 # Initial shake

def test_game_over_to_title(scene_setup):
    manager, _ = scene_setup
    scene = GameOverScene(manager)
    
    # Select "Menu Principal"
    scene.selector.index = 1
    assert scene.selector.current_item == "Menu Principal"
    
    scene._confirm_selection()
    assert scene.pending_action == "TITLE"
    assert scene.fade_target == 255
    
    # Update until transition
    scene.fade_alpha = 255
    scene.update(0.1)
    assert isinstance(manager.active_scene, TitleScene)

def test_combat_defeat_triggers_game_over(scene_setup):
    manager, context = scene_setup
    
    # Mock CombatManager
    class MockCombatManager:
        def __init__(self):
            self.is_over = True
            self.winner = "Enemies"
            self.active_entity = None
            self.is_waiting_for_input = False
            self.battle_log = []
            self.party = []
            self.enemies = []
    
    # We need a dummy pos
    from src.models.world import Position
    enemy_pos = Position(10, 10)
    
    combat_scene = CombatScene(manager, MockCombatManager(), enemy_pos)
    manager.push(combat_scene)
    
    combat_scene._handle_battle_end()
    assert isinstance(manager.active_scene, GameOverScene)

def test_roll_credits_action(scene_setup):
    manager, context = scene_setup
    from src.logic.quest_actions import RollCreditsAction
    
    action = RollCreditsAction()
    action.execute({"scene_manager": manager})
    
    assert isinstance(manager.active_scene, CreditsScene)
