import pytest
from src.logic.ai_controller import AIController, RandomWanderBehavior, StaticBehavior
from src.models.world import World
from src.models.dialogue import NPC
from src.models.world import Position

def test_static_behavior_does_nothing():
    world = World([[0, 0], [0, 0]])
    npc = NPC("Guard", Position(0, 0))
    world.add_interactable(0, 0, npc)
    
    controller = AIController(behavior=StaticBehavior())
    
    # Act
    controller.update(npc, world, 1.0)
    
    # Assert
    assert npc.position.x == 0
    assert npc.position.y == 0
    assert world.get_interactable_at(0, 0) is npc

def test_random_wander_behavior_moves_entity():
    world = World([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    # Grid (1, 1) corresponds to pixel (1*32 + 16, 1*32 + 16)
    npc = NPC("Villager", Position(1 * 32 + 16, 1 * 32 + 16)) 
    world.add_interactable(1, 1, npc)
    
    # Use a mock random behavior or inject a fixed random sequence for determinism?
    # Let's subclass or inject a random choice to ensure it moves right.
    class DeterministicWander(RandomWanderBehavior):
        def __init__(self):
            super().__init__(move_interval=0.5)
            self._next_direction = (1, 0) # Right
            
        def _get_random_direction(self):
            return self._next_direction

    controller = AIController(behavior=DeterministicWander())
    
    # Act - Not enough time passed
    controller.update(npc, world, 0.1)
    assert npc.position.x == 1 * 32 + 16
    assert world.get_interactable_at(1, 1) is npc
    
    # Act - Enough time passed
    controller.update(npc, world, 0.5)
    
    # Assert
    # NPC should have moved right to grid (2, 1) which is pixel (2*32 + 16, 1*32 + 16)
    assert npc.position.x == 2 * 32 + 16
    assert npc.position.y == 1 * 32 + 16
    assert world.get_interactable_at(1, 1) is None
    assert world.get_interactable_at(2, 1) is npc

def test_world_orchestrator_updates_all_ai():
    from src.core.orchestrator import WorldOrchestrator
    
    world = World([[0, 0, 0]])
    npc1 = NPC("N1", Position(0*32+16, 0*32+16))
    npc2 = NPC("N2", Position(2*32+16, 0*32+16))
    
    world.add_interactable(0, 0, npc1)
    world.add_interactable(2, 0, npc2)
    
    class MockAI:
        def __init__(self):
            self.updated = False
        def update(self, e, w, dt, context=None):
            self.updated = True
            
    npc1.ai = MockAI()
    npc2.ai = MockAI()
    
    orchestrator = WorldOrchestrator(None)
    
    # Act
    orchestrator.update_ai(world, 0.1)
    
    # Assert
    assert npc1.ai.updated is True
    assert npc2.ai.updated is True
