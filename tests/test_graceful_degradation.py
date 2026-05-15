import pytest
import pygame
from src.core.assets import AssetManager

def test_engine_headless_initialization():
    """Verifies that the engine can initialize AssetManager and get assets without a real display."""
    # Ensure pygame is initialized but we don't need a window
    if not pygame.get_init():
        pygame.init()
    
    # Force no-display mode for this test if possible, or just rely on existing dummy if used
    # But AssetManager should work as long as pygame.init() happened.
    
    am = AssetManager()
    sprite = am.get_sprite("non_existent", "missing")
    
    assert isinstance(sprite, pygame.Surface)
    # Magenta placeholder is 32x32 by default in our implementation
    assert sprite.get_width() == 32
    assert sprite.get_height() == 32

def test_asset_manager_handles_missing_image_file(monkeypatch):
    """Verifies AssetManager doesn't crash if image file is missing on disk."""
    am = AssetManager()
    am._sheets = {}
    am._sprite_cache = {}
    
    # Register a sheet with a non-existent path
    am.register_sheet("missing_file", "invalid_path.png", "invalid_meta.json")
    
    # This should return placeholder instead of raising FileNotFoundError
    sprite = am.get_sprite("missing_file", "any")
    assert isinstance(sprite, pygame.Surface)
    # Checkerboard pattern: 0,0 is black, 16,0 is magenta
    assert sprite.get_at((16, 0)) == (255, 0, 255, 255) # Magenta
