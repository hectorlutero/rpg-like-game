import os
import json
import pytest
from src.models.persistence import SaveManager
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World
from src.ui.scenes import GameContext
from src.core.state import GlobalState

def test_save_load_with_global_state():
    """Test that SaveManager correctly persists GlobalState."""
    save_file = "test_save_state"
    save_manager = SaveManager(save_file)
    actual_file = save_file + ".json"
    
    player = Character("Test", Warrior())
    world = World([[0]])
    context = GameContext(player, world)
    
    # Set some state
    context.global_state.set_flag("visited_village", True)
    context.global_state.set_entity_delta("chest_456", {"_is_open": True})
    
    # Save
    success = save_manager.save_game(context)
    assert success is True
    assert os.path.exists(actual_file)
    
    # Check JSON content
    with open(actual_file, 'r') as f:
        full_data = json.load(f)
        data = full_data["data"]
        assert "global_state" in data
        assert data["global_state"]["flags"]["visited_village"] is True
        assert data["global_state"]["deltas"]["chest_456"]["_is_open"] is True
    
    # Load
    save_data = save_manager.load_game()
    assert save_data is not None
    
    # Create new context and restore
    new_state = GlobalState.from_dict(save_data["global_state"])
    assert new_state.get_flag("visited_village") is True
    assert new_state.get_entity_delta("chest_456")["_is_open"] is True

    # Cleanup
    if os.path.exists(actual_file):
        os.remove(actual_file)

    if os.path.exists(save_file):
        os.remove(save_file)
