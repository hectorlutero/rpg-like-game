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
            if event.key in [pygame.K_ESCAPE, pygame.K_m, pygame.K_TAB]:
                self.manager.pop()

    def update(self, dt):
        pass

    def draw(self, screen):
        # Escurecer o fundo
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(220)
        overlay.fill((10, 10, 20))
        screen.blit(overlay, (0, 0))

        # Moldura principal
        pygame.draw.rect(screen, (200, 200, 200), (40, 40, 720, 520), 2)
        
        # Título centralizado
        self._draw_text(screen, "PAINEL DO HERÓI", 400, 75, size=32, color=(255, 215, 0))
        pygame.draw.line(screen, (100, 100, 100), (60, 110), (740, 110), 1)

        # --- Definição das Colunas (X) ---
        col1_x = 70
        col2_x = 310
        col3_x = 540

        # --- COLUNA 1: STATUS BÁSICOS ---
        self._draw_text(screen, "STATUS", col1_x, 140, color=(0, 255, 255), align="left", size=22)
        
        info_y = 180
        status_info = [
            (f"Nome:", self.player.name),
            (f"Classe:", self.player.character_class.__class__.__name__),
            (f"Nível:", str(self.player.level)),
            (f"XP:", str(self.player.xp)),
            (f"Ouro:", f"{self.player.gold} G", (255, 215, 0))
        ]
        
        for label, val, *color in status_info:
            c = color[0] if color else (255, 255, 255)
            self._draw_text(screen, label, col1_x, info_y, size=18, color=(180, 180, 180), align="left")
            self._draw_text(screen, val, col1_x + 80, info_y, size=18, color=c, align="left")
            info_y += 30

        # Atributos de Combate
        info_y += 20
        self._draw_text(screen, "ATRIBUTOS", col1_x, info_y, color=(0, 255, 255), align="left", size=22)
        info_y += 40
        
        attributes = [
            ("Força", self.player.get_attribute('forca')),
            ("Agilidade", self.player.get_attribute('agilidade')),
            ("Inteligência", self.player.get_attribute('inteligencia')),
            ("Defesa Abs.", self.player.defense_absolute),
            ("Defesa Rel.", f"{int(self.player.defense_relative * 100)}%")
        ]
        
        for attr, val in attributes:
            self._draw_text(screen, f"{attr}:", col1_x, info_y, size=18, color=(180, 180, 180), align="left")
            self._draw_text(screen, str(val), col1_x + 130, info_y, size=18, align="left")
            info_y += 25

        # Recursos
        info_y += 15
        self._draw_text(screen, f"HP: {self.player.hp}/{self.player.max_hp}", col1_x, info_y, size=18, color=(0, 255, 0), align="left")
        info_y += 25
        self._draw_text(screen, f"MP: {self.player.mana}/{self.player.max_mana}", col1_x, info_y, size=18, color=(80, 80, 255), align="left")
        info_y += 25
        self._draw_text(screen, f"Energia: {self.player.energy}/3", col1_x, info_y, size=18, color=(255, 255, 0), align="left")

        # --- COLUNA 2: EQUIPAMENTO ---
        self._draw_text(screen, "EQUIPAMENTO", col2_x, 140, color=(0, 255, 255), align="left", size=22)
        
        y_eq = 180
        slots = [
            ("Arma", "weapon"),
            ("Escudo", "shield"),
            ("Armadura", "armor"),
            ("Acessório", "accessory")
        ]
        
        for label, slot_key in slots:
            item = self.player.equipment.get(slot_key)
            item_name = item.name if item else "---"
            self._draw_text(screen, f"{label}:", col2_x, y_eq, size=18, color=(180, 180, 180), align="left")
            self._draw_text(screen, item_name, col2_x, y_eq + 20, size=16, color=(220, 220, 220), align="left")
            y_eq += 50

        # --- COLUNA 3: HABILIDADES ---
        self._draw_text(screen, "HABILIDADES", col3_x, 140, color=(0, 255, 255), align="left", size=22)
        
        y_abi = 180
        current_int = self.player.get_attribute('inteligencia')
        
        for name, ability in ABILITY_DATA.items():
            is_learned = name in self.player.skills
            meets_req = current_int >= ability.int_req
            
            type_tag = " [S]" if ability.category == "Skill" else " [M]"
            
            if is_learned:
                if meets_req:
                    color, status = (0, 255, 0), "Ativa"
                else:
                    color, status = (255, 50, 50), "Bloqueada"
            else:
                color, status = (120, 120, 120), f"Req. INT {ability.int_req}"
            
            self._draw_text(screen, f"{name}{type_tag}", col3_x, y_abi, size=17, color=color, align="left")
            self._draw_text(screen, status, col3_x, y_abi + 18, size=14, color=color, align="left")
            y_abi += 45

        # Instrução de saída
        self._draw_text(screen, "ESC/M - Voltar ao Jogo", 400, 540, size=16, color=(150, 150, 150))

    def _draw_text(self, screen, text, x, y, size=24, color=(255, 255, 255), align="center"):
        font = pygame.font.SysFont("Arial", size)
        surf = font.render(text, True, color)
        rect = surf.get_rect()
        if align == "center": rect.center = (x, y)
        else: rect.topleft = (x, y)
        screen.blit(surf, rect)
