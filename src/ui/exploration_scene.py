import pygame
import os
import time
from src.ui.scenes import Scene
from src.models.interaction import InteractionManager, TransitionRequest

class ExplorationScene(Scene):
    def __init__(self, manager, map_path=None, spawn_tag=None):
        self.manager = manager
        self.context = manager.context
        self.map_path = map_path
        self.spawn_tag = spawn_tag
        self.player_speed = 4
        
        # Fade management
        self.fade_alpha = 0
        self.fade_target = 0
        self.fade_speed = 510 # Alpha per second
        self.pending_transition = None

        self.interaction_manager = InteractionManager(self.context, self.manager)
        from src.ui.interaction_renderer import InteractionRenderer
        self.interaction_renderer = InteractionRenderer()
        
        if map_path and self.context.orchestrator:
            print(f"Loading map: {map_path}")
            self.context.world = self.context.orchestrator.load_map(map_path)
            
            # Position player at spawn tag if provided
            if spawn_tag:
                tx, ty = self.context.orchestrator.get_tag_position(spawn_tag)
                if tx is not None:
                    self.context.player.position.x = tx * self.context.world.tile_size + self.context.world.tile_size // 2
                    self.context.player.position.y = ty * self.context.world.tile_size + self.context.world.tile_size // 2

    def handle_event(self, event):
        if self.fade_alpha > 0:
            return

        if self.interaction_manager.is_active:
            self.interaction_manager.handle_event(event)
            return

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_SPACE, pygame.K_e]:
                self.interaction_manager.interact()
            elif event.key == pygame.K_F5:
                # Quick Save
                if self.context.save_manager:
                    self.context.save_manager.save_game(self.context)
                    print("Jogo Salvo!")
            elif event.key == pygame.K_F9:
                # Quick Load
                if self.context.save_manager:
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
        # Update Notifications
        nm = getattr(self.context, "notification_manager", None)
        if nm:
            nm.update(dt)

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
            # Update AI Reasoning
            orchestrator = getattr(self.context, "orchestrator", None)
            if orchestrator:
                orchestrator.update_ai(self.context.world, dt)

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

        # Load map and replace world in context
        new_world = orchestrator.load_map(f"data/maps/{req.target_map}")
        if new_world:
            self.context.world = new_world
            
            # Position player
            if req.target_tag:
                tx, ty = orchestrator.get_tag_position(req.target_tag)
                if tx is not None:
                    self.context.player.position.x = tx * new_world.tile_size + new_world.tile_size // 2
                    self.context.player.position.y = ty * new_world.tile_size + new_world.tile_size // 2
            
            # Auto-save
            if self.context.save_manager:
                self.context.save_manager.save_game(self.context)
        
        # Start fading in
        self.fade_target = 0
        self.pending_transition = None

    def trigger_transition(self, request):
        """Starts the fade out sequence before map transition."""
        self.pending_transition = request
        self.fade_target = 255

    def draw(self, screen):
        # Draw Map/World
        self._draw_world(screen)
        
        # Draw Interactions (Dialogues, etc.)
        self.interaction_renderer.screen = screen
        self.interaction_renderer.render(self.interaction_manager.get_view_model())
        
        # Draw Notifications
        nm = getattr(self.context, "notification_manager", None)
        if nm:
            nm.draw(screen)
            
        # Draw Fade Overlay
        if self.fade_alpha > 0:
            overlay = pygame.Surface(screen.get_size())
            overlay.set_alpha(self.fade_alpha)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

    def _draw_world(self, screen):
        tile_size = self.context.world.tile_size
        
        # Optimization: only draw what's on screen
        for y, row in enumerate(self.context.world.grid):
            for x, tile in enumerate(row):
                color = (30, 30, 30) if tile == 1 else (60, 60, 60)
                pygame.draw.rect(screen, color, (x*tile_size, y*tile_size, tile_size, tile_size))
                pygame.draw.rect(screen, (40, 40, 40), (x*tile_size, y*tile_size, tile_size, tile_size), 1)

        # Draw Interactables
        for (tx, ty), obj in self.context.world.interactables.items():
            obj.draw(screen, self.context, (tx * tile_size, ty * tile_size))

        # Draw Player
        self.context.player.draw(screen, (self.context.player.position.x, self.context.player.position.y))

    def _check_on_step_triggers(self):
        """Checks for non-interactive triggers like portals under player's feet."""
        tx = int(self.context.player.position.x // self.context.world.tile_size)
        ty = int(self.context.player.position.y // self.context.world.tile_size)
        
        obj = self.context.world.get_interactable_at(tx, ty)
        if obj and hasattr(obj, "require_interaction") and not obj.require_interaction:
            # Trigger portal directly
            req = obj.on_interact(self.context)
            if isinstance(req, TransitionRequest):
                self.trigger_transition(req)
