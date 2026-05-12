import unittest
from src.models.character import Character
from src.models.classes import Warrior, Mage
from src.models.items import Equipment

class TestEquipmentSystem(unittest.TestCase):
    def setUp(self):
        self.player = Character("Hero", Warrior())
        # Força base do Warrior no Nível 1: (10 + (1*2.0)) * 1.5 = 18

    def test_equip_weapon_increases_strength(self):
        initial_str = self.player.get_attribute('forca')
        
        # Espada que dá +5 Força
        sword = Equipment("Test Sword", "Desc", slot="weapon", bonuses={'forca': 5})
        success, old = self.player.equip_item(sword)
        
        self.assertTrue(success)
        self.assertEqual(self.player.get_attribute('forca'), initial_str + 5)
        self.assertEqual(self.player.equipment['weapon'], sword)

    def test_equip_armor_increases_defense(self):
        # Armadura que dá +10 Defesa Absoluta
        armor = Equipment("Plate Mail", "Desc", slot="armor", bonuses={'defesa_absoluta': 10})
        self.player.equip_item(armor)
        
        self.assertEqual(self.player.defense_absolute, 10)

    def test_requirement_gating_strength(self):
        # Espada que exige 50 de Força
        heavy_sword = Equipment("Heavy Sword", "Desc", slot="weapon", req_stats={'forca': 50})
        
        success, msg = self.player.equip_item(heavy_sword)
        self.assertFalse(success)
        self.assertIn("Forca insuficiente", msg)
        self.assertIsNone(self.player.equipment['weapon'])

    def test_requirement_gating_class(self):
        # Cajado que exige classe Mage
        staff = Equipment("Staff", "Desc", slot="weapon", req_class="Mage")
        
        success, msg = self.player.equip_item(staff)
        self.assertFalse(success)
        self.assertIn("Classe Warrior não pode usar", msg)

if __name__ == "__main__":
    unittest.main()
