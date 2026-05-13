import pytest
import pygame
from unittest.mock import MagicMock
from src.ui.exploration_scene import ExplorationScene
from src.models.interaction import Portal, InteractionManager, TransitionRequest
from src.models.world import Position

# Initialize pygame for font support in tests
pygame.init()
pygame.display.set_mode((1,1), pygame.HIDDEN)

class MockContext:
    def __init__(self, world, player):
        self.world = world
        self.player = player
        self.save_manager = MagicMock()
        self.signal_bus = MagicMock()

class MockPlayer:
    def __init__(self, x, y):
        self.position = Position(x, y)
        self.facing_direction = "S"
        self.energy = 3
    def update_orientation(self, dx, dy):
        if dx > 0: self.facing_direction = "E"
        elif dx < 0: self.facing_direction = "W"
        elif dy > 0: self.facing_direction = "S"
        elif dy < 0: self.facing_direction = "N"

class SimpleManager:
    def __init__(self, context):
        self.context = context
        self.active_scene = None

def test_step_on_portal_trigger():
    # Setup world with a portal
    world = MagicMock()
    world.tile_size = 32
    portal = Portal(target_map="forest.json", target_tag="entrance", require_interaction=False)
    
    # Mock get_interactable_at: portal is at (1, 1) -> pixels (32-63, 32-63)
    world.get_interactable_at.side_effect = lambda tx, ty: portal if (tx == 1 and ty == 1) else None
    world.can_move_to.return_value = True
    
    player = MockPlayer(16, 16) # Tile (0, 0)
    context = MockContext(world, player)
    
    manager = SimpleManager(context)
    scene = ExplorationScene(manager, None, None)
    manager.active_scene = scene
    scene.trigger_transition = MagicMock()
    
    # Simulate move to (48, 48) -> Tile (1, 1)
    player.position.x = 48
    player.position.y = 48
    scene._check_on_step_triggers()
    
    scene.trigger_transition.assert_called_once()
    request = scene.trigger_transition.call_args[0][0]
    assert isinstance(request, TransitionRequest)
    assert request.target_map == "forest.json"

def test_manual_portal_trigger():
    world = MagicMock()
    world.tile_size = 32
    portal = Portal(target_map="forest.json", target_tag="entrance", require_interaction=True)
    
    # Portal is south of player (at 1, 2)
    world.get_interactable_at.side_effect = lambda tx, ty: portal if (tx == 1 and ty == 2) else None
    
    player = MockPlayer(48, 48) # Tile (1, 1), facing South
    context = MockContext(world, player)
    
    manager = SimpleManager(context)
    scene = ExplorationScene(manager, None, None)
    manager.active_scene = scene
    scene.trigger_transition = MagicMock()
    
    # Interact manually
    scene.interaction_manager.interact()
    
    # The interaction manager should have a requested_transition now
    print(f"TEST_DEBUG: requested_transition before update: {scene.interaction_manager.requested_transition}")
    assert scene.interaction_manager.requested_transition is not None
    
    # ExplorationScene.update will process it
    scene.update(0)
    print(f"TEST_DEBUG: requested_transition after update: {scene.interaction_manager.requested_transition}")
    
    scene.trigger_transition.assert_called_once()
    assert scene.interaction_manager.requested_transition is None
