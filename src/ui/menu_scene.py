import pygame
from src.ui.scenes import Scene
from src.models.skills import ABILITY_DATA
from src.models.items import EQUIPMENT_DATA
from src.models.interaction import SelectionManager

class MenuScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.context = manager.context
        self.player = self.context.player
        
        # Gerenciamento de Abas
        self.tabs = ["STATUS", "INVENTÁRIO"]
        self.tab_selector = SelectionManager(self.tabs)
        
        # Gerenciamento de Itens no Inventário
        self.inventory_selector = SelectionManager()
        self._refresh_inventory_list()
        
        # Feedback visual
        self.message = ""
        
        # Estado: TABS ou INVENTORY_NAV
        self.focus = "TABS"

    def _refresh_inventory_list(self):
        # Filtra apenas nomes de itens que o herói realmente tem
        self.inventory_selector.set_options(self.player.inventory.items)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Sair
            if event.key in [pygame.K_ESCAPE, pygame.K_m, pygame.K_TAB]:
                self.manager.pop()
                return

            if self.focus == "TABS":
                if event.key == pygame.K_LEFT: self.tab_selector.prev()
                elif event.key == pygame.K_RIGHT: self.tab_selector.next()
                elif event.key in [pygame.K_DOWN, pygame.K_SPACE, pygame.K_RETURN]:
                    if self.tab_selector.current_item == "INVENTÁRIO" and self.player.inventory.items:
                        self.focus = "INVENTORY_NAV"
            
            elif self.focus == "INVENTORY_NAV":
                if event.key == pygame.K_UP: self.inventory_selector.prev()
                elif event.key == pygame.K_DOWN: self.inventory_selector.next()
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_LEFT:
                    self.focus = "TABS"
                elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    # Tenta usar ou equipar o item
                    item_name = self.inventory_selector.current_item
                    success, result_msg = self.player.use_item(item_name)
                    self.message = result_msg
                    if success:
                        self._refresh_inventory_list()
                        # Se o inventário ficou vazio, volta o foco para abas
                        if not self.player.inventory.items:
                            self.focus = "TABS"

    def update(self, dt):
        pass

    def draw(self, screen):
        # Background
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(230)
        overlay.fill((10, 10, 30))
        screen.blit(overlay, (0, 0))

        # Border
        pygame.draw.rect(screen, (200, 200, 200), (40, 40, 720, 520), 2)
        
        # Título e Abas
        for i, tab in enumerate(self.tabs):
            color = (255, 215, 0) if i == self.tab_selector.index else (100, 100, 100)
            if self.focus == "TABS" and i == self.tab_selector.index:
                pygame.draw.rect(screen, color, (100 + i*200, 70, 180, 40), 2)
            self._draw_text(screen, tab, 190 + i*200, 90, size=24, color=color)

        pygame.draw.line(screen, (100, 100, 100), (60, 120), (740, 120), 1)

        if self.tab_selector.current_item == "STATUS":
            self._draw_status_tab(screen)
        else:
            self._draw_inventory_tab(screen)

        # Mensagem de Feedback
        if self.message:
            self._draw_text(screen, self.message, 400, 500, size=20, color=(0, 255, 0))

        # Instruções
        instr = "SETAS: Navegar | ESPAÇO: Selecionar | ESC: Sair"
        self._draw_text(screen, instr, 400, 545, size=16, color=(150, 150, 150), align="center")

    def _draw_status_tab(self, screen):
        col1_x, col2_x, col3_x = 70, 310, 540
        # Reutilizando lógica anterior para STATUS...
        self._draw_text(screen, "ATRIBUTOS", col1_x, 150, color=(0, 255, 255), align="left", size=22)
        attr_y = 190
        for label, val in [("Força", self.player.get_attribute('forca')), 
                          ("Agilidade", self.player.get_attribute('agilidade')), 
                          ("Inteligência", self.player.get_attribute('inteligencia')),
                          ("Ouro", f"{self.player.gold} G")]:
            self._draw_text(screen, f"{label}:", col1_x, attr_y, size=18, color=(180, 180, 180), align="left")
            self._draw_text(screen, str(val), col1_x + 130, attr_y, size=18, align="left")
            attr_y += 30
        
        # Equipamento atual
        self._draw_text(screen, "EQUIPADO", col2_x, 150, color=(0, 255, 255), align="left", size=22)
        eq_y = 190
        for label, slot in [("Arma", "weapon"), ("Escudo", "shield"), ("Peitoral", "armor"), ("Acessório", "accessory")]:
            item = self.player.equipment.get(slot)
            name = item.name if item else "---"
            self._draw_text(screen, f"{label}:", col2_x, eq_y, size=18, color=(180, 180, 180), align="left")
            self._draw_text(screen, name, col2_x, eq_y + 20, size=16, color=(220, 220, 220), align="left")
            eq_y += 50

        # Habilidades
        self._draw_text(screen, "HABILIDADES", col3_x, 150, color=(0, 255, 255), align="left", size=22)
        abi_y = 190
        current_int = self.player.get_attribute('inteligencia')
        for name, ability in list(ABILITY_DATA.items())[:6]:
            is_learned = name in self.player.skills
            meets_req = current_int >= ability.int_req
            color = (0, 255, 0) if is_learned and meets_req else (255, 50, 50) if is_learned else (120, 120, 120)
            self._draw_text(screen, name, col3_x, abi_y, size=17, color=color, align="left")
            abi_y += 30

    def _draw_inventory_tab(self, screen):
        self._draw_text(screen, "MOCHILA (ITENS DISPONÍVEIS)", 70, 150, color=(0, 255, 255), align="left", size=22)
        
        if not self.player.inventory.items:
            self._draw_text(screen, "Sua mochila está vazia.", 400, 300, size=24, color=(150, 150, 150))
            return

        # Divisão: Lista (Esquerda) | Info (Direita)
        y_item = 190
        for i, item_name in enumerate(self.player.inventory.items):
            color = (255, 255, 0) if i == self.inventory_selector.index and self.focus == "INVENTORY_NAV" else (255, 255, 255)
            prefix = "> " if i == self.inventory_selector.index and self.focus == "INVENTORY_NAV" else "  "
            self._draw_text(screen, f"{prefix}{item_name}", 100, y_item, size=20, color=color, align="left")
            y_item += 35

        # Painel de Informações (Direita)
        selected_name = self.inventory_selector.current_item
        if selected_name:
            from src.models.items import CONSUMABLE_DATA, EQUIPMENT_DATA
            item = CONSUMABLE_DATA.get(selected_name) or EQUIPMENT_DATA.get(selected_name)
            if item:
                panel_x = 420
                pygame.draw.rect(screen, (30, 30, 50), (panel_x, 150, 320, 300))
                pygame.draw.rect(screen, (100, 100, 120), (panel_x, 150, 320, 300), 1)
                
                self._draw_text(screen, item.name.upper(), panel_x + 160, 180, size=20, color=(255, 215, 0))
                self._draw_text(screen, f"Tipo: {item.category}", panel_x + 10, 210, size=16, align="left", color=(180, 180, 180))
                
                # Descrição (Quebra de linha simples se necessário)
                desc_lines = item.description.split('\n')
                for j, line in enumerate(desc_lines):
                    self._draw_text(screen, line, panel_x + 10, 240 + j*20, size=16, align="left")
                
                # Stats / Efeitos
                if hasattr(item, 'bonuses') and item.bonuses:
                    self._draw_text(screen, "Bônus:", panel_x + 10, 290, size=16, align="left", color=(0, 255, 255))
                    for k, (stat, val) in enumerate(item.bonuses.items()):
                        self._draw_text(screen, f"+{val} {stat.capitalize()}", panel_x + 20, 310 + k*20, size=14, align="left")
                
                if hasattr(item, 'effect') and item.effect:
                    self._draw_text(screen, "Efeitos:", panel_x + 10, 290, size=16, align="left", color=(0, 255, 0))
                    for k, (eff, val) in enumerate(item.effect.items()):
                        self._draw_text(screen, f"{val} {eff.upper()}", panel_x + 20, 310 + k*20, size=14, align="left")
