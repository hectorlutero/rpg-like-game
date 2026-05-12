import unittest
from src.models.character import Character
from src.models.classes import Warrior
from src.models.items import CONSUMABLE_DATA

class TestInventoryUsage(unittest.TestCase):
    def setUp(self):
        self.player = Character("Hero", Warrior())
        self.player.hp = 10 # Low HP to test restoration

    def test_use_hp_potion_restores_hp_and_removes_item(self):
        item_name = "Poção de Vida"
        self.player.inventory.add_item(item_name)
        
        # Act
        success, msg = self.player.use_item(item_name)
        
        # Assert
        self.assertTrue(success)
        self.assertEqual(self.player.hp, 60) # 10 + 50
        self.assertNotIn(item_name, self.player.inventory.items)

    def test_use_antidote_cures_poison(self):
        item_name = "Antídoto"
        self.player.inventory.add_item(item_name)
        self.player.status_effects['poison'] = {'duration': 3, 'potency': 10}
        
        # Act
        success, msg = self.player.use_item(item_name)
        
        # Assert
        self.assertTrue(success)
        self.assertNotIn('poison', self.player.status_effects)
        self.assertNotIn(item_name, self.player.inventory.items)

if __name__ == '__main__':
    unittest.main()
