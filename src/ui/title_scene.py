import pygame
import sys
from src.ui.scenes import Scene
from src.models.interaction import SelectionManager
from src.ui.exploration_scene import ExplorationScene

class TitleScene(Scene):
    def __init__(self, manager):
        self.manager = manager
        self.context = manager.context
        self.options = ["Novo Jogo", "Carregar Jogo", "Opções", "Sair"]
        self.selector = SelectionManager(self.options)
        self.state = "MAIN" # MAIN, LOAD, OPTIONS
        
        # Load Menu
        self.save_slots = []
        self.load_selector = SelectionManager()
        
    def _refresh_load_menu(self):
        if self.context.save_manager:
            metadata = self.context.save_manager.get_slots_metadata()
            # Convert to a list of display strings
            self.save_slots = []
            options = []
            
            # Use slots 0 to 5 as defined in SaveManager
            for i in range(6):
                if i in metadata:
                    m = metadata[i]
                    # Format play time
                    pt = m.get('play_time', 0)
                    hours = int(pt // 3600)
                    minutes = int((pt % 3600) // 60)
                    time_str = f"{hours}h {minutes}m"
                    
                    display = f"Slot {i}: Nvl {m.get('level', 1)} - {m.get('location', '???')} ({time_str})"
                    self.save_slots.append(i)
                    options.append(display)
                else:
                    # Optional: show empty slots
                    # display = f"Slot {i}: --- Vazio ---"
                    # self.save_slots.append(None)
                    # options.append(display)
                    pass
            
            if not options:
                options = ["Nenhum jogo salvo"]
                self.save_slots = [None]
                
            self.load_selector.set_options(options)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            inputs = self.context.inputs
            
            if self.state == "MAIN":
                if inputs.is_action_just_pressed(inputs.InputAction.UP, event): self.selector.prev()
                elif inputs.is_action_just_pressed(inputs.InputAction.DOWN, event): self.selector.next()
                elif inputs.is_action_just_pressed(inputs.InputAction.CONFIRM, event):
                    self._handle_main_selection()
            
            elif self.state == "LOAD":
                if inputs.is_action_just_pressed(inputs.InputAction.UP, event): self.load_selector.prev()
                elif inputs.is_action_just_pressed(inputs.InputAction.DOWN, event): self.load_selector.next()
                elif inputs.is_action_just_pressed(inputs.InputAction.CANCEL, event):
                    self.state = "MAIN"
                elif inputs.is_action_just_pressed(inputs.InputAction.CONFIRM, event):
                    self._handle_load_selection()

            elif self.state == "OPTIONS":
                if inputs.is_action_just_pressed(inputs.InputAction.CANCEL, event):
                    self.state = "MAIN"

    def _handle_main_selection(self):
        selection = self.selector.current_item
        if selection == "Novo Jogo":
            self._start_new_game()
        elif selection == "Carregar Jogo":
            self._refresh_load_menu()
            self.state = "LOAD"
        elif selection == "Opções":
            self.state = "OPTIONS"
        elif selection == "Sair":
            self.context.running = False

    def _handle_load_selection(self):
        if not self.save_slots or self.load_selector.index >= len(self.save_slots):
            return
            
        slot_id = self.save_slots[self.load_selector.index]
        if slot_id is not None:
            self._load_game(slot_id)

    def _start_new_game(self):
        # Reset context for new game
        from src.models.character import Character
        from src.models.classes import Warrior
        from src.models.items import EQUIPMENT_DATA
        from src.core.state import GlobalState
        
        player = Character("Herói", Warrior())
        player.position.x, player.position.y = 64, 64
        player.gold = 50
        player.equip_item(EQUIPMENT_DATA["Espada de Ferro"])
        
        self.context.player = player
        self.context.play_time = 0.0
        self.context.global_state = GlobalState() # Fresh state
        
        # Reset world to starting village
        world = self.context.orchestrator.load_map("data/maps/starting_village.json", player=player)
        self.context.world = world
        
        # Re-init managers that depend on state/player if necessary
        if self.context.quest_manager:
            self.context.quest_manager.global_state = self.context.global_state
            self.context.quest_manager.load_quests("data/quests.json")
        
        self.manager.change_scene(ExplorationScene(self.manager))

    def _load_game(self, slot_id):
        save_data = self.context.save_manager.load_game(slot_id)
        if not save_data:
            return

        from src.models.character import Character
        from src.models.classes import Warrior, Mage, Rogue
        from src.core.state import GlobalState
        
        # Load Global State
        if 'global_state' in save_data:
            self.context.global_state = GlobalState.from_dict(save_data['global_state'])
        
        # Load Player
        class_map = {"Warrior": Warrior, "Mage": Mage, "Rogue": Rogue}
        char_class_name = save_data.get('class', 'Warrior')
        char_class = class_map.get(char_class_name, Warrior)()
        
        player = Character(save_data['name'], char_class, level=save_data['level'])
        player.hp = save_data['hp']
        player.xp = save_data['xp']
        player.energy = save_data.get('energy', 3)
        player.gold = save_data.get('gold', 0)
        player.skills = set(save_data.get('skills', []))
        player.inventory.items = save_data.get('inventory', [])
        
        # Load Equipment
        from src.models.items import EQUIPMENT_DATA
        eq_data = save_data.get('equipment', {})
        for slot, item_name in eq_data.items():
            if item_name in EQUIPMENT_DATA:
                player.equipment[slot] = EQUIPMENT_DATA[item_name]

        player.position.x = save_data['position']['x']
        player.position.y = save_data['position']['y']
        
        self.context.player = player
        self.context.play_time = save_data.get('play_time', 0.0)
        
        # Update Quest Manager
        if self.context.quest_manager:
            self.context.quest_manager.global_state = self.context.global_state
        
        # Load map
        map_name = save_data.get('location', 'starting_village')
        if not map_name.endswith('.json'):
            map_name += '.json'
        
        if not map_name.startswith('data/maps/'):
            map_path = f"data/maps/{map_name}"
        else:
            map_path = map_name
            
        world = self.context.orchestrator.load_map(map_path, player=player)
        self.context.world = world
        
        self.manager.change_scene(ExplorationScene(self.manager))

    def update(self, dt):
        pass

    def draw(self, screen):
        # Fondo degradado o color sólido
        screen.fill((10, 10, 30))
        
        if self.state == "MAIN":
            self._draw_text(screen, "RPG CLASSIC", 400, 150, size=64, color=(255, 215, 0))
            
            for i, opt in enumerate(self.options):
                color = (255, 255, 255) if i == self.selector.index else (100, 100, 100)
                prefix = "> " if i == self.selector.index else "  "
                self._draw_text(screen, f"{prefix}{opt}", 400, 300 + i*40, size=32, color=color)
        
        elif self.state == "LOAD":
            self._draw_text(screen, "CARREGAR JOGO", 400, 100, size=48, color=(0, 255, 255))
            
            if not self.load_selector.options or self.load_selector.options[0] == "Nenhum jogo salvo":
                 self._draw_text(screen, "Nenhum jogo salvo encontrado.", 400, 300, size=24, color=(150, 150, 150))
            else:
                for i, opt in enumerate(self.load_selector.options):
                    color = (255, 255, 255) if i == self.load_selector.index else (100, 100, 100)
                    prefix = "> " if i == self.load_selector.index else "  "
                    self._draw_text(screen, f"{prefix}{opt}", 400, 200 + i*40, size=24, color=color)
            
            self._draw_text(screen, "ESC: Voltar", 400, 550, size=20, color=(150, 150, 150))

        elif self.state == "OPTIONS":
            self._draw_text(screen, "OPÇÕES", 400, 100, size=48, color=(0, 255, 255))
            self._draw_text(screen, "Volume Geral: 100%", 400, 250, size=24)
            self._draw_text(screen, "Dificuldade: Normal", 400, 300, size=24)
            self._draw_text(screen, "Pressione ESC para voltar", 400, 500, size=18, color=(150, 150, 150))
            self._draw_text(screen, "ESC: Voltar", 400, 550, size=20, color=(150, 150, 150))
