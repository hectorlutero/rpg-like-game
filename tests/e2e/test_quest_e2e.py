import pytest
import pygame
from tests.e2e.ui_tester import UITester
from src.models.interaction import Interactable

class MockNPC(Interactable):
    def __init__(self, name):
        self.name = name
    def on_interact(self, context):
        return f"Olá, eu sou o {self.name}."
    def draw(self, screen, context, pos):
        pygame.draw.rect(screen, (0, 255, 0), (pos[0], pos[1], 32, 32))

class MockChest(Interactable):
    def __init__(self, item_name):
        self.name = "Baú"
        self.item_name = item_name
        self.is_open = False
    def on_interact(self, context):
        if not self.is_open:
            self.is_open = True
            context.player.receive_item(self.item_name, context.signal_bus)
            return f"Você encontrou {self.item_name}!"
        return "O baú está vazio."
    def draw(self, screen, context, pos):
        color = (139, 69, 19) if not self.is_open else (210, 105, 30)
        pygame.draw.rect(screen, color, (pos[0], pos[1], 32, 32))

def test_full_quest_narrative_loop_assisted():
    tester = UITester()
    
    # 1. Setup World with NPC and Chest
    tester.world.tile_size = 32
    npc = MockNPC("Ancião")
    chest = MockChest("Espada de Ferro")
    tester.world.interactables[(1, 1)] = npc
    tester.world.interactables[(3, 1)] = chest
    
    # Inject quest manager if not present (UITester setup is minimal)
    from src.logic.quest_manager import QuestManager
    from src.core.signals import SignalBus
    bus = SignalBus()
    tester.context.signal_bus = bus
    tester.context.quest_manager = QuestManager(tester.context.global_state, bus)
    
    tester.context.quest_manager.quests = {
        "tutorial": {
            "name": "Tutorial de Combate",
            "description": "Fale com o ancião e pegue sua arma.",
            "stages": [
                {"id": 0, "description": "Fale com o Ancião", "objectives": [{"type": "INTERACT", "target": "Ancião"}]},
                {"id": 1, "description": "Pegue a Espada de Ferro", "objectives": [{"type": "PICK_ITEM", "target": "Espada de Ferro"}]}
            ]
        }
    }
    bus.subscribe_all(tester.context.quest_manager.on_event)
    
    # Subscribe notifications if present
    from src.ui.notifications import NotificationManager
    tester.context.notification_manager = NotificationManager()
    bus.subscribe("QUEST_UPDATED", tester.context.notification_manager.on_quest_updated)
    bus.subscribe("QUEST_COMPLETED", tester.context.notification_manager.on_quest_completed)

    from src.ui.exploration_scene import ExplorationScene
    scene = ExplorationScene(tester.manager, None, None)
    tester.manager.push(scene)
    
    # 2. Accept Quest
    tester.context.quest_manager.accept_quest("tutorial")
    tester._render_watch(1.0)
    
    # 3. Go to NPC
    # Player starts at (0,0)? UITester default is (0,0) tiles
    tester.player.position.x = 32 + 16 # Tile (1, 1) but center
    tester.player.position.y = 64 + 16 # Tile (1, 2)
    tester.player.facing_direction = "N"
    tester._render_watch(0.5)
    
    tester.post_key(pygame.K_SPACE, delay=1.0) # Interact with NPC
    assert tester.context.global_state.quests["tutorial"]["stage"] == 1
    
    # Confirm Dialogue
    tester.post_key(pygame.K_SPACE, delay=0.5) 
    
    # 4. Go to Chest
    tester.player.position.x = 96 + 16 # Tile (3, 1) center
    tester.player.position.y = 64 + 16 # Tile (3, 2)
    tester.player.facing_direction = "N"
    tester._render_watch(0.5)
    
    tester.post_key(pygame.K_SPACE, delay=1.5) # Interact with Chest
    assert tester.context.global_state.quests["tutorial"]["status"] == "COMPLETED"
    
    # Confirm Chest Dialogue
    tester.post_key(pygame.K_SPACE, delay=0.5)

    # 5. Show Menu
    tester.post_key(pygame.K_m, delay=1.0) # Open Menu
    tester.post_key(pygame.K_RIGHT, delay=0.5) # STATUS -> INVENTORY
    tester.post_key(pygame.K_RIGHT, delay=1.5) # INVENTORY -> MISSÕES
    
    tester._render_watch(2.0)
    
    pygame.quit()
