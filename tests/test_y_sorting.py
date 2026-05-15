import pytest
import pygame
from unittest.mock import MagicMock
from src.ui.exploration_scene import ExplorationScene

class MockEntity:
    def __init__(self, y):
        self.y = y
        self.draw = MagicMock()

def test_y_sorting_logic():
    # Setup
    entities = [
        MockEntity(100),
        MockEntity(50),
        MockEntity(150)
    ]
    
    # We want to verify that when we sort them by Y, they are in the right order
    sorted_entities = sorted(entities, key=lambda e: e.y)
    
    assert sorted_entities[0].y == 50
    assert sorted_entities[1].y == 100
    assert sorted_entities[2].y == 150

def test_scene_draw_world_sorting(monkeypatch):
    # This test will verify that ExplorationScene._draw_world calls draw in the correct Y order.
    # We need to mock context, world, and pygame.
    
    mock_manager = MagicMock()
    mock_context = MagicMock()
    
    # Mock World
    mock_world = MagicMock()
    mock_world.tile_size = 32
    mock_world.grid = [[0]] # 1x1 grid
    mock_world.tileset_id = None
    
    # Mock Player
    mock_player = MagicMock()
    mock_player.position.x = 16
    mock_player.position.y = 80 # Player at Y=80
    
    # Mock Interactables
    mock_npc = MagicMock()
    # If we put NPC at tile (0,0), its base Y is tile_size // 2 = 16
    
    mock_world.interactables = {
        (0, 0): mock_npc
    }
    
    mock_context.world = mock_world
    mock_context.player = mock_player
    mock_manager.context = mock_context
    
    # Initialize Scene (avoiding full init if possible, or mocking parts)
    monkeypatch.setattr(ExplorationScene, "__init__", lambda self, m, p=None, s=None: None)
    scene = ExplorationScene(mock_manager)
    scene.context = mock_context
    
    # We will record the order of calls to draw
    draw_order = []
    
    def player_draw(screen, pos):
        draw_order.append("player")
    
    def npc_draw(screen, context, pos):
        draw_order.append("npc")
        
    mock_player.draw = player_draw
    mock_npc.draw = npc_draw
    
    # Mock pygame.draw.rect and AssetManager to avoid errors
    monkeypatch.setattr("pygame.draw.rect", MagicMock())
    monkeypatch.setattr("src.core.assets.AssetManager", MagicMock())
    
    # Execute
    mock_screen = MagicMock()
    # Mock blit as well just in case
    mock_screen.blit = MagicMock()
    
    scene._draw_world(mock_screen)
    
    # Verify: NPC (at 16) should be drawn before Player (at 80)
    assert draw_order == ["npc", "player"]
    
    # Swap positions and test again
    draw_order.clear()
    mock_player.position.y = 10 # Player now at 10, NPC at 16
    scene._draw_world(mock_screen)
    assert draw_order == ["player", "npc"]
