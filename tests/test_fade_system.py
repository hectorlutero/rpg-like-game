import pytest
import pygame
from unittest.mock import MagicMock
from src.ui.exploration_scene import ExplorationScene
from src.models.interaction import TransitionRequest
from src.models.world import Position

# Initialize pygame for Surface and Font support
pygame.init()
pygame.display.set_mode((1,1), pygame.HIDDEN)

class MockContext:
    def __init__(self):
        self.world = MagicMock()
        self.player = MagicMock()
        self.player.position = Position(0, 0)
        self.save_manager = MagicMock()
        self.orchestrator = MagicMock()
        self.orchestrator.get_tag_position.return_value = (None, None)

def test_fade_out_logic():
    manager = MagicMock()
    manager.context = MockContext()
    manager.active_scene = None
    
    scene = ExplorationScene(manager, None, None)
    manager.active_scene = scene
    
    # Request transition
    req = TransitionRequest("forest.json", "tag")
    scene.trigger_transition(req)
    
    assert scene.fade_target == 255
    assert scene.pending_transition == req
    
    # Simulate update (dt = 0.5s)
    # fade_speed is 510, so 0.5s should bring alpha to 255
    scene.update(0.5)
    assert scene.fade_alpha == 255

def test_input_blocking_during_fade():
    manager = MagicMock()
    manager.context = MockContext()
    
    scene = ExplorationScene(manager, None, None)
    manager.active_scene = scene
    
    # Start fade
    scene.fade_alpha = 100
    scene.fade_target = 255
    
    # Simulate move keys
    from collections import defaultdict
    pygame.key.get_pressed = MagicMock(return_value=defaultdict(bool, {pygame.K_RIGHT: True}))
    scene.update(0.016)
    
    # Player should NOT have moved
    assert manager.context.player.position.x == 0
    
    # Simulate interaction event
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_e)
    scene.handle_event(event)
    
    # Interaction manager should NOT have been called
    scene.interaction_manager.interact = MagicMock()
    scene.handle_event(event)
    scene.interaction_manager.interact.assert_not_called()

def test_fade_in_logic():
    manager = MagicMock()
    manager.context = MockContext()
    
    scene = ExplorationScene(manager, None, None)
    manager.active_scene = scene
    
    # Start at peak
    scene.fade_alpha = 255
    scene.fade_target = 0 # Request Fade In
    
    from collections import defaultdict
    pygame.key.get_pressed = MagicMock(return_value=defaultdict(bool))
    
    scene.update(0.5)
    assert scene.fade_alpha == 0
