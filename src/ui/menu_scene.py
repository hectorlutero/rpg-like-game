import pygame
from src.ui.scenes import Scene
from src.models.skills import ABILITY_DATA

class MenuScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.context = manager.context
        self.player = self.context.player

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Sair do menu ao apertar ESC ou M novamente
            if event.key in [pygame.K_ESCAPE, pygame.K_m, pygame.K_TAB]:
                self.manager.pop()

    def update(self, dt):
        pass

    def draw(self, screen):
        # Escurecer o fundo (efeito de sobreposição)
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Moldura do Menu
        pygame.draw.rect(screen, (255, 255, 255), (50, 50, 700, 500), 2)
        
        # Título
        self._draw_text(screen, "STATUS DO PERSONAGEM", 400, 80, size=30, color=(255, 255, 0))

        # --- Coluna Esquerda: Atributos ---
        self._draw_text(screen, f"Nome: {self.player.name}", 100, 150, align="left")
        self._draw_text(screen, f"Classe: {self.player.character_class.__class__.__name__}", 100, 180, align="left")
        self._draw_text(screen, f"Nível: {self.player.level}", 100, 210, align="left")
        self._draw_text(screen, f"XP: {self.player.xp}", 100, 240, align="left")
        
        self._draw_text(screen, "ATRIBUTOS ATUAIS", 100, 300, color=(0, 255, 255), align="left")
        self._draw_text(screen, f"Força: {self.player.get_attribute('forca')}", 100, 330, align="left")
        self._draw_text(screen, f"Agilidade: {self.player.get_attribute('agilidade')}", 100, 360, align="left")
        self._draw_text(screen, f"Inteligência: {self.player.get_attribute('inteligencia')}", 100, 390, align="left")
        
        self._draw_text(screen, f"HP: {self.player.hp}/{self.player.max_hp}", 100, 440, align="left")
        self._draw_text(screen, f"Mana: {self.player.mana}/{self.player.max_mana}", 100, 470, align="left")
        self._draw_text(screen, f"Energia: {self.player.energy}/3", 100, 500, align="left")

        # --- Coluna Direita: Abilities ---
        self._draw_text(screen, "HABILIDADES & MAGIAS", 430, 150, color=(0, 255, 255), align="left")
        
        y_offset = 190
        current_int = self.player.get_attribute('inteligencia')
        for name, ability in ABILITY_DATA.items():
            is_learned = name in self.player.skills
            meets_req = current_int >= ability.int_req
            
            type_tag = "[Skill]" if ability.category == "Skill" else "[Magia]"
            
            if is_learned:
                if meets_req:
                    color = (0, 255, 0)
                    status_text = "[ATIVA]"
                else:
                    color = (255, 50, 50) # Vermelho se perdeu o requisito
                    status_text = "[BLOQUEADA]"
            else:
                color = (150, 150, 150)
                status_text = f"[REQUER INT {ability.int_req}]"
            
            self._draw_text(screen, f"{type_tag} {name}:", 430, y_offset, color=color, align="left", size=18)
            self._draw_text(screen, status_text, 640, y_offset, color=color, align="left", size=16)
            y_offset += 30

        self._draw_text(screen, "Pressione ESC ou M para fechar", 400, 530, size=18)

    def _draw_text(self, screen, text, x, y, size=24, color=(255, 255, 255), align="center"):
        font = pygame.font.SysFont("Arial", size)
        surf = font.render(text, True, color)
        rect = surf.get_rect()
        if align == "center": rect.center = (x, y)
        else: rect.topleft = (x, y)
        screen.blit(surf, rect)
