import pytest
from src.core.registry import EntityRegistry
from src.models.interaction import Portal, TransitionRequest

def test_portal_registration():
    # Setup registry (using the actual entities.json)
    registry = EntityRegistry("data/entities.json")
    
    # Check if 'portal' is in prefabs
    assert "portal" in registry.prefabs
    
    # Spawn a portal
    portal = registry.spawn("portal")
    
    assert isinstance(portal, Portal)
    assert portal.target_map == "forest.json"
    assert portal.target_tag == "entrance"
    assert portal.require_interaction is False

def test_portal_overrides():
    registry = EntityRegistry("data/entities.json")
    
    # Spawn with overrides
    overrides = {
        "target_map": "dungeon.json",
        "target_tag": "boss_room",
        "require_interaction": True
    }
    portal = registry.spawn("portal", **overrides)
    
    assert portal.target_map == "dungeon.json"
    assert portal.target_tag == "boss_room"
    assert portal.require_interaction is True
    
    request = portal.on_interact(None)
    assert isinstance(request, TransitionRequest)
    assert request.target_map == "dungeon.json"
