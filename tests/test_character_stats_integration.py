import unittest
from src.models.character import Character
from src.models.classes import Warrior
from src.models.stats import Modifier, ModifierType

class TestCharacterStatsIntegration(unittest.TestCase):
    def test_character_uses_stats_system(self):
        """Test that get_attribute reflects modifiers added to a hidden stats collection."""
        warrior_class = Warrior()
        base_stats = {'forca': 10, 'vida': 100, 'mana': 50, 'agilidade': 10, 'inteligencia': 10}
        hero = Character(name="Aragorn", character_class=warrior_class, base_stats=base_stats, level=1)
        
        # Initial strength: (10 + (1 * 2)) * 1.5 = 18
        self.assertEqual(hero.get_attribute('forca'), 18)
        
        # Add a temporary modifier
        # We need an interface to add modifiers to the character
        hero.add_temporary_modifier('forca', Modifier(10, ModifierType.FLAT, source="Divine Strength"))
        
        # New strength should be 18 + 10 = 28
        self.assertEqual(hero.get_attribute('forca'), 28)

if __name__ == "__main__":
    unittest.main()
