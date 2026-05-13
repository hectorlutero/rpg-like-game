import pytest
from unittest.mock import MagicMock
from src.logic.quest_actions import RunScriptAction

def test_run_script_action():
    action = RunScriptAction("my_script")
    
    mock_director = MagicMock()
    context = {"director": mock_director}
    
    action.execute(context)
    
    mock_director.run_script.assert_called_once_with("my_script")

def test_run_script_action_no_director():
    action = RunScriptAction("my_script")
    
    context = {} # Missing director
    
    # Should not raise an exception
    action.execute(context)
