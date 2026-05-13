import os
import sys
import time
import pytest
import pygame
from src.models.world import World

# Check if --watch is passed to pytest
WATCH_MODE = "--watch" in sys.argv

if not WATCH_MODE:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'

class MockEntity:
    def __init__(self, color):
        self.color = color

def setup_pygame():
    if WATCH_MODE:
        pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Immediate Tile Claiming E2E")
        return screen
    return None

def draw_grid(screen, world, case_name, action_text=""):
    if not WATCH_MODE:
        return

    tile_size = 32
    screen.fill((20, 20, 20))
    
    # Draw Grid and Walls
    for y, row in enumerate(world.grid):
        for x, val in enumerate(row):
            color = (50, 50, 50) if val == 0 else (100, 100, 100) # Floor = dark gray, Wall = gray
            rect = (x * tile_size, y * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (30, 30, 30), rect, 1) # border

    # Draw Entities
    for (tx, ty), entity in world.interactables.items():
        rect = (tx * tile_size + 8, ty * tile_size + 8, tile_size - 16, tile_size - 16)
        pygame.draw.rect(screen, entity.color, rect)
        
    # Draw Text
    if pygame.font.get_init():
        font = pygame.font.SysFont(None, 24)
        text1 = font.render(case_name, True, (255, 255, 255))
        screen.blit(text1, (10, len(world.grid) * tile_size + 10))
        
        if action_text:
            text2 = font.render(action_text, True, (255, 255, 0)) # Yellow text for actions
            screen.blit(text2, (10, len(world.grid) * tile_size + 40))

    pygame.display.flip()
    
    # Keep window responsive
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def animate_attempt(screen, world, case_name, from_pos, to_pos, success):
    if not WATCH_MODE:
        return
        
    fx, fy = from_pos
    tx, ty = to_pos
    
    draw_grid(screen, world, case_name, f"Attempting move: ({fx},{fy}) -> ({tx},{ty})")
    time.sleep(1.5)
    
    if success:
        draw_grid(screen, world, case_name, "Success! Tile Claimed.")
    else:
        draw_grid(screen, world, case_name, "Rejected! Collision Detected.")
        
    time.sleep(2)

def test_tile_claiming_e2e_scenarios():
    screen = setup_pygame()
    
    grid = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0], # Wall in the middle
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]
    world = World(grid)
    
    player_entity = MockEntity((0, 255, 0)) # Green
    npc_entity = MockEntity((0, 0, 255)) # Blue
    
    # Initial state
    world.add_interactable(1, 1, player_entity)
    world.add_interactable(3, 1, npc_entity)
    
    if WATCH_MODE:
        draw_grid(screen, world, "Initial State")
        time.sleep(1.5)
    
    # Case 1: Successful Move into empty tile
    case_name = "Case 1: Successful Move"
    success = world.move_interactable(1, 1, 2, 1)
    assert success is True
    animate_attempt(screen, world, case_name, (1, 1), (2, 1), success)
    
    # Case 2: Collision with Wall
    case_name = "Case 2: Wall Collision"
    success = world.move_interactable(2, 1, 2, 2)
    assert success is False
    animate_attempt(screen, world, case_name, (2, 1), (2, 2), success)
    
    # Case 3: Collision with another Entity (Immediate Claiming resolution)
    case_name = "Case 3: Entity Collision"
    success = world.move_interactable(2, 1, 3, 1)
    assert success is False
    animate_attempt(screen, world, case_name, (2, 1), (3, 1), success)

    if WATCH_MODE:
        pygame.quit()
