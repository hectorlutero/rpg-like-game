import pytest
import os
import json
from src.core.orchestrator import WorldOrchestrator
from src.core.registry import EntityRegistry
from src.models.world import World
from src.core.state import GlobalState

@pytest.fixture
def test_map(tmp_path):
    map_file = tmp_path / "test_map.json"
    data = {
        "name": "Test Map",
        "grid": [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ],
        "entities": [
            {
                "id": "chest_basic",
                "x": 1,
                "y": 1,
                "overrides": {"gold": 123}
            }
        ],
        "tags": {
            "spawn": {"x": 1, "y": 1}
        }
    }
    with open(map_file, "w") as f:
        json.dump(data, f)
    return str(map_file)

def test_orchestrator_loads_map_grid(test_map):
    """Test that the orchestrator loads the map grid correctly."""
    registry = EntityRegistry("data/entities.json")
    orchestrator = WorldOrchestrator(registry)
    
    world = orchestrator.load_map(test_map)
    
    assert isinstance(world, World)
    assert world.width == 3
    assert world.height == 3
    assert world.grid[1][1] == 0

def test_orchestrator_populates_entities(test_map):
    """Test that the orchestrator populates the world with entities from the JSON."""
    registry = EntityRegistry("data/entities.json")
    orchestrator = WorldOrchestrator(registry)
    
    world = orchestrator.load_map(test_map)
    
    # Check chest at (1, 1)
    chest = world.get_interactable_at(1, 1)
    assert chest is not None
    assert chest.gold == 123

def test_orchestrator_tags(test_map):
    """Test that tags are loaded correctly."""
    registry = EntityRegistry("data/entities.json")
    orchestrator = WorldOrchestrator(registry)
    orchestrator.load_map(test_map)
    
    tx, ty = orchestrator.get_tag_position("spawn")
    assert tx == 1
    assert ty == 1

def test_orchestrator_applies_deltas(test_map):
    """Test that the orchestrator applies persistent deltas to entities."""
    registry = EntityRegistry("data/entities.json")
    state = GlobalState()
    state.set_entity_delta("chest_123", {"_is_open": True, "gold": 0})
    
    orchestrator = WorldOrchestrator(registry, state)
    
    # Custom map for delta test
    with open("test_delta.json", "w") as f:
        json.dump({
            "grid": [[0]],
            "entities": [{"id": "chest_basic", "x": 0, "y": 0, "overrides": {"chest_id": "chest_123"}}]
        }, f)
        
    world = orchestrator.load_map("test_delta.json")
    chest = world.get_interactable_at(0, 0)
    
    assert chest.is_open is True
    assert chest.gold == 0
    
    if os.path.exists("test_delta.json"):
        os.remove("test_delta.json")
