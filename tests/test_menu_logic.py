import unittest
from src.ui.menu_scene import MenuScene
from src.ui.scenes import SceneManager, GameContext
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World

class MockManager:
    def __init__(self, context):
        self.context = context
        self.stack = []
    def push(self, scene): self.stack.append(scene)
    def pop(self): return self.stack.pop()
    def active_scene(self): return self.stack[-1] if self.stack else None

class TestMenuLogic(unittest.TestCase):
    def setUp(self):
        self.player = Character("Hero", Warrior())
        self.player.inventory.add_item("Poção de Vida")
        self.player.inventory.add_item("Espada de Ferro")
        
        self.context = GameContext(self.player, World([[]]))
        self.manager = MockManager(self.context)
        self.scene = MenuScene(self.manager)

    def test_inventory_selection_updates_selected_item_info(self):
        # Switch to Inventory tab
        self.scene.tab_selector.next() # STATUS -> INVENTORY
        self.scene.focus = "INVENTORY_NAV"
        
        # Select first item (Poção de Vida)
        self.scene.inventory_selector.index = 0
        
        # We need a way to get the currently selected item's info for the UI
        # Let's see how the current draw logic does it and expose it or test it
        selected_item = self.scene.inventory_selector.current_item
        self.assertEqual(selected_item, "Poção de Vida")
        
        # Now we need to verify that we can get the description/stats
        from src.models.items import CONSUMABLE_DATA
        item_data = CONSUMABLE_DATA.get(selected_item)
        self.assertIsNotNone(item_data)
        self.assertEqual(item_data.description, "Restaura 50 de HP.")

    def test_confirm_on_potion_uses_it_and_updates_hp(self):
        import pygame
        self.player.hp = 10
        self.scene.tab_selector.next() # INVENTORY
        self.scene.focus = "INVENTORY_NAV"
        self.scene.inventory_selector.index = 0 # Poção de Vida
        
        # Simulate SPACE key
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
        self.scene.handle_event(event)
        
        # Assert
        self.assertEqual(self.player.hp, 60)
        self.assertNotIn("Poção de Vida", self.player.inventory.items)
        self.assertEqual(self.scene.message, "Usou Poção de Vida!")

if __name__ == '__main__':
    unittest.main()
