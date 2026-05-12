import pygame
import pytest
from tests.e2e.ui_tester import UITester
from src.ui.menu_scene import MenuScene

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
