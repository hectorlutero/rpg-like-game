import pytest
import pygame
from unittest.mock import MagicMock
from src.models.character import Character

def test_character_get_hitbox_from_metadata(monkeypatch):
    # Setup: Mock AssetManager to return custom hitbox data
    mock_am = MagicMock()
    # sprite metadata: [offset_x, offset_y, w, h]
    mock_am.get_hitbox_data.return_value = [8, 20, 16, 12]
    mock_am.get_sprite_size.return_value = (32, 32)
    
    # We monkeypatch the AssetManager class to return our mock instance
    monkeypatch.setattr("src.core.assets.AssetManager", lambda: mock_am)
    
    # Create Character at (100, 100)
    # Note: Character currently assumes (0,0) as top-left in some contexts, 
    # but world.py's can_move_to treats character as centered.
    # The requirement says "hitbox defined in sprite metadata".
    # Sprites are usually drawn with their center at (x, y) or top-left.
    # Let's assume Character.position is the top-left of the sprite for hitbox offset simplicity,
    # OR follow the current centered convention. 
    # If the sprite is 32x32, and position is center (100, 100), 
    # the sprite top-left is (84, 84).
    # Hitbox offset [8, 20] from top-left (84, 84) -> (92, 104).
    # Hitbox size 16x12 -> Rect(92, 104, 16, 12).
    
    char = Character("Hero", MagicMock())
    char.position.x = 100
    char.position.y = 100
    char.sprite_sheet_id = "hero_sheet"
    char.sprite_id = "idle_S"
    
    # Execute
    hitbox = char.get_hitbox()
    
    # Verify
    # Assuming for now Character.position is CENTER (matching world.can_move_to logic)
    # and sprite is 32x32 (standard in this project)
    expected_x = 100 - 16 + 8   # Center - half_width + offset_x
    expected_y = 100 - 16 + 20  # Center - half_height + offset_y
    
    assert hitbox.x == expected_x
    assert hitbox.y == expected_y
    assert hitbox.width == 16
    assert hitbox.height == 12
    assert isinstance(hitbox, pygame.Rect)

def test_world_rect_tile_collision():
    from src.models.world import World
    # 3x3 grid, center is empty, top is solid
    grid = [
        [1, 1, 1],
        [0, 0, 0],
        [0, 0, 0]
    ]
    world = World(grid, tile_size=32)
    
    # 1. Collision with top wall
    # Rect at (32, 10) width 16, height 16. 
    # Y=10 is inside tile_y=0 (0-31)
    rect_colliding = pygame.Rect(32, 10, 16, 16)
    assert world.is_collision(rect_colliding) == True
    
    # 2. No collision in the middle
    rect_safe = pygame.Rect(32, 40, 16, 16)
    assert world.is_collision(rect_safe) == False
    
    # 3. Out of bounds (left)
    rect_oob = pygame.Rect(-5, 40, 10, 10)
    assert world.is_collision(rect_oob) == True

def test_world_entity_hitbox_collision(monkeypatch):
    from src.models.world import World
    
    # Grid is all empty
    grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    world = World(grid, tile_size=32)
    
    # Mock NPC with get_hitbox
    mock_npc = MagicMock()
    # NPC at (32, 32) with a 10x10 hitbox at its center
    mock_npc.get_hitbox.return_value = pygame.Rect(32+11, 32+11, 10, 10)
    
    # Register NPC in world
    world.add_interactable(1, 1, mock_npc)
    
    # 1. Collision with NPC hitbox
    rect_colliding = pygame.Rect(40, 40, 10, 10) # Overlaps (43, 43, 10, 10)
    assert world.is_collision(rect_colliding) == True
    
    # 2. Ignore itself
    assert world.is_collision(rect_colliding, ignore_entity=mock_npc) == False
    
    # 3. No collision nearby
    rect_safe = pygame.Rect(0, 0, 10, 10)
    assert world.is_collision(rect_safe) == False

def test_organic_movement_behind_tall_sprite(monkeypatch):
    from src.models.world import World, Position
    from src.models.interaction import Interactable
    
    grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    world = World(grid, tile_size=32)
    
    # Mock AssetManager for the Tree
    mock_am = MagicMock()
    # Tree is 32x64. Position (50, 60) is center.
    # Top-left = (50-16, 60-32) = (34, 28)
    # Trunk hitbox: relative to top-left of 32x64, let's say it's at the bottom 16px.
    # [ox, oy, w, h] = [8, 48, 16, 16]
    mock_am.get_sprite_size.return_value = (32, 64)
    mock_am.get_hitbox_data.return_value = [8, 48, 16, 16]
    
    monkeypatch.setattr("src.core.assets.AssetManager", lambda: mock_am)
    
    # Create Tree
    tree = Interactable()
    tree.sprite_sheet_id = "nature"
    tree.sprite_id = "tree"
    tree.position = Position(50, 60)
    
    world.add_interactable(1, 1, tree) # Adding at tile 1,1 for registry
    
    # Player trying to walk "behind" the tree top (no collision)
    # Tree top-left is (34, 28). Top-half is (34, 28, 32, 32)
    # Trunk is at y >= 28 + 48 = 76.
    
    # Player at (50, 40) - should be safe (behind leaves)
    player_rect_behind = pygame.Rect(45, 35, 10, 10)
    assert world.is_collision(player_rect_behind) == False
    
    # Player at (50, 80) - should COLLIDE (hitting the trunk)
    # Trunk is [34+8, 28+48, 16, 16] = [42, 76, 16, 16]
    player_rect_hitting = pygame.Rect(45, 75, 10, 10)
    assert world.is_collision(player_rect_hitting) == True
