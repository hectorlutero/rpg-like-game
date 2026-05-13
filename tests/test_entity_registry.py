import pytest
import os
import json
import pygame
from src.core.registry import EntityRegistry
from src.models.interaction import Chest
from src.models.dialogue import NPC

def test_registry_loads_json():
    """Test that the registry loads the JSON file and can access definitions."""
    registry = EntityRegistry("data/entities.json")
    
    # Check if we can find a prefab by ID
    chest_prefab = registry.get_prefab("chest_basic")
    assert chest_prefab is not None
    assert chest_prefab["type"] == "Chest"
    assert chest_prefab["data"]["gold"] == 10

def test_registry_returns_none_for_missing_id():
    """Test that the registry returns None for non-existent IDs."""
    registry = EntityRegistry("data/entities.json")
    assert registry.get_prefab("non_existent") is None

def test_registry_spawns_correct_class():
    """Test that spawn returns the correct class instance."""
    registry = EntityRegistry("data/entities.json")
    
    entity = registry.spawn("chest_basic")
    assert isinstance(entity, Chest)
    assert entity.gold == 10
    assert entity.items == ["potion"]
    
    # NPC might need position in current implementation
    entity_npc = registry.spawn("npc_villager", position=pygame.Vector2(0,0))
    assert isinstance(entity_npc, NPC)
    assert entity_npc.name == "João"
    assert entity_npc.dialogue_data == ["Olá, viajante!"]

def test_registry_spawn_overrides():
    """Test that spawn correctly overrides prefab data."""
    registry = EntityRegistry("data/entities.json")
    
    # Override gold in chest
    entity = registry.spawn("chest_basic", gold=500, chest_id="unique_1")
    assert entity.gold == 500
    assert entity.chest_id == "unique_1"
    assert entity.items == ["potion"] # Should keep original items

def test_registry_spawn_to_map():
    """Test that spawn_to_map correctly places an entity in the world."""
    from src.models.world import World
    registry = EntityRegistry("data/entities.json")
    world = World([[0, 0], [0, 0]])
    
    chest = registry.spawn_to_map("chest_basic", world, 1, 1, gold=100)
    assert world.get_interactable_at(1, 1) == chest
    assert chest.gold == 100
