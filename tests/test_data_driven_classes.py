import unittest
import json
import os
from src.models.classes import Warrior, Mage, Rogue

class TestDataDrivenClasses(unittest.TestCase):
    def test_warrior_loads_from_json(self):
        """Warrior should have stats defined in the JSON file."""
        warrior = Warrior()
        self.assertEqual(warrior.initial_stats['vida'], 100)
        self.assertEqual(warrior.proficiencies['sword'], 1.2)

    def test_mage_loads_from_json(self):
        """Mage should have stats defined in the JSON file."""
        mage = Mage()
        self.assertEqual(mage.initial_stats['mana'], 100)
        self.assertEqual(mage.proficiencies['staff'], 1.3)

if __name__ == "__main__":
    unittest.main()
