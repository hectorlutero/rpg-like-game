import pygame
from src.ui.scenes import Scene

class CreditsScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.context = manager.context
        
        self.credits = [
            {"text": "RPG CLASSIC", "size": 64, "color": (255, 215, 0)},
            {"text": "", "size": 32},
            {"text": "Um jogo criado por", "size": 24, "color": (200, 200, 200)},
            {"text": "HECTOR SIMAN (LUTERO)", "size": 32, "color": (255, 255, 255)},
            {"text": "", "size": 32},
            {"text": "EQUIPE DE DESENVOLVIMENTO", "size": 24, "color": (200, 200, 200)},
            {"text": "Design & Programação: Lutero", "size": 24},
            {"text": "IA & Sistemas: Gemini CLI", "size": 24},
            {"text": "", "size": 32},
            {"text": "AGRADECIMENTOS ESPECIAIS", "size": 24, "color": (200, 200, 200)},
            {"text": "Kauã (Sr. Lutero)", "size": 24},
            {"text": "Comunidade de RPG", "size": 24},
            {"text": "", "size": 32},
            {"text": "OBRIGADO POR JOGAR!", "size": 48, "color": (255, 215, 0)},
        ]
        
        self.scroll_y = 600 # Start from bottom
        self.scroll_speed = 60 # Pixels per second
        self.total_height = 0
        
        # Calculate total height
        for item in self.credits:
            self.total_height += item["size"] + 10
        
        # Fade management
        self.fade_alpha = 255 # Start faded in
        self.fade_target = 0
        self.fade_speed = 300
        self.exiting = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            inputs = self.context.inputs
            if inputs.is_action_just_pressed(inputs.InputAction.CANCEL, event) or \
               inputs.is_action_just_pressed(inputs.InputAction.CONFIRM, event):
                self._exit_credits()

    def _exit_credits(self):
        self.exiting = True
        self.fade_target = 255

    def update(self, dt):
        # Update Fade
        if self.fade_alpha != self.fade_target:
            step = self.fade_speed * dt
            if self.fade_alpha < self.fade_target:
                self.fade_alpha = min(self.fade_target, self.fade_alpha + step)
            else:
                self.fade_alpha = max(self.fade_target, self.fade_alpha - step)
        
        if self.exiting and self.fade_alpha == 255:
            from src.ui.title_scene import TitleScene
            self.manager.change_scene(TitleScene(self.manager))
            return

        # Update Scroll
        if not self.exiting:
            self.scroll_y -= self.scroll_speed * dt
            
            # Check if finished
            if self.scroll_y < -self.total_height:
                self._exit_credits()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        # Optional: draw background images/particles here
        
        # Draw Credits
        current_y = self.scroll_y
        for item in self.credits:
            text = item["text"]
            size = item["size"]
            color = item.get("color", (255, 255, 255))
            
            # Only draw if on screen
            if -size < current_y < 600 + size:
                self._draw_text(screen, text, 400, int(current_y), size=size, color=color)
            
            current_y += size + 10

        # Fade Overlay
        if self.fade_alpha > 0:
            overlay = pygame.Surface(screen.get_size())
            overlay.set_alpha(self.fade_alpha)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
