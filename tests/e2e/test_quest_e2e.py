import pytest
import pygame
from src.ui.scenes import GameContext, SceneManager
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World, Position
from src.models.interaction import Portal, InteractionManager
from src.core.signals import SignalBus
from src.logic.quest_manager import QuestManager
from src.logic.director import DirectorEngine, MapAPI
from src.core.state import GlobalState
from src.models.interaction import Interactable

class MockNPC(Interactable):
    def __init__(self, name):
        self.name = name
    def on_interact(self, context):
        return f"Olá, eu sou o {self.name}."
    def draw(self, screen, context, pos): pass

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
    def draw(self, screen, context, pos): pass

def test_full_quest_narrative_loop():
    # 1. Setup Environment
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.HIDDEN)
    
    player = Character("TestHero", Warrior())
    world = World([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    world.tile_size = 32
    
    # Place NPC at (1, 0) and Chest at (2, 0)
    npc = MockNPC("Ancião")
    chest = MockChest("Espada de Ferro")
    world.interactables[(1, 0)] = npc
    world.interactables[(2, 0)] = chest
    
    state = GlobalState()
    bus = SignalBus()
    quest_manager = QuestManager(state, bus)
    
    # Mock quest definition
    quest_manager.quests = {
        "tutorial": {
            "name": "Tutorial",
            "stages": [
                {"id": 0, "description": "Talk to Elder", "objectives": [{"type": "INTERACT", "target": "Ancião"}]},
                {"id": 1, "description": "Get Sword", "objectives": [{"type": "PICK_ITEM", "target": "Espada de Ferro"}]}
            ]
        }
    }
    bus.subscribe_all(quest_manager.on_event)
    
    context = GameContext(player, world)
    context.global_state = state
    context.signal_bus = bus
    context.quest_manager = quest_manager
    
    manager = SceneManager(context)
    interaction_manager = InteractionManager(context, manager)
    
    # 2. Accept Quest
    quest_manager.accept_quest("tutorial")
    assert state.quests["tutorial"]["stage"] == 0
    assert state.quests["tutorial"]["status"] == "IN_PROGRESS"
    
    # 3. Move to NPC and Interact
    player.position.x = 32 # Tile (1, 0)
    player.position.y = 32
    player.facing_direction = "N" # Facing tile (1, -1) - wait, tile coordinates...
    # Let's place player at (1, 1) facing North to (1, 0)
    player.position.x = 32 + 16
    player.position.y = 32 + 16
    player.facing_direction = "N"
    
    interaction_manager.interact()
    assert state.quests["tutorial"]["stage"] == 1
    
    # 4. Move to Chest and Interact
    player.position.x = 64 + 16 # Tile (2, 1)
    player.position.y = 32 + 16
    player.facing_direction = "N" # Facing tile (2, 0)
    
    interaction_manager.interact()
    assert state.quests["tutorial"]["status"] == "COMPLETED"
    assert "Espada de Ferro" in player.inventory.items
    
    pygame.quit()
