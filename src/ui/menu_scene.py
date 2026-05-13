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
        self.tabs = ["STATUS", "INVENTÁRIO", "MISSÕES"]
        self.tab_selector = SelectionManager(self.tabs)
        
        # Gerenciamento de Itens no Inventário
        self.inventory_selector = SelectionManager()
        self._refresh_inventory_list()
        
        # Gerenciamento de Missões
        self.quest_selector = SelectionManager()
        self._refresh_quest_list()
        
        # Feedback visual
        self.message = ""
        
        # Estado: TABS, INVENTORY_NAV, QUEST_NAV
        self.focus = "TABS"

    def _refresh_inventory_list(self):
        # Filtra apenas nomes de itens que o herói realmente tem
        self.inventory_selector.set_options(self.player.inventory.items)

    def _refresh_quest_list(self):
        # Pega as missões em progresso
        if hasattr(self.context, "quest_manager") and self.context.quest_manager:
            active_quests = self.context.quest_manager.get_active_quests()
            self.quest_selector.set_options(active_quests)
        else:
            self.quest_selector.set_options([])

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
                    elif self.tab_selector.current_item == "MISSÕES" and self.quest_selector.options:
                        self.focus = "QUEST_NAV"
            
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

            elif self.focus == "QUEST_NAV":
                if event.key == pygame.K_UP: self.quest_selector.prev()
                elif event.key == pygame.K_DOWN: self.quest_selector.next()
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_LEFT:
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
        elif self.tab_selector.current_item == "INVENTÁRIO":
            self._draw_inventory_tab(screen)
        else:
            self._draw_quests_tab(screen)

        # Mensagem de Feedback
        if self.message:
            self._draw_text(screen, self.message, 400, 500, size=20, color=(0, 255, 0))

        # Instruções
        instr = "SETAS: Navegar | ESPAÇO: Selecionar | ESC: Sair"
        self._draw_text(screen, instr, 400, 545, size=16, color=(150, 150, 150), align="center")

    def _draw_status_tab(self, screen):
        col1_x, col2_x, col3_x = 70, 310, 540
        
        # Vida e Mana (Barras horizontais)
        self._draw_text(screen, "VITALIDADE", col1_x, 140, color=(0, 255, 255), align="left", size=20)
        
        # Barra de Vida
        hp_y = 170
        pygame.draw.rect(screen, (50, 0, 0), (col1_x, hp_y, 180, 15))
        hp_ratio = self.player.hp / self.player.max_hp if self.player.max_hp > 0 else 0
        pygame.draw.rect(screen, (0, 200, 0), (col1_x, hp_y, int(180 * hp_ratio), 15))
        self._draw_text(screen, f"HP: {self.player.hp}/{self.player.max_hp}", col1_x + 90, hp_y + 7, size=14, align="center")
        
        # Barra de Mana
        mana_y = 190
        pygame.draw.rect(screen, (0, 0, 50), (col1_x, mana_y, 180, 15))
        mana_ratio = self.player.mana / self.player.max_mana if self.player.max_mana > 0 else 0
        pygame.draw.rect(screen, (0, 100, 255), (col1_x, mana_y, int(180 * mana_ratio), 15))
        self._draw_text(screen, f"MP: {self.player.mana}/{self.player.max_mana}", col1_x + 90, mana_y + 7, size=14, align="center")

        # Reutilizando lógica anterior para STATUS...
        self._draw_text(screen, "ATRIBUTOS", col1_x, 230, color=(0, 255, 255), align="left", size=20)
        attr_y = 260
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
        
        # Resumo de Vida/Mana no Inventário (Sidebar Direita, topo)
        res_x = 420
        self._draw_text(screen, f"Sua Vida: {self.player.hp}/{self.player.max_hp}", res_x, 110, size=16, color=(0, 255, 0), align="left")
        self._draw_text(screen, f"Sua Mana: {self.player.mana}/{self.player.max_mana}", res_x + 160, 110, size=16, color=(0, 100, 255), align="left")

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

    def _draw_quests_tab(self, screen):
        self._draw_text(screen, "DIÁRIO DE AVENTURAS", 70, 150, color=(0, 255, 255), align="left", size=22)
        
        active_quests = self.quest_selector.options
        if not active_quests:
            self._draw_text(screen, "Você não tem missões ativas.", 400, 300, size=24, color=(150, 150, 150))
            return

        # Divisão: Lista (Esquerda) | Info (Direita)
        y_item = 190
        for i, quest_id in enumerate(active_quests):
            quest_def = self.context.quest_manager.quests.get(quest_id, {})
            name = quest_def.get("name", quest_id)
            
            color = (255, 255, 0) if i == self.quest_selector.index and self.focus == "QUEST_NAV" else (255, 255, 255)
            prefix = "> " if i == self.quest_selector.index and self.focus == "QUEST_NAV" else "  "
            self._draw_text(screen, f"{prefix}{name}", 100, y_item, size=20, color=color, align="left")
            y_item += 35

        # Painel de Detalhes (Direita)
        selected_id = self.quest_selector.current_item
        if selected_id:
            quest_def = self.context.quest_manager.quests.get(selected_id, {})
            state = self.context.global_state.quests.get(selected_id, {})
            
            panel_x = 420
            pygame.draw.rect(screen, (30, 30, 50), (panel_x, 150, 320, 300))
            pygame.draw.rect(screen, (100, 100, 120), (panel_x, 150, 320, 300), 1)
            
            self._draw_text(screen, quest_def.get("name", "???").upper(), panel_x + 160, 180, size=20, color=(255, 215, 0))
            
            # Descrição Geral
            desc = quest_def.get("description", "")
            self._draw_text(screen, desc, panel_x + 10, 210, size=15, align="left", color=(180, 180, 180))
            
            # Objetivo Atual
            current_stage_idx = state.get("stage", 0)
            stages = quest_def.get("stages", [])
            if current_stage_idx < len(stages):
                stage_data = stages[current_stage_idx]
                self._draw_text(screen, "Objetivo Atual:", panel_x + 10, 260, size=17, align="left", color=(0, 255, 255))
                
                obj_desc = stage_data.get("description", "???")
                # Wrap text if too long (simplified)
                words = obj_desc.split(' ')
                lines = []
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) < 30:
                        current_line += word + " "
                    else:
                        lines.append(current_line)
                        current_line = word + " "
                lines.append(current_line)
                
                for k, line in enumerate(lines):
                    self._draw_text(screen, line, panel_x + 20, 290 + k*20, size=15, align="left")
            else:
                self._draw_text(screen, "Missão Concluída!", panel_x + 10, 260, size=17, align="left", color=(0, 255, 0))
