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
                    # Tenta equipar o item
                    item_name = self.inventory_selector.current_item
                    if item_name in EQUIPMENT_DATA:
                        item = EQUIPMENT_DATA[item_name]
                        success, result = self.player.equip_item(item)
                        if success:
                            # Se equipou, removemos do inventário e talvez devolvemos o antigo
                            self.player.inventory.remove_item(item_name)
                            if result: # old_item
                                self.player.inventory.add_item(result.name)
                            self._refresh_inventory_list()
                            print(f"Equipou {item_name}")
                        else:
                            print(f"Falha ao equipar: {result}")

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

        y_item = 190
        for i, item_name in enumerate(self.player.inventory.items):
            color = (255, 255, 0) if i == self.inventory_selector.index and self.focus == "INVENTORY_NAV" else (255, 255, 255)
            prefix = "> " if i == self.inventory_selector.index and self.focus == "INVENTORY_NAV" else "  "
            
            # Info extra do item se selecionado
            if i == self.inventory_selector.index and self.focus == "INVENTORY_NAV":
                if item_name in EQUIPMENT_DATA:
                    eq = EQUIPMENT_DATA[item_name]
                    self._draw_text(screen, f"Tipo: {eq.slot.capitalize()} | Bônus: {eq.bonuses}", 400, 500, size=18, color=(0, 255, 0))

            self._draw_text(screen, f"{prefix}{item_name}", 100, y_item, size=20, color=color, align="left")
            y_item += 35
