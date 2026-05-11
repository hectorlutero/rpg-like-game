import unittest
from src.models.character import Character
from src.models.classes import Warrior, Mage, Rogue

class TestCharacterInitialization(unittest.TestCase):
    def test_create_warrior_with_default_stats(self):
        # We want to be able to create a character just by passing the class
        # and it should automatically use the initial_stats defined in that class.
        hero = Character(name="Aragorn", character_class=Warrior())
        
        # Expected Strength for Warrior Level 1: (Base 10 + (1 * 2)) * 1.5 = 18
        self.assertEqual(hero.get_attribute('forca'), 18)
        self.assertEqual(hero.level, 1)

    def test_create_mage_with_default_stats(self):
        hero = Character(name="Gandalf", character_class=Mage())
        
        # Expected Intelligence for Mage Level 1: (Base 10 + (1 * 5)) * 1.8 = 27
        self.assertEqual(hero.get_attribute('inteligencia'), 27)

if __name__ == '__main__':
    unittest.main()
