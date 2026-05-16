import pygame
from src.ui.scenes import Scene
from src.models.interaction import SelectionManager
from src.core.juice import JuiceService
from src.core.particles import ParticleManager

class GameOverScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.context = manager.context
        self.options = ["Tentar Novamente", "Menu Principal"]
        self.selector = SelectionManager(self.options)
        self.particles = ParticleManager()
        self.juice = JuiceService(self.particles, settings_manager=self.context.settings)
        
        # Polish
        self.fade_alpha = 0
        self.fade_target = 0
        self.fade_speed = 400
        self.juice.shake(0.8) # Shake on entry
        
        # Track transition
        self.pending_action = None

    def handle_event(self, event):
        if self.fade_alpha > 0 and self.fade_target == 255:
            return

        if event.type == pygame.KEYDOWN:
            inputs = self.context.inputs
            if inputs.is_action_just_pressed(inputs.InputAction.UP, event):
                self.selector.prev()
            elif inputs.is_action_just_pressed(inputs.InputAction.DOWN, event):
                self.selector.next()
            elif inputs.is_action_just_pressed(inputs.InputAction.CONFIRM, event):
                self._confirm_selection()

    def _confirm_selection(self):
        selection = self.selector.current_item
        if selection == "Tentar Novamente":
            self.pending_action = "RETRY"
        elif selection == "Menu Principal":
            self.pending_action = "TITLE"
        
        self.fade_target = 255

    def update(self, dt):
        self.juice.update(dt)
        self.particles.update(dt)
        
        # Update Fade
        if self.fade_alpha != self.fade_target:
            step = self.fade_speed * dt
            if self.fade_alpha < self.fade_target:
                self.fade_alpha = min(self.fade_target, self.fade_alpha + step)
            else:
                self.fade_alpha = max(self.fade_target, self.fade_alpha - step)

        if self.fade_alpha == 255 and self.pending_action:
            self._execute_pending_action()

    def _execute_pending_action(self):
        if self.pending_action == "RETRY":
            self._retry_game()
        elif self.pending_action == "TITLE":
            from src.ui.title_scene import TitleScene
            self.manager.change_scene(TitleScene(self.manager))
        
        self.pending_action = None

    def _retry_game(self):
        # Try to load last save
        if self.context.save_manager:
            # We don't know which slot was the last one, 
            # but usually slot 0 is the quicksave/auto-save slot.
            # TitleScene has more complex logic for slot selection, 
            # here we'll try slot 0 first.
            save_data = self.context.save_manager.load_game(0)
            if save_data:
                # Reuse TitleScene's loading logic would be better, 
                # but for simplicity we'll do it here or refactor.
                # Actually, TitleScene is a separate scene.
                # Let's use a trick: go back to Title and trigger load if we wanted perfect reuse,
                # but it's better to have a central Load utility.
                
                # For now, let's just use TitleScene's _load_game logic manually
                # or better: instantiate TitleScene and call its _load_game.
                from src.ui.title_scene import TitleScene
                ts = TitleScene(self.manager)
                ts._load_game(0)
                return

        # Fallback: start new game if no save found
        from src.ui.title_scene import TitleScene
        ts = TitleScene(self.manager)
        ts._start_new_game()

    def draw(self, screen):
        # Apply camera shake
        shake_x, shake_y = self.juice.camera_offset
        
        # Background
        screen.fill((20, 0, 0)) # Dark red tint
        
        content_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        
        self._draw_text(content_surf, "FIM DE JOGO", 400, 200, size=72, color=(255, 50, 50))
        
        for i, opt in enumerate(self.options):
            color = (255, 255, 255) if i == self.selector.index else (100, 100, 100)
            prefix = "> " if i == self.selector.index else "  "
            self._draw_text(content_surf, f"{prefix}{opt}", 400, 350 + i*50, size=32, color=color)
            
        self.particles.draw(content_surf)
        screen.blit(content_surf, (int(shake_x), int(shake_y)))
        
        # Fade Overlay
        if self.fade_alpha > 0:
            overlay = pygame.Surface(screen.get_size())
            overlay.set_alpha(self.fade_alpha)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
