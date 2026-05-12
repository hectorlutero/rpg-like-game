import unittest
from src.models.stats import Stat, Modifier, ModifierType

class TestStatsPackage(unittest.TestCase):
    def test_base_value_only(self):
        """Behaves correctly with only a base value."""
        s = Stat("strength", base_value=10)
        self.assertEqual(s.calculate(), 10)

    def test_flat_modifier(self):
        """Adds flat modifiers correctly."""
        s = Stat("strength", base_value=10)
        s.add_modifier(Modifier(5, ModifierType.FLAT, source="Sword"))
        self.assertEqual(s.calculate(), 15)

    def test_percent_modifier(self):
        """Applies percent modifiers correctly."""
        s = Stat("strength", base_value=10)
        s.add_modifier(Modifier(0.5, ModifierType.PERCENT, source="Buff")) # +50%
        self.assertEqual(s.calculate(), 15)

    def test_stacking_modifiers(self):
        """Stacks multiple types correctly: (Base + Flat) * (1 + Percent)."""
        s = Stat("strength", base_value=10)
        s.add_modifier(Modifier(10, ModifierType.FLAT, source="Sword")) # 10 + 10 = 20
        s.add_modifier(Modifier(0.5, ModifierType.PERCENT, source="Buff")) # 20 * 1.5 = 30
        self.assertEqual(s.calculate(), 30)

    def test_remove_by_source(self):
        """Removes all modifiers from a specific source."""
        s = Stat("strength", base_value=10)
        s.add_modifier(Modifier(10, ModifierType.FLAT, source="Sword"))
        s.add_modifier(Modifier(0.5, ModifierType.PERCENT, source="Buff"))
        
        s.remove_modifiers_from_source("Sword")
        # Base 10 * 1.5 = 15
        self.assertEqual(s.calculate(), 15)

if __name__ == "__main__":
    unittest.main()
