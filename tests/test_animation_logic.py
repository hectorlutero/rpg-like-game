import pytest
from src.models.character import Character
from src.models.world import Position

class MockClass:
    def __init__(self):
        self.initial_stats = {"vida": 100, "mana": 50}
        self.multipliers = {}
        self.gain_rates = {}
        self.proficiencies = {}

def test_character_animation_timer_increments():
    char = Character("Hero", MockClass())
    assert char.animation_timer == 0
    
    char.update(16) # 16ms update
    assert char.animation_timer == 16
    
    char.update(34)
    assert char.animation_timer == 50

def test_character_animation_frame_cycling(monkeypatch):
    char = Character("Hero", MockClass())
    char.sprite_sheet_id = "hero"
    char.state = "walk"
    
    # Mock AssetManager
    class MockAM:
        def get_animation(self, sid, aid):
            return [1, 2, 3] # 3 frames
        def get_animation_duration(self, sid, aid):
            return 100 # 100ms per frame
            
    monkeypatch.setattr("src.core.assets.AssetManager", lambda: MockAM())
    
    # Start: Frame 0
    assert char.frame_index == 0
    
    # Update 50ms (not enough for next frame)
    char.update(50)
    assert char.frame_index == 0
    
    # Update another 60ms (Total 110ms > 100ms) -> Frame 1
    char.update(60)
    assert char.frame_index == 1
    assert char.animation_timer == 10 # Remainder
    
    # Jump to Frame 2
    char.update(100)
    assert char.frame_index == 2
    
    # Loop back to Frame 0
    char.update(100)
    assert char.frame_index == 0

def test_character_draw_uses_animation_frame(monkeypatch):
    char = Character("Hero", MockClass())
    char.sprite_sheet_id = "hero"
    char.state = "walk"
    char.facing_direction = "S"
    char.frame_index = 1
    
    import pygame
    from unittest.mock import MagicMock
    
    mock_frame = MagicMock(spec=pygame.Surface)
    mock_frame.get_rect.return_value = pygame.Rect(0, 0, 32, 32)
    mock_screen = MagicMock()
    
    # Mock AssetManager
    class MockAM:
        _placeholder = MagicMock()
        def get_animation(self, sid, aid):
            assert aid == "walk_S"
            return [None, mock_frame, None]
            
    monkeypatch.setattr("src.core.assets.AssetManager", lambda: MockAM())
    
    char.draw(mock_screen, (50, 50))
    
    # Verify blit was called with our frame
    mock_screen.blit.assert_called_once()
    args, _ = mock_screen.blit.call_args
    assert args[0] == mock_frame

def test_character_automatic_state_selection(monkeypatch):
    char = Character("Hero", MockClass())
    char.sprite_sheet_id = "hero"
    
    # Mock AssetManager to avoid errors during update
    class MockAM:
        def get_animation_duration(self, sid, aid): return 100
        def get_animation(self, sid, aid): return [1]
    monkeypatch.setattr("src.core.assets.AssetManager", lambda: MockAM())
    
    # Initial state
    assert char.state == "idle"
    
    # Move position
    char.position = Position(10, 10)
    char.update(16)
    assert char.state == "walk"
    
    # Stay still
    char.update(16)
    assert char.state == "idle"

def test_character_animation_state_defaults_to_idle():
    char = Character("Hero", MockClass())
    assert char.state == "idle"
    assert char.frame_index == 0
