import pytest
from src.logic.quest_objectives import EventObjective, CountableObjective

def test_event_objective_is_fulfilled():
    obj = EventObjective("KILL", "Slime")
    
    assert obj.is_fulfilled({"type": "KILL", "target": "Slime"}, None) is True
    assert obj.is_fulfilled({"type": "KILL", "target": "Goblin"}, None) is False
    assert obj.is_fulfilled({"type": "INTERACT", "target": "Slime"}, None) is False
    assert obj.is_fulfilled({}, None) is False

def test_countable_objective():
    obj = CountableObjective("KILL", "Slime", 3, "slimes_killed")
    state = {}
    
    # First kill
    assert obj.is_fulfilled({"type": "KILL", "target": "Slime"}, state) is False
    assert state["progress"]["slimes_killed"] == 1
    
    # Second kill
    assert obj.is_fulfilled({"type": "KILL", "target": "Slime"}, state) is False
    assert state["progress"]["slimes_killed"] == 2
    
    # Unrelated event
    assert obj.is_fulfilled({"type": "KILL", "target": "Goblin"}, state) is False
    assert state["progress"]["slimes_killed"] == 2
    
    # Third kill
    assert obj.is_fulfilled({"type": "KILL", "target": "Slime"}, state) is True
    assert state["progress"]["slimes_killed"] == 3
