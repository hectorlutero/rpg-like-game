import os
import sys
import time
import pygame
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World
from src.ui.scenes import GameContext, SceneManager

# Check if --watch is passed to pytest
WATCH_MODE = "--watch" in sys.argv

if not WATCH_MODE:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
elif 'SDL_VIDEODRIVER' in os.environ:
    del os.environ['SDL_VIDEODRIVER']

class UITester:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        if WATCH_MODE:
            pygame.display.set_caption("ROBÔ RPG: Assistindo a Automação")
        self.world = World([[0]*10 for _ in range(10)])
        self.player = Character("Tester", Warrior())
        self.context = GameContext(self.player, self.world)
        self.manager = SceneManager(self.context)
        self.watch = WATCH_MODE
        
        # Initial draw
        self._render_watch(1.0)

    def _render_watch(self, delay=1.0):
        if self.watch:
            self.screen.fill((20, 20, 20))
            self.manager.draw(self.screen)
            pygame.display.flip()
            # Process events so the window doesn't freeze
            for event in pygame.event.get():
                pass
            time.sleep(delay)

    def post_key(self, key, delay=1.0):
        event = pygame.event.Event(pygame.KEYDOWN, {'key': key})
        self.manager.handle_event(event)
        self.manager.update(0.1)
        self._render_watch(delay)
    
    def wait_for_player_turn(self, timeout_steps=1000):
        """Advances time until it's the player's turn or timeout."""
        for _ in range(timeout_steps):
            if self.manager.active_scene.combat_manager.is_waiting_for_input:
                self._render_watch(0.5)
                return True
            self.manager.update(0.1)
            self._render_watch(0.05)
        return False
