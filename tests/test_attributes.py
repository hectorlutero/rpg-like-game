import unittest
from src.models.character import Character
from src.models.classes import Warrior, Mage, Rogue

class TestAttributes(unittest.TestCase):
    def test_warrior_initial_strength(self):
        # Warrior stats: Base 10, Mult 1.5, Gain 2.0
        # Level 1: (10 + (1 * 2)) * 1.5 = 18
        warrior_class = Warrior()
        base_stats = {'forca': 10, 'vida': 100, 'mana': 50, 'agilidade': 10, 'inteligencia': 10}
        hero = Character(name="Aragorn", character_class=warrior_class, base_stats=base_stats, level=1)
        self.assertEqual(hero.get_attribute('forca'), 18)

    def test_attribute_growth_on_level_up(self):
        # Warrior stats: Base 10, Mult 1.5, Gain 2.0
        # Level 10: (10 + (10 * 2)) * 1.5 = 45
        warrior_class = Warrior()
        base_stats = {'forca': 10, 'vida': 100, 'mana': 50, 'agilidade': 10, 'inteligencia': 10}
        hero = Character(name="Aragorn", character_class=warrior_class, base_stats=base_stats, level=1)
        hero.level = 10
        self.assertEqual(hero.get_attribute('forca'), 45)
    
    def test_mage_initial_intelligence(self):
        # Mage stats: Base 10, Mult 1.8, Gain 5.0
        # Level 1: (10 + (1 * 5)) * 1.8 = 27
        mage_class = Mage()
        base_stats = {'forca': 10, 'vida': 100, 'mana': 50, 'agilidade': 10, 'inteligencia': 10}
        hero = Character(name="Gandalf", character_class=mage_class, base_stats=base_stats, level=1)
        self.assertEqual(hero.get_attribute('inteligencia'), 27)

    def test_rogue_initial_agility(self):
        # Rogue stats: Base 10, Mult 1.6, Gain 4.0
        # Level 1: (10 + (1 * 4)) * 1.6 = 14 * 1.6 = 22.4 (22)
        rogue_class = Rogue()
        base_stats = {'forca': 10, 'vida': 100, 'mana': 50, 'agilidade': 10, 'inteligencia': 10}
        hero = Character(name="Legolas", character_class=rogue_class, base_stats=base_stats, level=1)
        self.assertEqual(hero.get_attribute('agilidade'), 22)

if __name__ == '__main__':
    unittest.main()
