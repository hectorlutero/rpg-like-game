import pytest
import os
import json
from src.core.orchestrator import WorldOrchestrator
from src.core.registry import EntityRegistry
from src.models.world import World

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
