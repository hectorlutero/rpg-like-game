import os
import sys
import time
import pytest
import pygame
from src.logic.pathfinding import PathfindingEngine

# Check if --watch is passed to pytest
WATCH_MODE = "--watch" in sys.argv

if not WATCH_MODE:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'

def create_is_walkable(grid):
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    def is_walkable(x, y):
        if not (0 <= x < width and 0 <= y < height):
            return False
        return grid[y][x] == 0
    return is_walkable

def draw_grid_and_path(screen, grid, start, target, path, case_name):
    if not WATCH_MODE:
        return

    tile_size = 32
    screen.fill((20, 20, 20))
    
    # Draw Grid
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            color = (50, 50, 50) if val == 0 else (100, 100, 100) # Floor = dark gray, Wall = gray
            rect = (x * tile_size, y * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (30, 30, 30), rect, 1) # border
            
    # Draw Path
    for (px, py) in path:
        rect = (px * tile_size + 8, py * tile_size + 8, tile_size - 16, tile_size - 16)
        pygame.draw.rect(screen, (0, 255, 0), rect) # Green
        
    # Draw Start and Target
    pygame.draw.rect(screen, (0, 0, 255), (start[0] * tile_size + 4, start[1] * tile_size + 4, tile_size - 8, tile_size - 8)) # Blue
    pygame.draw.rect(screen, (255, 0, 0), (target[0] * tile_size + 4, target[1] * tile_size + 4, tile_size - 8, tile_size - 8)) # Red
    
    # Draw Case Name
    if pygame.font.get_init():
        font = pygame.font.SysFont(None, 24)
        text = font.render(case_name, True, (255, 255, 255))
        screen.blit(text, (10, len(grid) * tile_size + 10))

    pygame.display.flip()
    
    # Let user see the path
    for _ in range(20): # 2 seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        time.sleep(0.1)

def setup_pygame():
    if WATCH_MODE:
        pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("A* Pathfinding E2E")
        return screen
    return None

def test_pathfinding_e2e_scenarios():
    screen = setup_pygame()
    engine = PathfindingEngine()
    
    # Case 1: Straight Path
    grid_straight = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    start_1 = (1, 2)
    target_1 = (8, 2)
    path_1 = engine.find_path(start_1, target_1, create_is_walkable(grid_straight))
    assert len(path_1) == 7
    draw_grid_and_path(screen, grid_straight, start_1, target_1, path_1, "Case 1: Straight Path")
    
    # Case 2: U-Shape Obstacle
    grid_u = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    start_2 = (4, 3)
    target_2 = (4, 0)
    path_2 = engine.find_path(start_2, target_2, create_is_walkable(grid_u))
    assert len(path_2) > 0 # Must have a path around
    assert target_2 in path_2
    draw_grid_and_path(screen, grid_u, start_2, target_2, path_2, "Case 2: U-Shape Obstacle Evasion")
    
    # Case 3: Unreachable Target (Closed Box)
    grid_box = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    start_3 = (4, 2)
    target_3 = (4, 0)
    path_3 = engine.find_path(start_3, target_3, create_is_walkable(grid_box))
    assert len(path_3) == 0 # Graceful failure
    draw_grid_and_path(screen, grid_box, start_3, target_3, path_3, "Case 3: Unreachable Target")
    
    # Case 4: Target is inside wall
    start_4 = (1, 2)
    target_4 = (4, 3) # (4,3) is a wall in grid_box
    path_4 = engine.find_path(start_4, target_4, create_is_walkable(grid_box))
    assert len(path_4) == 0 # Target itself is not walkable
    draw_grid_and_path(screen, grid_box, start_4, target_4, path_4, "Case 4: Target in Wall")

    if WATCH_MODE:
        pygame.quit()
