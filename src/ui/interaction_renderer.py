import pygame

class InteractionRenderer:
    """Renderer especializado para a camada de visão de interações."""
    def __init__(self, screen=None):
        self.screen = screen
        # Fallback para fontes se não inicializadas (geralmente via pygame.font.init())
        self.font_name = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_text = pygame.font.SysFont("Arial", 18)
        self.font_choice = pygame.font.SysFont("Arial", 18)

    def render(self, view_model):
        """Desenha o estado da interação na tela baseado no DTO (view_model)."""
        if not view_model:
            return

        # Dialogue Box (Centralizada na parte inferior)
        pygame.draw.rect(self.screen, (0, 0, 0), (50, 400, 700, 150))
        pygame.draw.rect(self.screen, (255, 255, 255), (50, 400, 700, 150), 2)
        
        # Speaker
        speaker_surf = self.font_name.render(view_model['speaker'] + ":", True, (200, 200, 50))
        self.screen.blit(speaker_surf, (70, 415))
        
        # Texto principal (com suporte a quebra de linha manual)
        text_lines = view_model['text'].split("\n")
        for i, line in enumerate(text_lines):
            text_surf = self.font_text.render(line, True, (255, 255, 255))
            self.screen.blit(text_surf, (70, 445 + (i * 25)))
        
        # Opções de escolha
        choices = view_model['choices']
        if choices:
            for i, choice_text in enumerate(choices):
                is_selected = i == view_model['selected_index']
                color = (255, 255, 0) if is_selected else (200, 200, 200)
                
                # Desloca choices para baixo dinamicamente baseado nas linhas de texto
                y_pos = 480 + (len(text_lines)-1)*20 + (i * 25)
                
                prefix = "> " if is_selected else "  "
                choice_surf = self.font_choice.render(f"{prefix}{choice_text}", True, color)
                self.screen.blit(choice_surf, (100, y_pos))
