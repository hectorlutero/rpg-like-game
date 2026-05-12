import unittest
from src.models.character import Character
from src.models.classes import Warrior

class TestInventorySystem(unittest.TestCase):
    def setUp(self):
        self.player = Character("Hero", Warrior())

    def test_gold_initialization(self):
        # Deve começar com 0 de ouro
        self.assertEqual(self.player.gold, 0)

    def test_add_gold(self):
        self.player.gold += 100
        self.assertEqual(self.player.gold, 100)
        
        # Não deve permitir ouro negativo
        self.player.gold = -50
        self.assertEqual(self.player.gold, 0)

    def test_inventory_add_item(self):
        # A classe Character deve ter um inventário
        self.player.inventory.add_item("Poção de Vida")
        self.assertIn("Poção de Vida", self.player.inventory.items)

    def test_inventory_remove_item(self):
        self.player.inventory.add_item("Espada de Madeira")
        self.player.inventory.remove_item("Espada de Madeira")
        self.assertNotIn("Espada de Madeira", self.player.inventory.items)

if __name__ == "__main__":
    unittest.main()
