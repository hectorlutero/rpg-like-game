import pytest
import time
from unittest.mock import MagicMock
from src.models.world import World, Position
from src.models.dialogue import NPC
from src.logic.ai_controller import AIController, RandomWanderBehavior, StaticBehavior
from src.core.orchestrator import WorldOrchestrator

def test_ai_density_stress_no_overlaps():
    """10 NPCs in a 4x4 grid. After many ticks, no two NPCs should occupy the same tile."""
    grid = [[0]*4 for _ in range(4)]
    world = World(grid)
    orchestrator = WorldOrchestrator(None)
    
    npcs = []
    # Fill almost the whole grid
    for i in range(10):
        tx, ty = i % 4, i // 4
        npc = NPC(f"NPC_{i}", Position(tx*32+16, ty*32+16))
        # Rapid movement for stress
        npc.ai = AIController(RandomWanderBehavior(move_interval=0.01))
        world.add_interactable(tx, ty, npc)
        npcs.append(npc)
        
    # Simulate 100 ticks of AI reasoning
    for _ in range(100):
        orchestrator.update_ai(world, 0.1)
        
        # Invariant: Dictionary size must remain 10
        assert len(world.interactables) == 10
        
        # Invariant: Each position in dict must match entity's internal pixel position
        for (tx, ty), entity in world.interactables.items():
            expected_x = tx * 32 + 16
            expected_y = ty * 32 + 16
            assert entity.position.x == expected_x
            assert entity.position.y == expected_y

def test_ai_paused_during_dialogue():
    """If an NPC is being interacted with, its AI should not move it."""
    from src.ui.scenes import GameContext, SceneManager
    from src.ui.exploration_scene import ExplorationScene
    from src.models.character import Character
    from src.models.classes import Warrior
    
    world = World([[0, 0, 0]])
    npc = NPC("Target", Position(16, 16)) # Tile (0, 0)
    
    # Always wants to move right
    class AggressiveWander(RandomWanderBehavior):
        def _get_random_direction(self): return (1, 0)
        
    npc.ai = AIController(AggressiveWander(move_interval=0.1))
    world.add_interactable(0, 0, npc)
    
    player = Character("Hero", Warrior())
    context = GameContext(player, world)
    context.orchestrator = WorldOrchestrator(None)
    
    manager = SceneManager(context)
    scene = ExplorationScene(manager, None, None)
    
    # 1. Start dialogue (activate interaction manager)
    scene.interaction_manager.active_dialogue = MagicMock()
    
    # 2. Tick
    scene.update(0.2)
    
    # 3. Assert NPC stayed at (0,0) because interaction is active
    assert npc.position.x == 16
    assert world.get_interactable_at(0, 0) is npc
    
    # 4. End dialogue
    scene.interaction_manager.active_dialogue = None
    
    # 5. Tick again
    scene.update(0.2)
    
    # 6. Assert NPC moved to (1,0)
    assert npc.position.x == 48
    assert world.get_interactable_at(1, 0) is npc

def test_dynamic_obstacle_blocks_path_execution():
    """An AI tries to move to a tile, but another entity gets there first."""
    world = World([[0, 0, 0]])
    npc = NPC("SlowNPC", Position(16, 16)) # (0,0)
    npc.ai = AIController(RandomWanderBehavior(move_interval=0.1))
    world.add_interactable(0, 0, npc)
    
    # 1. Manually add an obstacle at (1,0) right before AI ticks
    obstacle = NPC("Obstacle", Position(48, 16))
    world.add_interactable(1, 0, obstacle)
    
    # 2. Force AI to try and move to (1,0)
    # We'll monkeypatch the random direction
    npc.ai.behavior._get_random_direction = lambda: (1, 0)
    
    # 3. Tick
    npc.ai.update(npc, world, 0.2)
    
    # 4. Assert NPC stayed at (0,0) because (1,0) was occupied
    assert npc.position.x == 16
    assert world.get_interactable_at(0, 0) is npc
    assert world.get_interactable_at(1, 0) is obstacle

def test_persistence_sync_check():
    """Simulate a save/load and verify dictionary integrity."""
    from src.core.state import GlobalState
    from src.core.registry import EntityRegistry
    import json
    import os
    
    # Create a dummy map file
    map_data = {
        "grid": [[0, 0], [0, 0]],
        "entities": [
            {"id": "npc_villager", "x": 0, "y": 0, "overrides": {"entity_id": "joao_1"}}
        ]
    }
    with open("temp_map.json", "w") as f:
        json.dump(map_data, f)
        
    registry = EntityRegistry("data/entities.json")
    gs = GlobalState()
    orch = WorldOrchestrator(registry, gs)
    
    # Load map
    world = orch.load_map("temp_map.json")
    npc = world.get_interactable_at(0, 0)
    
    # Move NPC via AI
    npc.ai = AIController(RandomWanderBehavior(move_interval=0.1))
    npc.ai.behavior._get_random_direction = lambda: (1, 0)
    npc.ai.update(npc, world, 0.2) # Moves to (1, 0)
    
    assert world.get_interactable_at(0, 0) is None
    assert world.get_interactable_at(1, 0) is npc
    
    # Simulate Save (what actually happens in persistence.py)
    # It usually saves player pos and global state. 
    # In our PRD, NPCs respawn, but their position could be saved in global_state deltas.
    
    # Let's verify that if we saved the delta, it loads back correctly.
    gs.set_entity_delta("joao_1", {"position": {"x": 48, "y": 16}})
    
    # Reload
    world2 = orch.load_map("temp_map.json")
    
    # The registry should have spawned it at (1,0) instead of (0,0)
    assert world2.get_interactable_at(0, 0) is None
    assert world2.get_interactable_at(1, 0) is not None
    assert world2.get_interactable_at(1, 0).name == "João"
    
    os.remove("temp_map.json")

def test_ai_performance_baseline_50_npcs():
    """Tick 50 NPCs and ensure it stays under a reasonable time budget (e.g. 5ms)."""
    grid = [[0]*10 for _ in range(10)]
    world = World(grid)
    orchestrator = WorldOrchestrator(None)
    
    for i in range(50):
        tx, ty = i % 10, i // 10
        npc = NPC(f"NPC_{i}", Position(tx*32+16, ty*32+16))
        # Wander behavior triggers movement every 0.1s
        npc.ai = AIController(RandomWanderBehavior(move_interval=0.1))
        world.add_interactable(tx, ty, npc)
        
    start_time = time.perf_counter()
    # Simulate a frame update
    orchestrator.update_ai(world, 0.1)
    end_time = time.perf_counter()
    
    duration_ms = (end_time - start_time) * 1000
    print(f"\nAI Performance (50 NPCs): {duration_ms:.4f}ms")
    
    # Even on a slow CI, 50 basic wanders should be sub-10ms. 
    # Python is slow, but dict lookups and basic math are fast.
    assert duration_ms < 10
