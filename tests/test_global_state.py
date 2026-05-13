import pytest
from src.core.state import GlobalState

def test_global_state_flags():
    """Test setting and getting global flags."""
    state = GlobalState()
    state.set_flag("tutorial_done", True)
    assert state.get_flag("tutorial_done") is True
    assert state.get_flag("non_existent") is False

def test_global_state_entity_deltas():
    """Test setting and getting entity-specific deltas."""
    state = GlobalState()
    state.set_entity_delta("chest_1", {"is_open": True, "gold": 0})
    
    delta = state.get_entity_delta("chest_1")
    assert delta["is_open"] is True
    assert delta["gold"] == 0
    
    # Partial update
    state.set_entity_delta("chest_1", {"items": ["sword"]})
    delta = state.get_entity_delta("chest_1")
    assert delta["is_open"] is True # Should persist
    assert delta["items"] == ["sword"]

def test_global_state_serialization():
    """Test that global state can be converted to/from a dictionary."""
    state = GlobalState()
    state.set_flag("a", 1)
    state.set_entity_delta("e1", {"x": 10})
    
    data = state.to_dict()
    assert data["flags"]["a"] == 1
    assert data["deltas"]["e1"]["x"] == 10
    
    new_state = GlobalState.from_dict(data)
    assert new_state.get_flag("a") == 1
    assert new_state.get_entity_delta("e1")["x"] == 10
