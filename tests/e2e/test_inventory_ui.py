import os
import pygame
import pytest
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World
from src.ui.scenes import GameContext, SceneManager
from src.ui.menu_scene import MenuScene

# Configure Pygame to use a dummy video driver for headless testing
os.environ['SDL_VIDEODRIVER'] = 'dummy'

class UITester:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.world = World([[0]*10 for _ in range(10)])
        self.player = Character("Tester", Warrior())
        self.context = GameContext(self.player, self.world)
        self.manager = SceneManager(self.context)

    def post_key(self, key):
        event = pygame.event.Event(pygame.KEYDOWN, {'key': key})
        self.manager.handle_event(event)
        self.manager.update(0.1)

def test_inventory_ui_flow_automated():
    tester = UITester()
    
    # 1. Setup state
    tester.player.hp = 10
    tester.player.inventory.add_item("Poção de Vida") # 50 HP
    tester.player.inventory.add_item("Espada de Ferro")
    
    scene = MenuScene(tester.manager)
    tester.manager.push(scene)
    
    # 2. Navigate to Inventory Tab
    assert scene.tab_selector.current_item == "STATUS"
    tester.post_key(pygame.K_RIGHT)
    assert scene.tab_selector.current_item == "INVENTÁRIO"
    
    # 3. Enter Inventory Navigation (Down or Space)
    tester.post_key(pygame.K_DOWN)
    assert scene.focus == "INVENTORY_NAV"
    
    # 4. Use Potion (Should be at top or selected)
    # Alphabetical order: ["Espada de Ferro", "Poção de Vida"]
    # So we need to find where "Poção de Vida" is.
    options = tester.player.inventory.items
    idx = options.index("Poção de Vida")
    for _ in range(idx):
        tester.post_key(pygame.K_DOWN)
    
    tester.post_key(pygame.K_SPACE)
    
    # Verify Potion used
    assert tester.player.hp == 60 # 10 + 50
    assert "Poção de Vida" not in tester.player.inventory.items
    assert "Usou Poção de Vida" in scene.message
    
    # 5. Equip Sword
    # Now only "Espada de Ferro" should be left
    assert len(tester.player.inventory.items) == 1
    assert tester.player.inventory.items[0] == "Espada de Ferro"
    
    # If the inventory was refreshed and was not empty, focus should remain in INVENTORY_NAV
    # (Actually my code says if it's empty it goes back to TABS, but here it's not empty)
    
    tester.post_key(pygame.K_SPACE)
    assert tester.player.equipment["weapon"].name == "Espada de Ferro"
    assert "Espada de Ferro" not in tester.player.inventory.items
    assert "Equipou Espada de Ferro" in scene.message
    
    # Since inventory is now empty, it should have returned to TABS focus
    assert scene.focus == "TABS"
    
    pygame.quit()
