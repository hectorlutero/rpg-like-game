import pytest
import json
import os
import pygame
from src.core.orchestrator import WorldOrchestrator
from src.core.assets import AssetManager
from src.core.registry import EntityRegistry

def test_world_orchestrator_registers_assets(tmp_path, monkeypatch):
    # Setup dummy assets
    map_data = {
        "tileset": {
            "id": "forest",
            "image": "forest.png",
            "metadata": "forest.json"
        },
        "grid": [[0, 1], [0, 0]],
        "entities": []
    }
    map_path = tmp_path / "map.json"
    map_path.write_text(json.dumps(map_data))
    
    # Mock AssetManager and pygame.image.load
    monkeypatch.setattr(pygame.image, "load", lambda p: pygame.Surface((32, 32)))
    am = AssetManager()
    am._sheets = {}
    
    registry = EntityRegistry("dummy.json")
    orchestrator = WorldOrchestrator(registry)
    
    # Execute
    world = orchestrator.load_map(str(map_path))
    
    # Verify
    assert "forest" in am._sheets
    assert am._sheets["forest"]["image_path"] == "forest.png"
    assert world.tileset_id == "forest"
