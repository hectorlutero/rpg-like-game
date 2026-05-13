import pytest
from src.logic.quest_objectives import EventObjective

def test_event_objective_is_fulfilled():
    obj = EventObjective("KILL", "Slime")
    
    assert obj.is_fulfilled({"type": "KILL", "target": "Slime"}, None) is True
    assert obj.is_fulfilled({"type": "KILL", "target": "Goblin"}, None) is False
    assert obj.is_fulfilled({"type": "INTERACT", "target": "Slime"}, None) is False
    assert obj.is_fulfilled({}, None) is False
