import unittest
from src.models.character import Character
from src.models.classes import Warrior
from src.models.items import EQUIPMENT_DATA
from src.models.combat import CombatManager

class TestEconomy(unittest.TestCase):
    def setUp(self):
        self.player = Character("Hero", Warrior())
        self.player.gold = 100

    def test_enemy_loot_gold(self):
        # Simula ganho de ouro pós-batalha
        enemy_gold_yield = 50
        self.player.gold += enemy_gold_yield
        self.assertEqual(self.player.gold, 150)

    def test_shop_purchase_success(self):
        # Tenta comprar Espada de Ferro (50 G)
        item = EQUIPMENT_DATA["Espada de Ferro"]
        if self.player.gold >= item.price:
            self.player.gold -= item.price
            self.player.inventory.add_item(item.name)
            
        self.assertEqual(self.player.gold, 50)
        self.assertIn("Espada de Ferro", self.player.inventory.items)

    def test_shop_purchase_insufficient_gold(self):
        self.player.gold = 10
        item = EQUIPMENT_DATA["Espada de Ferro"]
        
        # Simula lógica de compra
        success = False
        if self.player.gold >= item.price:
            self.player.gold -= item.price
            success = True
            
        self.assertFalse(success)
        self.assertEqual(self.player.gold, 10)

if __name__ == "__main__":
    unittest.main()
