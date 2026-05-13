import pytest
from src.logic.director import DirectorEngine, MapAPI
from src.ui.scenes import GameContext
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World

def test_director_executes_generator():
    """Test that the director can start and advance a generator script."""
    player = Character("Test", Warrior())
    world = World([[0]])
    context = GameContext(player, world)
    api = MapAPI(context)
    director = DirectorEngine(context, api)
    
    def simple_script():
        context.global_state.set_flag("step1", True)
        yield "wait_click"
        context.global_state.set_flag("step2", True)
        
    director.start_script(simple_script())
    
    assert context.global_state.get_flag("step1") is True
    assert context.global_state.get_flag("step2") is False
    assert director.is_busy() is True
    
    director.advance("click")
    
    assert context.global_state.get_flag("step2") is True
    assert director.is_busy() is False

def test_map_api_set_flag():
    """Test that MapAPI correctly interacts with GlobalState."""
    player = Character("Test", Warrior())
    world = World([[0]])
    context = GameContext(player, world)
    api = MapAPI(context)
    
    api.set_flag("quest_abc", 123)
    assert context.global_state.get_flag("quest_abc") == 123

def test_map_api_give_item():
    """Test that MapAPI correctly adds items to player inventory."""
    player = Character("Test", Warrior())
    world = World([[0]])
    context = GameContext(player, world)
    api = MapAPI(context)
    
    api.give_item("Espada de Teste")
    assert "Espada de Teste" in player.inventory.items

def test_director_branching_script():
    """Test that the director can handle branching scripts with choices."""
    player = Character("Test", Warrior())
    world = World([[0]])
    context = GameContext(player, world)
    api = MapAPI(context)
    director = DirectorEngine(context, api)
    
    def branching_script(api):
        yield api.say("Oi!")
        choice = yield ("choice", ["Sim", "Não"])
        if choice == "Sim":
            api.set_flag("said_yes", True)
        else:
            api.set_flag("said_no", True)
            
    director.start_script(branching_script(api))
    
    # After start, it should be at the first yield (say)
    director.advance() # Move past "say"
    
    # Now it should be at the "choice" yield
    director.advance("Sim")
    
    assert context.global_state.get_flag("said_yes") is True
    assert context.global_state.get_flag("said_no") is False
    assert director.is_busy() is False
