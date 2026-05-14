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
        pygame.display.set_caption("AI Combat Contact E2E")
        return screen
    return None

def test_ai_contact_engagement_e2e():
    screen = setup_pygame()
    
    registry = EntityRegistry("data/entities.json")
    global_state = GlobalState()
    orchestrator = WorldOrchestrator(registry, global_state)
    
    # Player at (0, 0)
    player = Character("Hero", Warrior())
    player.position = Position(16, 16) 
    
    grid = [[0, 0, 0], [0, 0, 0]]
    world = World(grid)
    
    context = GameContext(player, world)
    context.orchestrator = orchestrator
    context.global_state = global_state
    from src.core.signals import SignalBus
    context.signal_bus = SignalBus()
    
    manager = SceneManager(context)
    context.scene_manager = manager
    scene = ExplorationScene(manager, None, None)
    manager.push(scene)
    
    # Spy on emit
    original_emit = context.signal_bus.emit
    context.signal_bus.emit = MagicMock(side_effect=original_emit)
    
    # Spawn Enemy at (1, 0)
    enemy = EnemyInteractable("Slime", Warrior(), 1, world_pos=Position(48, 16))
    world.add_interactable(1, 0, enemy)
    
    # Give Enemy REAL Pursuit AI
    from src.logic.ai_controller import AIController, PursuitBehavior
    # LoS 10, leash 10, move every 0.1s
    enemy.ai = AIController(PursuitBehavior(player=player, los_range=10, leash_range=10, move_interval=0.1))
    
    def render_all(msg=""):
        if not WATCH_MODE: return
        screen.fill((20, 20, 20))
        for y, row in enumerate(world.grid):
            for x, val in enumerate(row):
                pygame.draw.rect(screen, (50, 50, 50), (x*32, y*32, 32, 32))
        
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
        time.sleep(0.5)

    # Act
    render_all("AI moving into player...")
    scene.update(0.2) # Tick AI (must be > move_interval 0.1)
    
    # Assert Signal emitted
    context.signal_bus.emit.assert_called_with("START_COMBAT", target=enemy)
    
    # Assert Combat Scene pushed
    assert manager.active_scene.__class__.__name__ == "CombatScene"
    
    if WATCH_MODE:
        render_all("Combat Triggered by AI!")
        time.sleep(1)
        pygame.quit()
