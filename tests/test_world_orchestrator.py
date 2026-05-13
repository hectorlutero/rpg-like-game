import pytest
import os
import json
from src.core.orchestrator import WorldOrchestrator
from src.core.registry import EntityRegistry
from src.models.world import World
from src.core.state import GlobalState

def test_orchestrator_loads_map_grid():
    """Test that the orchestrator loads the map grid correctly."""
    registry = EntityRegistry("data/entities.json")
    orchestrator = WorldOrchestrator(registry)
    
    world = orchestrator.load_map("data/maps/vila_inicial.json")
    
    assert isinstance(world, World)
    assert world.width == 5
    assert world.height == 5
    assert world.grid[0][0] == 1
    assert world.grid[1][1] == 0

def test_orchestrator_populates_entities():
    """Test that the orchestrator populates the world with entities from the JSON."""
    registry = EntityRegistry("data/entities.json")
    orchestrator = WorldOrchestrator(registry)
    
    world = orchestrator.load_map("data/maps/vila_inicial.json")
    
    # Check chest at (1, 1)
    chest = world.get_interactable_at(1, 1)
    assert chest is not None
    assert chest.gold == 50
    
    # Check NPC at (3, 3)
    npc = world.get_interactable_at(3, 3)
    assert npc is not None
    assert npc.name == "João"

def test_orchestrator_applies_deltas():
    """Test that the orchestrator applies persistent deltas to entities."""
    registry = EntityRegistry("data/entities.json")
    state = GlobalState()
    # Mock a chest that is already open and empty
    # Note: Chest uses _is_open internally, which is open via property.
    state.set_entity_delta("chest_123", {"_is_open": True, "gold": 0})
    
    orchestrator = WorldOrchestrator(registry, state)
    
    test_map_path = "data/maps/test_delta.json"
    with open(test_map_path, "w") as f:
        json.dump({
            "grid": [[0]],
            "entities": [{"id": "chest_basic", "x": 0, "y": 0, "overrides": {"chest_id": "chest_123"}}]
        }, f)
        
    world = orchestrator.load_map(test_map_path)
    chest = world.get_interactable_at(0, 0)
    
    assert chest.chest_id == "chest_123"
    assert chest.is_open is True
    assert chest.gold == 0
    
    if os.path.exists(test_map_path):
        os.remove(test_map_path)
