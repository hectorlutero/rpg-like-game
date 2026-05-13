import pytest
from unittest.mock import MagicMock
from src.logic.quest_actions import RunScriptAction, GiveItemAction, GiveXPAction

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

def test_give_item_action():
    action = GiveItemAction("Espada Lendária")
    mock_game_context = MagicMock()
    mock_bus = MagicMock()
    
    context = {"game_context": mock_game_context, "signal_bus": mock_bus}
    action.execute(context)
    
    mock_game_context.player.receive_item.assert_called_once_with("Espada Lendária", mock_bus)

def test_give_xp_action():
    action = GiveXPAction(100)
    mock_game_context = MagicMock()
    
    context = {"game_context": mock_game_context}
    action.execute(context)
    
    mock_game_context.player.gain_xp.assert_called_once_with(100)

