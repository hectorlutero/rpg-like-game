import pytest
import json
import os
from unittest.mock import MagicMock
from src.logic.quest_manager import QuestManager
from src.core.state import GlobalState

@pytest.fixture
def sample_quests_file(tmp_path):
    quests = {
        "q1": {
            "name": "Test Quest",
            "stages": [
                {
                    "id": 0,
                    "description": "Step 1",
                    "objectives": [{"type": "ITEM", "target": "Apple"}]
                },
                {
                    "id": 1,
                    "description": "Step 2",
                    "objectives": [{"type": "KILL", "target": "Slime"}]
                }
            ]
        }
    }
    path = tmp_path / "quests.json"
    with open(path, "w") as f:
        json.dump(quests, f)
    return str(path)

def test_quest_loading(sample_quests_file):
    manager = QuestManager(None, None)
    manager.load_quests(sample_quests_file)
    assert "q1" in manager.quests
    assert manager.quests["q1"]["name"] == "Test Quest"

def test_accept_quest():
    state = GlobalState()
    manager = QuestManager(state, None)
    manager.quests = {"q1": {"stages": [{"id": 0}]}}
    
    manager.accept_quest("q1")
    assert state.quests["q1"]["stage"] == 0
    assert state.quests["q1"]["status"] == "IN_PROGRESS"

def test_quest_progression():
    state = GlobalState()
    bus = MagicMock()
    manager = QuestManager(state, bus)
    manager.quests = {
        "q1": {
            "stages": [
                {"id": 0, "objectives": [{"type": "ITEM", "target": "Apple"}]},
                {"id": 1, "objectives": [{"type": "KILL", "target": "Slime"}]}
            ]
        }
    }
    
    manager.accept_quest("q1")
    
    # Simulate picking up an apple
    manager.on_event({"type": "ITEM", "target": "Apple"})
    
    assert state.quests["q1"]["stage"] == 1
    
    # Simulate killing a slime
    manager.on_event({"type": "KILL", "target": "Slime"})
    assert state.quests["q1"]["status"] == "COMPLETED"

def test_countable_quest_progression():
    state = GlobalState()
    bus = MagicMock()
    manager = QuestManager(state, bus)
    manager.quests = {
        "q1": {
            "stages": [
                {"id": 0, "objectives": [{"type": "KILL", "target": "Slime", "count": 3}]}
            ]
        }
    }
    
    manager.accept_quest("q1")
    
    manager.on_event({"type": "KILL", "target": "Slime"})
    assert state.quests["q1"]["status"] == "IN_PROGRESS"
    
    manager.on_event({"type": "KILL", "target": "Slime"})
    assert state.quests["q1"]["status"] == "IN_PROGRESS"
    
    manager.on_event({"type": "KILL", "target": "Slime"})
    assert state.quests["q1"]["status"] == "COMPLETED"


def test_reward_script_trigger():
    state = GlobalState()
    bus = MagicMock()
    director = MagicMock()
    manager = QuestManager(state, bus)
    manager.director = director
    manager.quests = {
        "q1": {
            "stages": [
                {"id": 0, "objectives": [{"type": "ITEM", "target": "Apple"}], "reward_script": "done"}
            ]
        }
    }
    
    manager.accept_quest("q1")
    manager.on_event({"type": "ITEM", "target": "Apple"})
    
    director.run_script.assert_called_with("done")

def test_quest_querying():
    state = GlobalState()
    manager = QuestManager(state, None)
    state.quests["q1"] = {"stage": 2, "status": "IN_PROGRESS"}
    state.quests["q2"] = {"stage": 0, "status": "COMPLETED"}
    
    assert manager.get_quest_stage("q1") == 2
    assert manager.get_quest_stage("q2") == 0
    assert manager.get_quest_stage("nonexistent") == -1
    
    assert manager.is_completed("q2") is True
    assert manager.is_completed("q1") is False
    assert manager.is_completed("nonexistent") is False
