import pygame
from src.ui.scenes import Scene
from src.models.interaction import InteractionManager, Portal, TransitionRequest
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
        self.is_transitioning = False
        self.fade_alpha = 0
        self.fade_target = 0
        self.fade_speed = 510 # Alpha per second (approx 0.5s for full fade)
        self.pending_transition = None

    def handle_event(self, event):
        # Only process events if this is the active scene and no fade is active
        if self.manager.active_scene != self or self.fade_alpha > 0:
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

        # Process any pending transition requests from interaction
        if self.interaction_manager.requested_transition:
            req = self.interaction_manager.requested_transition
            self.interaction_manager.requested_transition = None
            self.trigger_transition(req)

        # Update Fade Animation
        if self.fade_alpha != self.fade_target:
            step = self.fade_speed * dt
            if self.fade_alpha < self.fade_target:
                self.fade_alpha = min(self.fade_target, self.fade_alpha + step)
            else:
                self.fade_alpha = max(self.fade_target, self.fade_alpha - step)

        # Block everything else if fading
        if self.fade_alpha > 0:
            # Check if reached peak
            if self.fade_alpha == 255 and self.fade_target == 255:
                self._execute_transition()
            return

        if not self.interaction_manager.is_active:
            # Safety check for video system (important for headless tests or watch mode)
            if not pygame.display.get_init():
                return
                
            try:
                keys = pygame.key.get_pressed()
            except pygame.error:
                return # Skip input processing if system is not ready

            dx, dy = 0, 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -self.player_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = self.player_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -self.player_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = self.player_speed
            
            if dx != 0 or dy != 0:
                if self.context.world.can_move_to(self.context.player, self.context.player.position.x + dx, self.context.player.position.y + dy):
                    self.context.player.position.move(dx, dy)
                    self.context.player.update_orientation(dx, dy)
                    self._check_on_step_triggers()

    def _execute_transition(self):
        """Perform the actual map swap and auto-save at the peak of the fade."""
        req = self.pending_transition
        if not req:
            self.fade_target = 0
            return
            
        print(f"Executing transition to {req.target_map}...")
        
        orchestrator = self.context.orchestrator
        if not orchestrator:
            print("Error: No orchestrator found in context.")
            self.fade_target = 0
            self.pending_transition = None
            return

        # 1. Load the new map
        map_path = f"data/maps/{req.target_map}"
        new_world = orchestrator.load_map(map_path)
        
        if new_world:
            self.context.world = new_world
            
            # 2. Position the player using the target tag
            tx, ty = orchestrator.get_tag_position(req.target_tag)
            if tx is not None and ty is not None:
                self.context.player.position.x = tx * new_world.tile_size + new_world.tile_size // 2
                self.context.player.position.y = ty * new_world.tile_size + new_world.tile_size // 2
            else:
                print(f"Warning: Tag '{req.target_tag}' not found in {req.target_map}. Keeping current position.")

            # 3. Auto-save
            if self.context.save_manager:
                if self.context.save_manager.save_game(self.context):
                    print("Auto-save completed.")
        else:
            print(f"Error: Could not load map {map_path}")

        # 4. Trigger Fade In
        self.pending_transition = None
        self.fade_target = 0

    def _check_on_step_triggers(self):
        """Checks if the player stepped on an automatic trigger (like a Portal)."""
        world = self.context.world
        tx = int(self.context.player.position.x // world.tile_size)
        ty = int(self.context.player.position.y // world.tile_size)
        
        target = world.get_interactable_at(tx, ty)
        if isinstance(target, Portal) and not target.require_interaction:
            self.trigger_transition(target.on_interact(self.context))

    def trigger_transition(self, request):
        """Starts the transition process (Fade Out -> Swap -> Fade In)."""
        if not request: return
        print(f"Triggering transition to {request.target_map} at {request.target_tag}")
        self.fade_target = 255
        self.pending_transition = request

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

        # Draw Fade Overlay
        if self.fade_alpha > 0:
            fade_surf = pygame.Surface(screen.get_size())
            fade_surf.set_alpha(int(self.fade_alpha))
            fade_surf.fill((0, 0, 0))
            screen.blit(fade_surf, (0, 0))
