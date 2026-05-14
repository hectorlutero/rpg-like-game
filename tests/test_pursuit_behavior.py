import pytest
from unittest.mock import MagicMock
from src.logic.ai_controller import AIController, PursuitBehavior
from src.models.world import World, Position
from src.models.dialogue import NPC

def test_pursuit_behavior_triggers_on_los():
    # Setup world with player and enemy
    grid = [[0]*10 for _ in range(10)]
    world = World(grid)
    
    # Player at (5, 5)
    player = MagicMock()
    player.position = Position(5*32+16, 5*32+16)
    
    # Enemy at (2, 5) - clear line of sight
    enemy = NPC("Slime", Position(2*32+16, 5*32+16))
    world.add_interactable(2, 5, enemy)
    
    # Pursuit behavior with LoS range of 4 tiles
    behavior = PursuitBehavior(player=player, los_range=4, leash_range=8)
    enemy.ai = AIController(behavior)
    
    # Initially enemy at (2, 5)
    assert (int(enemy.position.x // 32), int(enemy.position.y // 32)) == (2, 5)
    
    # Tick AI
    # It should see player at distance 3, and move towards them
    behavior.update(enemy, world, 1.0)
    
    # Enemy should have moved towards player (to the right)
    assert (int(enemy.position.x // 32), int(enemy.position.y // 32)) == (3, 5)
    assert world.get_interactable_at(2, 5) is None
    assert world.get_interactable_at(3, 5) is enemy

def test_pursuit_behavior_leashes_when_too_far():
    # Setup world
    grid = [[0]*20 for _ in range(20)]
    world = World(grid)
    
    # Spawn is (0, 0)
    enemy = NPC("Slime", Position(16, 16))
    world.add_interactable(0, 0, enemy)
    
    # Player is far away (15, 0) - beyond leash range of 10
    player = MagicMock()
    player.position = Position(15*32+16, 0*32+16)
    
    behavior = PursuitBehavior(player=player, los_range=20, leash_range=10)
    enemy.ai = AIController(behavior)
    
    # Tick once at spawn to capture spawn_pos = (0, 0)
    behavior.update(enemy, world, 0.0)
    assert behavior.spawn_pos == (0, 0)
    
    # Move enemy to (11, 0) - beyond leash range of 10
    world.move_interactable(0, 0, 11, 0)
    enemy.position.x = 11*32+16
    
    # Tick AI - should trigger leashing
    behavior.update(enemy, world, 1.0)
    
    # Enemy should start returning towards spawn (0,0)
    # So it should move left from (11, 0) to (10, 0)
    assert (int(enemy.position.x // 32), int(enemy.position.y // 32)) == (10, 0)

def test_pursuit_behavior_respects_walls():
    # Setup world with a wall blocking LoS
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0], # Wall at (1,1), (2,1), (3,1)
        [0, 0, 0, 0, 0],
    ]
    world = World(grid)
    
    # Player at (2, 0)
    player = MagicMock()
    player.position = Position(2*32+16, 0*32+16)
    
    # Enemy at (2, 2)
    enemy = NPC("Slime", Position(2*32+16, 2*32+16))
    world.add_interactable(2, 2, enemy)
    
    behavior = PursuitBehavior(player=player, los_range=5)
    enemy.ai = AIController(behavior)
    
    # Tick AI - wall blocks LoS, so no movement
    behavior.update(enemy, world, 1.0)
    
    assert (int(enemy.position.x // 32), int(enemy.position.y // 32)) == (2, 2)
