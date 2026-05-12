import pygame
import sys
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World
from src.ui.scenes import GameContext, SceneManager

class E2EBase:
    def __init__(self, title="E2E Test"):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        
        # Default empty world
        self.world = World([[0]*25 for _ in range(20)])
        self.player = Character("Tester", Warrior())
        self.context = GameContext(self.player, self.world)
        self.context.screen = self.screen
        self.manager = SceneManager(self.context)
        self.context.scene_manager = self.manager

    def handle_debug_keys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h: # Heal
                self.player.hp = self.player.max_hp
                print("DEBUG: Player Healed")
            if event.key == pygame.K_g: # Gold
                self.player.gold += 100
                print(f"DEBUG: +100 Gold (Total: {self.player.gold})")

    def run(self, initial_scene):
        self.manager.push(initial_scene)
        
        while self.context.running:
            dt = self.clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.context.running = False
                self.handle_debug_keys(event)
                self.manager.handle_event(event)
            
            self.manager.update(dt)
            self.screen.fill((30, 30, 30))
            self.manager.draw(self.screen)
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()
