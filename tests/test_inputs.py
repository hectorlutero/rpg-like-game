import pytest
import pygame
from src.core.inputs import InputManager, InputAction

def test_input_manager_presets():
    im = InputManager()
    
    # Test Standard preset
    assert im.current_preset == "Standard"
    assert pygame.K_UP in im.mapping[InputAction.UP]
    assert pygame.K_w not in im.mapping[InputAction.UP]
    
    # Test WASD preset
    im.set_preset("WASD")
    assert im.current_preset == "WASD"
    assert pygame.K_w in im.mapping[InputAction.UP]
    assert pygame.K_UP not in im.mapping[InputAction.UP]

def test_is_action_pressed():
    im = InputManager()
    
    # Use a dict to avoid IndexError with large Pygame key constants
    from collections import defaultdict
    mock_keys = defaultdict(bool)
    mock_keys[pygame.K_UP] = True
    
    assert im.is_action_pressed(InputAction.UP, keys=mock_keys) == True
    assert im.is_action_pressed(InputAction.DOWN, keys=mock_keys) == False
    
    im.set_preset("WASD")
    assert im.is_action_pressed(InputAction.UP, keys=mock_keys) == False
    
    mock_keys[pygame.K_w] = True
    assert im.is_action_pressed(InputAction.UP, keys=mock_keys) == True

def test_is_action_just_pressed():
    im = InputManager()
    
    # Mocking event
    class MockEvent:
        def __init__(self, key):
            self.type = pygame.KEYDOWN
            self.key = key
            
    event_up = MockEvent(pygame.K_UP)
    event_w = MockEvent(pygame.K_w)
    
    assert im.is_action_just_pressed(InputAction.UP, event_up) == True
    assert im.is_action_just_pressed(InputAction.UP, event_w) == False
    
    im.set_preset("WASD")
    assert im.is_action_just_pressed(InputAction.UP, event_up) == False
    assert im.is_action_just_pressed(InputAction.UP, event_w) == True
