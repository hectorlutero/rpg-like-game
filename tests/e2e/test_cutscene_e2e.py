import pygame
import pytest
from tests.e2e.ui_tester import UITester
from src.logic.director import DirectorEngine, MapAPI
from src.models.dialogue import NPC
from src.models.world import Position

def test_cutscene_npc_walk_and_talk():
    """E2E-style test for a cutscene where an NPC moves and then speaks."""
    # 1. Setup
    tester = UITester()
    # NPC starts at (0,0)
    npc = NPC("Guarda", Position(0, 0))
    tester.world.add_interactable(0, 0, npc)
    
    # Setup Director
    api = MapAPI(tester.context)
    director = DirectorEngine(tester.context, api)
    
    # 2. Define Cutscene Script
    def cutscene():
        # Move NPC to (80, 80)
        yield api.move_to(npc, Position(80, 80), speed=100)
        # Then say something
        yield api.say("Pare aí, viajante!")
        tester.context.global_state.set_flag("cutscene_finished", True)
        
    # 3. Start Script
    director.start_script(cutscene())
    assert director.is_busy() is True
    
    # 4. Advance time (update)
    # Speed is 100, distance is ~113. Needs ~1.13s. 
    # Let's do two ticks of 1.0s
    director.update(1.0) 
    assert npc.position.x < 80 # Not yet there
    
    director.update(1.0)
    # Now it should have reached and advanced to "say"
    assert npc.position.x == 80
    assert npc.position.y == 80
    assert director.current_action[0] == "say"
    assert director.current_action[1] == "Pare aí, viajante!"
    
    # 5. Complete dialogue (Simulate player click/confirm)
    director.advance() # Move past "say"
    
    # 6. Verify final state
    assert tester.context.global_state.get_flag("cutscene_finished") is True
    assert director.is_busy() is False
