import pytest
import json
from src.logic.director import DirectorEngine, MapAPI
from src.logic.cutscene_parser import CutsceneParser
from src.ui.scenes import GameContext, SceneManager
from src.ui.exploration_scene import ExplorationScene
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World, Position

class MockManager:
    def __init__(self, context):
        self.context = context
        self.active_scene = None
    def push(self, scene):
        self.active_scene = scene

def test_cutscene_parser_dialogue_and_wait():
    player = Character("Hero", Warrior())
    world = World([[0]])
    context = GameContext(player, world)
    api = MapAPI(context)
    parser = CutsceneParser(api)
    
    script_data = [
        {"type": "dialogue", "text": "Step 1"},
        {"type": "wait", "duration": 0.5},
        {"type": "flag", "name": "finished", "value": True}
    ]
    
    director = DirectorEngine(context, api)
    context.director = director
    
    gen = parser.create_generator(script_data)
    director.start_script(gen)
    
    # Step 1: Dialogue
    assert director.is_busy()
    assert director.current_action[0] == "say"
    assert director.current_action[1] == "Step 1"
    
    # Simulate dialogue finish
    director.advance()
    
    # Step 2: Wait
    assert director.is_busy()
    assert director.current_action[0] == "wait"
    assert director.current_action[1] == 0.5
    
    director.update(0.3)
    assert director.current_action[1] == pytest.approx(0.2)
    assert director.is_busy()
    
    director.update(0.3)
    
    # Step 3: Flag (instant) should have finished the script
    assert context.global_state.get_flag("finished") is True
    assert not director.is_busy()

def test_exploration_scene_input_lock():
    import pygame
    pygame.init()
    pygame.display.set_mode((1, 1))
    
    player = Character("Hero", Warrior())
    world = World([[0]*10]*10)
    context = GameContext(player, world)
    context.inputs = type('obj', (object,), {'is_action_pressed': lambda *a: True, 'InputAction': type('obj', (object,), {'LEFT':1, 'RIGHT':2, 'UP':3, 'DOWN':4})})
    
    api = MapAPI(context)
    director = DirectorEngine(context, api)
    context.director = director
    
    manager = MockManager(context)
    scene = ExplorationScene(manager)
    manager.active_scene = scene
    
    # Move player to a safe position where they won't hit walls (0,0 is edge)
    player.position.x = 100
    player.position.y = 100
    
    # Start a script
    def dummy_script():
        yield ("wait", 10.0)
    director.start_script(dummy_script())
    
    initial_pos = (player.position.x, player.position.y)
    
    # Try to update scene - should not move player because director is busy
    scene.update(0.1)
    
    assert player.position.x == initial_pos[0]
    assert player.position.y == initial_pos[1]
    
    # Finish script
    director.advance()
    assert not director.is_busy()
    
    # Now it should move (if we had a real input system hooked up, but here we mocked it to return True)
    # Wait, the update loop in ExplorationScene checks inputs.is_action_pressed
    scene.update(0.1)
    assert player.position.x != initial_pos[0] or player.position.y != initial_pos[1]
