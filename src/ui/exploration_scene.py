import pygame
from src.ui.scenes import Scene
from src.models.interaction import InteractionManager
from src.ui.interaction_renderer import InteractionRenderer

class ExplorationScene(Scene):
    def __init__(self, manager, npc, enemy_pos):
        self.manager = manager
        self.context = manager.context
        self.npc = npc
        self.enemy_pos = enemy_pos
        self.interaction_manager = InteractionManager(self.context, self.manager)
        self.interaction_renderer = InteractionRenderer()
        self.player_speed = 4

    def handle_event(self, event):
        # Only process events if this is the active scene
        if self.manager.active_scene != self:
            return

        if event.type == pygame.KEYDOWN:
            if self.interaction_manager.is_active:
                if event.key == pygame.K_UP: self.interaction_manager.process_command("up")
                elif event.key == pygame.K_DOWN: self.interaction_manager.process_command("down")
                elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    self.interaction_manager.process_command("confirm")
            else:
                if event.key in [pygame.K_e, pygame.K_SPACE]:
                    self.interaction_manager.interact()
                
                # Save/Load/Rest
                if event.key == pygame.K_k: # K for Keep (Save)
                    if self.context.save_manager.save_game(self.context):
                        print("Jogo Salvo com Sucesso!")
                
                elif event.key == pygame.K_r: # R for Rest
                    self.context.player.rest()
                    print("Você descansou. HP, Mana e Energia restaurados!")

                elif event.key == pygame.K_l: # L for Load
                    save_data = self.context.save_manager.load_game()
                    if save_data:
                        self.context.player.position.x = save_data['position']['x']
                        self.context.player.position.y = save_data['position']['y']
                        self.context.player.hp = save_data['hp']
                        self.context.player.xp = save_data['xp']
                        self.context.player.energy = save_data.get('energy', 3)
                        self.context.player.skills = set(save_data.get('skills', []))
                        
                        if 'global_state' in save_data:
                            from src.core.state import GlobalState
                            self.context.global_state = GlobalState.from_dict(save_data['global_state'])
                        elif 'opened_chests' in save_data: # Migração legada
                            for cid in save_data['opened_chests']:
                                self.context.global_state.set_entity_delta(cid, {"_is_open": True})

                        print("Jogo Carregado!")
                elif event.key in [pygame.K_m, pygame.K_TAB]:
                    from src.ui.menu_scene import MenuScene
                    self.manager.push(MenuScene(self.manager))

    def update(self, dt):
        # Only process movement if this is the active scene
        if self.manager.active_scene != self:
            return

        if not self.interaction_manager.is_active:
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -self.player_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = self.player_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -self.player_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = self.player_speed
            
            if dx != 0 or dy != 0:
                if self.context.world.can_move_to(self.context.player, self.context.player.position.x + dx, self.context.player.position.y + dy):
                    self.context.player.position.move(dx, dy)
                    self.context.player.update_orientation(dx, dy)

    def draw(self, screen):
        # Draw Map
        for y, row in enumerate(self.context.world.grid):
            for x, tile in enumerate(row):
                if tile == 1: pygame.draw.rect(screen, (100, 100, 100), (x*32, y*32, 32, 32))
                else: pygame.draw.rect(screen, (50, 50, 50), (x*32, y*32, 32, 32), 1)
        
        # Draw all interactables in the world (polymorphic drawing)
        for (tx, ty), obj in self.context.world.interactables.items():
            x_pos, y_pos = tx * 32, ty * 32
            obj.draw(screen, self.context, (x_pos, y_pos))

        # Player (Blue Square)
        px, py = self.context.player.position.x, self.context.player.position.y
        pygame.draw.rect(screen, (0, 100, 255), (px - 16, py - 16, 32, 32))
        
        # Direction Indicator (Small yellow dot/line)
        indicator_color = (255, 255, 0)
        if self.context.player.facing_direction == "N":
            pygame.draw.rect(screen, indicator_color, (px - 4, py - 16, 8, 4))
        elif self.context.player.facing_direction == "S":
            pygame.draw.rect(screen, indicator_color, (px - 4, py + 12, 8, 4))
        elif self.context.player.facing_direction == "W":
            pygame.draw.rect(screen, indicator_color, (px - 16, py - 4, 4, 8))
        elif self.context.player.facing_direction == "E":
            pygame.draw.rect(screen, indicator_color, (px + 12, py - 4, 4, 8))
        
        # Draw Interaction Overlay (Delegated)
        if self.interaction_manager.is_active:
            self.interaction_renderer.screen = screen
            vm = self.interaction_manager.get_view_model()
            self.interaction_renderer.render(vm)

        # UI Overlay (Energy)
        self._draw_text(screen, f"Energia: {self.context.player.energy}/3", 20, 20, size=20, color=(255, 255, 0), align="left")
