import pytest
import json
import os
import pygame
from src.core.assets import MetadataLoader, AssetManager

# Initialize pygame for Surface operations (no display needed for basic slicing)
if not pygame.get_init():
    pygame.init()

def test_metadata_loader_parses_valid_json(tmp_path):
    # Setup
    data = {
        "sprites": {
            "hero_idle": {"x": 0, "y": 0, "w": 32, "h": 32},
            "hero_walk": {"x": 32, "y": 0, "w": 32, "h": 32}
        },
        "animations": {
            "walk": ["hero_walk", "hero_idle"]
        }
    }
    p = tmp_path / "metadata.json"
    p.write_text(json.dumps(data))
    
    # Execute
    loader = MetadataLoader()
    result = loader.load(str(p))
    
    # Verify
    assert result == data
    assert result["sprites"]["hero_idle"]["w"] == 32

def test_metadata_loader_returns_empty_dict_on_missing_file():
    loader = MetadataLoader()
    result = loader.load("non_existent.json")
    assert result == {}

def test_asset_manager_singleton():
    am1 = AssetManager()
    am2 = AssetManager()
    assert am1 is am2

def test_asset_manager_lazy_slices_sprite(tmp_path, monkeypatch):
    # Setup metadata
    metadata = {
        "sprites": {
            "hero_idle": {"x": 0, "y": 0, "w": 16, "h": 16}
        }
    }
    meta_path = tmp_path / "hero.json"
    meta_path.write_text(json.dumps(metadata))
    
    # Setup dummy sheet image
    sheet_surface = pygame.Surface((32, 32))
    sheet_surface.fill((255, 0, 0)) # Red
    
    # Mock pygame.image.load to return our dummy surface
    monkeypatch.setattr(pygame.image, "load", lambda p: sheet_surface)
    
    am = AssetManager()
    # Reset internal state for test purity since it's a singleton
    am._sheets = {}
    am._sprite_cache = {}
    
    am.register_sheet("hero", "dummy_path.png", str(meta_path))
    
    # Execute
    sprite = am.get_sprite("hero", "hero_idle")
    
    # Verify
    assert isinstance(sprite, pygame.Surface)
    assert sprite.get_width() == 16
    assert sprite.get_height() == 16
    
    # Verify caching (requesting again should return same object)
    sprite2 = am.get_sprite("hero", "hero_idle")
    assert sprite is sprite2

def test_asset_manager_returns_placeholder_on_missing_sprite(monkeypatch):
    # Mock load to avoid disk access
    monkeypatch.setattr(pygame.image, "load", lambda p: pygame.Surface((32, 32)))
    
    am = AssetManager()
    am._sheets = {}
    am._sprite_cache = {}
    
    am.register_sheet("test", "test.png", "missing.json")
    
    sprite = am.get_sprite("test", "invalid_id")
    assert isinstance(sprite, pygame.Surface)
    assert sprite.get_width() == 32 # Default placeholder size

def test_asset_manager_get_animation(tmp_path, monkeypatch):
    metadata = {
        "sprites": {
            "f1": {"x": 0, "y": 0, "w": 16, "h": 16},
            "f2": {"x": 16, "y": 0, "w": 16, "h": 16}
        },
        "animations": {
            "walk": ["f1", "f2"]
        }
    }
    meta_path = tmp_path / "anim.json"
    meta_path.write_text(json.dumps(metadata))
    
    monkeypatch.setattr(pygame.image, "load", lambda p: pygame.Surface((32, 16)))
    
    am = AssetManager()
    am._sheets = {}
    am._sprite_cache = {}
    am.register_sheet("anim_test", "path.png", str(meta_path))
    
    frames = am.get_animation("anim_test", "walk")
    assert len(frames) == 2
    assert frames[0].get_width() == 16
    assert frames[1].get_width() == 16

def test_asset_manager_get_animation_duration(tmp_path, monkeypatch):
    metadata = {
        "animations": {
            "walk": ["f1", "f2"],
            "walk_duration": 150
        }
    }
    meta_path = tmp_path / "duration.json"
    meta_path.write_text(json.dumps(metadata))
    
    monkeypatch.setattr(pygame.image, "load", lambda p: pygame.Surface((32, 16)))
    
    am = AssetManager()
    am._sheets = {}
    am.register_sheet("dur_test", "path.png", str(meta_path))
    
    # Specified duration
    assert am.get_animation_duration("dur_test", "walk") == 150
    # Default duration
    assert am.get_animation_duration("dur_test", "non_existent") == 100
