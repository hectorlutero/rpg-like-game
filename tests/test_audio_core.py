import pytest
import pygame
from src.core.audio import SoundManager

@pytest.fixture(autouse=True)
def setup_pygame():
    pygame.init()
    # No need to init mixer here as SoundManager should handle it
    yield
    pygame.quit()

def test_sound_manager_initialization():
    """B1: SoundManager should initialize without crashing even if mixer fails."""
    manager = SoundManager()
    assert manager is not None
    # If mixer is not available, it should be in silent mode
    if not pygame.mixer.get_init():
        assert manager.enabled is False
    else:
        assert manager.enabled is True

def test_play_music_updates_state():
    """B2: play_music should update the current track ID."""
    manager = SoundManager()
    # Mocking track mapping for testing
    manager.tracks = {"test_bgm": "dummy.wav"}
    
    # We don't need real files for the state check if we mock the pygame call
    # or handle the file-not-found gracefully.
    manager.play_music("test_bgm")
    assert manager.current_track == "test_bgm"

def test_volume_clamping():
    """B3: Volume settings should stay within [0.0, 1.0]."""
    manager = SoundManager()
    manager.set_volume("master", 1.5)
    assert manager.get_volume("master") == 1.0
    manager.set_volume("master", -0.5)
    assert manager.get_volume("master") == 0.0
