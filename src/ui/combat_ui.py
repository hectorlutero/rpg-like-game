import pygame
import math

class CombatUI:
    def __init__(self, screen):
        self.screen = screen
        self.font_small = pygame.font.SysFont("Arial", 16)
        self.font_medium = pygame.font.SysFont("Arial", 22)
        
    def draw_circular_meter(self, x, y, radius, percentage, color=(0, 255, 255)):
        """Draws a circular ATB meter."""
        # Draw background circle (faded)
        pygame.draw.circle(self.screen, (50, 50, 50), (x, y), radius, 2)
        
        if percentage <= 0:
            return

        # Pygame arc uses radians and starts from 0 (right). 
        # We want it to start from top (-PI/2) and go clockwise.
        start_angle = -math.pi / 2
        end_angle = start_angle + (2 * math.pi * (percentage / 100.0))
        
        rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        
        # Draw the progress arc
        if percentage > 0:
            # We use a loop or multiple arcs to simulate thickness if needed, 
            # but simple arc works for now.
            pygame.draw.arc(self.screen, color, rect, -end_angle, -start_angle, 3)

    def draw_combat_scene(self, party, enemies, combat_manager):
        # 1. Draw Entities
        # Enemies on the Left
        for i, enemy in enumerate(enemies):
            ex, ey = 150, 150 + (i * 100)
            pygame.draw.rect(self.screen, (200, 50, 50), (ex - 20, ey - 20, 40, 40))
            self.draw_text(enemy.name, ex, ey - 40, color=(255, 100, 100))
            # HP Bar
            self.draw_hp_bar(ex - 30, ey + 30, 60, 8, enemy.hp, enemy.max_hp)

        # Heroes on the Right
        for i, hero in enumerate(party):
            hx, hy = 600, 150 + (i * 100)
            color = (0, 100, 255)
            if combat_manager.active_entity == hero:
                color = (255, 255, 255) # Highlight active hero
                
            pygame.draw.rect(self.screen, color, (hx - 20, hy - 20, 40, 40))
            self.draw_text(hero.name, hx, hy - 40)
            
            # ATB Meter next to hero
            atb_pc = combat_manager.get_atb_percentage(hero)
            self.draw_circular_meter(hx + 50, hy, 15, atb_pc)
            
            # HP Bar
            self.draw_hp_bar(hx - 30, hy + 30, 60, 8, hero.hp, hero.max_hp)
            # Mana Bar
            self.draw_resource_bar(hx - 30, hy + 42, 60, 6, hero.mana, hero.max_mana, color=(0, 100, 255))

    def draw_hp_bar(self, x, y, w, h, current, maximum):
        self.draw_resource_bar(x, y, w, h, current, maximum, color=(0, 200, 0))

    def draw_resource_bar(self, x, y, w, h, current, maximum, color=(0, 200, 0)):
        pygame.draw.rect(self.screen, (50, 0, 0), (x, y, w, h))
        fill_w = int(w * (current / maximum)) if maximum > 0 else 0
        pygame.draw.rect(self.screen, color, (x, y, fill_w, h))

    def draw_action_menu(self, options, selected_index, title="Menu"):
        # Bottom menu box
        pygame.draw.rect(self.screen, (0, 0, 50), (50, 450, 700, 120))
        pygame.draw.rect(self.screen, (255, 255, 255), (50, 450, 700, 120), 2)
        
        # Exibe o título do menu (ex: "SELECIONE A MAGIA")
        self.draw_text(title.upper(), 400, 470, color=(0, 255, 255), size="small")

        for i, opt in enumerate(options):
            color = (255, 255, 0) if i == selected_index else (200, 200, 200)
            # Ajusta posição se houver muitos itens
            x_pos = 100 + (i * 150)
            if len(options) > 4:
                x_pos = 80 + (i * 120)
            self.draw_text(opt, x_pos, 520, color=color, size="medium")

    def draw_battle_log(self, log):
        """Draws the last 3 messages of the battle log."""
        if not log:
            return
        
        # Draw background for log (semi-transparent)
        log_surface = pygame.Surface((700, 80))
        log_surface.set_alpha(150)
        log_surface.fill((0, 0, 0))
        self.screen.blit(log_surface, (50, 20))
        
        # Last 3 messages
        messages = log[-3:]
        for i, msg in enumerate(messages):
            self.draw_text(msg, 400, 35 + (i * 20), color=(255, 255, 255), size="small")

    def draw_text(self, text, x, y, color=(255, 255, 255), size="small"):
        font = self.font_medium if size == "medium" else self.font_small
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(x, y))
        self.screen.blit(surf, rect)
