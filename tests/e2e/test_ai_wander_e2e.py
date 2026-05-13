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
        pygame.display.set_caption("AI Random Wander E2E")
        return screen
    return None

def test_ai_wander_e2e():
    screen = setup_pygame()
    
    # 1. Setup real dependencies
    registry = EntityRegistry("data/entities.json")
    global_state = GlobalState()
    orchestrator = WorldOrchestrator(registry, global_state)
    
    player = Character("Hero", Warrior())
    # Small 5x5 grid with a wall
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    from src.models.world import World
    world = World(grid)
    
    context = GameContext(player, world)
    context.orchestrator = orchestrator
    context.global_state = global_state
    
    manager = SceneManager(context)
    scene = ExplorationScene(manager, None, None)
    manager.push(scene)
    
    # 2. Spawn NPC with RandomWander (move every 0.5s for testing)
    from src.logic.ai_controller import AIController, RandomWanderBehavior
    npc = registry.spawn_to_map("npc_villager", world, 0, 0)
    npc.ai = AIController(RandomWanderBehavior(move_interval=0.5))
    
    initial_pos = (npc.position.x, npc.position.y)
    
    # 3. Simulation Loop
    # We want to see it move at least 3 times
    moves_detected = 0
    last_pos = initial_pos
    
    max_steps = 100
    dt = 0.1
    
    for i in range(max_steps):
        scene.update(dt)
        
        current_pos = (npc.position.x, npc.position.y)
        if current_pos != last_pos:
            moves_detected += 1
            last_pos = current_pos
            
        if WATCH_MODE:
            screen.fill((20, 20, 20))
            # Draw Grid
            for y, row in enumerate(world.grid):
                for x, val in enumerate(row):
                    color = (50, 50, 50) if val == 0 else (100, 100, 100)
                    pygame.draw.rect(screen, color, (x*32, y*32, 32, 32))
                    pygame.draw.rect(screen, (30, 30, 30), (x*32, y*32, 32, 32), 1)
            
            # Draw NPC
            pygame.draw.rect(screen, (50, 200, 50), (npc.position.x - 12, npc.position.y - 12, 24, 24))
            
            # Text
            if pygame.font.get_init():
                font = pygame.font.SysFont(None, 24)
                text = font.render(f"Moves: {moves_detected}", True, (255, 255, 255))
                screen.blit(text, (10, 170))
                
            pygame.display.flip()
            time.sleep(0.05)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
        if moves_detected >= 3:
            break

    assert moves_detected >= 3
    if WATCH_MODE:
        time.sleep(1)
        pygame.quit()
