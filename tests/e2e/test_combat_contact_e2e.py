import os
import sys
import time
import pytest
import pygame
from unittest.mock import MagicMock
from src.core.registry import EntityRegistry
from src.core.state import GlobalState
from src.core.orchestrator import WorldOrchestrator
from src.models.character import Character
from src.models.classes import Warrior
from src.ui.scenes import GameContext, SceneManager
from src.ui.exploration_scene import ExplorationScene
from src.models.world import World, Position
from src.models.combat import EnemyInteractable

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
        pygame.display.set_caption("Combat Contact E2E")
        return screen
    return None

def test_combat_contact_engagement_e2e():
    screen = setup_pygame()
    
    registry = EntityRegistry("data/entities.json")
    global_state = GlobalState()
    orchestrator = WorldOrchestrator(registry, global_state)
    
    player = Character("Hero", Warrior())
    player.position = Position(16, 16) # Tile (0, 0)
    
    grid = [[0, 0, 0], [0, 0, 0]]
    world = World(grid)
    
    context = GameContext(player, world)
    context.orchestrator = orchestrator
    context.global_state = global_state
    
    manager = SceneManager(context)
    context.scene_manager = manager
    scene = ExplorationScene(manager, None, None)
    manager.push(scene)
    
    # Spawn Enemy at (2, 0)
    enemy = EnemyInteractable("Slime", Warrior(), 1, world_pos=Position(2*32+16, 16))
    world.add_interactable(2, 0, enemy)
    
    def render_all(msg=""):
        if not WATCH_MODE: return
        screen.fill((20, 20, 20))
        for y, row in enumerate(world.grid):
            for x, val in enumerate(row):
                pygame.draw.rect(screen, (50, 50, 50), (x*32, y*32, 32, 32))
                pygame.draw.rect(screen, (30, 30, 30), (x*32, y*32, 32, 32), 1)
        
        # Enemy
        ex, ey = int(enemy.position.x // 32), int(enemy.position.y // 32)
        if (ex, ey) in world.interactables:
            pygame.draw.rect(screen, (255, 50, 50), (ex*32+4, ey*32+4, 24, 24))
        
        # Player
        px, py = int(player.position.x // 32), int(player.position.y // 32)
        pygame.draw.circle(screen, (50, 50, 255), (px*32+16, py*32+16), 12)
        
        if pygame.font.get_init():
            font = pygame.font.SysFont(None, 24)
            img = font.render(msg, True, (255, 255, 255))
            screen.blit(img, (10, 100))
            
        pygame.display.flip()
        time.sleep(0.1)

    # 1. Player walks into Enemy
    render_all("Walking into enemy...")
    
    # Move player right
    # (0, 0) -> (1, 0) -> contact at (2, 0)
    original_get_pressed = pygame.key.get_pressed
    try:
        pygame.key.get_pressed = MagicMock(return_value={
            pygame.K_RIGHT: True, pygame.K_d: False, pygame.K_LEFT: False, 
            pygame.K_a: False, pygame.K_UP: False, pygame.K_w: False, 
            pygame.K_DOWN: False, pygame.K_s: False
        })
        
        for _ in range(8): # 32 pixels / 4 speed = 8 steps
            scene.update(0.016)
            render_all("Walking into enemy...")
            
        # Now player at (1, 0)
        assert int(player.position.x // 32) == 1
        
        # Move again to hit (2, 0)
        for _ in range(8):
            scene.update(0.016)
            render_all("About to hit enemy...")
            if manager.active_scene != scene:
                break
    finally:
        pygame.key.get_pressed = original_get_pressed
            
    # Should have triggered combat
    assert manager.active_scene != scene
    assert manager.active_scene.__class__.__name__ == "CombatScene"
    
    if WATCH_MODE:
        render_all("Combat Started!")
        time.sleep(1)
        
    # 2. Simulate Victory
    combat_scene = manager.active_scene
    combat_scene.combat_manager.is_over = True
    combat_scene.combat_manager.winner = "Party"
    combat_scene._handle_battle_end()
    
    # Should be back to ExplorationScene
    assert manager.active_scene == scene
    
    # Enemy should be gone from the map
    assert world.get_interactable_at(2, 0) is None
    
    if WATCH_MODE:
        render_all("Victory! Enemy removed.")
        time.sleep(1)
        pygame.quit()
