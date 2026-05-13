import pytest
from src.models.persistence import SaveManager
from src.ui.scenes import GameContext
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World
from src.logic.director import DirectorEngine, MapAPI

def test_save_protection_when_director_busy():
    """Test that SaveManager prevents saving while director is busy."""
    player = Character("Test", Warrior())
    world = World([[0]])
    context = GameContext(player, world)
    api = MapAPI(context)
    director = DirectorEngine(context, api)
    context.director = director
    
    save_manager = SaveManager("test_protected.json")
    
    # 1. Start a script
    def busy_script():
        yield "wait"
    director.start_script(busy_script())
    assert director.is_busy() is True
    
    # 2. Try to save
    success = save_manager.save_game(context)
    assert success is False
    
    # 3. Finish script
    director.advance()
    assert director.is_busy() is False
    
    # 4. Try to save again
    success = save_manager.save_game(context)
    assert success is True
    
    import os
    if os.path.exists("test_protected.json"):
        os.remove("test_protected.json")
