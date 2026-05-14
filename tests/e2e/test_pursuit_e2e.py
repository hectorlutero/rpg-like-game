import os
import sys
import time
import pytest
import pygame
from src.core.registry import EntityRegistry
from src.core.state import GlobalState
from src.core.orchestrator import WorldOrchestrator
from src.models.character import Character
from src.models.classes import Warrior
from src.ui.scenes import GameContext, SceneManager
from src.ui.exploration_scene import ExplorationScene
from src.models.world import World, Position

# Check if --watch is passed to pytest
WATCH_MODE = "--watch" in sys.argv

if not WATCH_MODE:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'

def setup_pygame():
    if WATCH_MODE:
        pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("AI Pursuit E2E")
        return screen
    return None

def test_ai_pursuit_and_leash_e2e():
    screen = setup_pygame()
    
    registry = EntityRegistry("data/entities.json")
    global_state = GlobalState()
    orchestrator = WorldOrchestrator(registry, global_state)
    
    player = Character("Hero", Warrior())
    player.position = Position(8*32+16, 1*32+16) # Far right top
    
    # 10x10 grid with a U-wall in the middle
    grid = [[0]*10 for _ in range(10)]
    # U-wall
    grid[3][3:7] = [1]*4
    grid[4][3] = 1
    grid[4][6] = 1
    grid[5][3:7] = [1]*4
    
    world = World(grid)
    
    context = GameContext(player, world)
    context.orchestrator = orchestrator
    context.global_state = global_state
    
    manager = SceneManager(context)
    scene = ExplorationScene(manager, None, None)
    manager.push(scene)
    
    # Spawn Enemy with Pursuit (spawn at 1,1)
    from src.logic.ai_controller import AIController, PursuitBehavior
    # Manual setup because entities.json might not have pursuit yet
    enemy = registry.spawn("npc_villager", position={"x": 32+16, "y": 32+16}) 
    enemy.name = "Stalker"
    enemy.color = (255, 50, 50) # Red
    enemy.ai = AIController(PursuitBehavior(player=player, los_range=10, leash_range=5, move_interval=0.2))
    world.add_interactable(1, 1, enemy)
    
    def render_all(msg=""):
        if not WATCH_MODE: return
        screen.fill((20, 20, 20))
        for y, row in enumerate(world.grid):
            for x, val in enumerate(row):
                color = (50, 50, 50) if val == 0 else (100, 100, 100)
                pygame.draw.rect(screen, color, (x*25, y*25, 25, 25))
                pygame.draw.rect(screen, (30, 30, 30), (x*25, y*25, 25, 25), 1)
        
        # Spawn point (1,1)
        pygame.draw.rect(screen, (255, 255, 255), (1*25+8, 1*25+8, 9, 9), 1)
        
        # Enemy
        ex, ey = int(enemy.position.x // world.tile_size), int(enemy.position.y // world.tile_size)
        pygame.draw.rect(screen, (255, 50, 50), (ex*25+4, ey*25+4, 17, 17))
        
        # Player
        px, py = int(player.position.x // world.tile_size), int(player.position.y // world.tile_size)
        pygame.draw.circle(screen, (50, 50, 255), (px*25+12, py*25+12), 8)
        
        if pygame.font.get_init():
            font = pygame.font.SysFont(None, 20)
            img = font.render(msg, True, (255, 255, 0))
            screen.blit(img, (10, 260))
            
        pygame.display.flip()
        time.sleep(0.1)

    # Simulation phase 1: Player stays far. Enemy doesn't see or is idle.
    # Actually, player at (8,1), enemy at (1,1). Dist is 7. LoS range is 10.
    # Enemy should see player and start chasing.
    
    for _ in range(30):
        scene.update(0.1)
        render_all("Enemy Pursuing Player...")
        # Check if enemy moved closer to player
        if int(enemy.position.x // 32) > 1:
            break
            
    assert int(enemy.position.x // 32) > 1 # Proves pursuit started
    
    # Simulation phase 2: Move player beyond leash range
    # Spawn is (1,1). Leash is 5.
    # Move player to (9,9)
    player.position.x = 9*32+16
    player.position.y = 9*32+16
    
    # Wait for enemy to move far from spawn (say to tile 7,1)
    for _ in range(50):
        scene.update(0.1)
        render_all("Player fled! Enemy chasing...")
        if int(enemy.position.x // 32) >= 6:
            break
            
    # Now enemy should leash because it's at (6,1) and spawn is (1,1) -> dist is 5.
    # Next step will be 6.0 > 5, so leashing.
    
    for _ in range(50):
        scene.update(0.1)
        render_all("Leashing! Returning to spawn...")
        # Check if enemy is returning to (1,1)
        if int(enemy.position.x // 32) < 6:
            break
            
    assert int(enemy.position.x // 32) < 6 # Proves leashing started

    if WATCH_MODE:
        pygame.quit()
