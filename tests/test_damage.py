import unittest
from src.models.character import Character
from src.models.classes import Warrior, Mage

# We will create DamageCalculator in src/models/combat.py
try:
    from src.models.combat import DamageCalculator
except ImportError:
    DamageCalculator = None

class TestDamageCalculation(unittest.TestCase):
    def test_physical_damage_absolute_defense(self):
        # Attacker: Warrior, Level 1, Strength 18
        attacker = Character("Attacker", Warrior())
        # Defender: Warrior, Level 1, assuming some base defense
        defender = Character("Defender", Warrior())
        
        # Manually setting a temporary defense value for the test
        defender.defense_absolute = 5
        
        # Formula: (Strength * 1.0) - Defense = 18 - 5 = 13
        calc = DamageCalculator()
        damage = calc.calculate_physical(attacker, defender)
        
        self.assertEqual(damage, 13)

    def test_magical_damage_relative_defense(self):
        # Attacker: Mage, Level 1, Intelligence 27
        attacker = Character("Attacker", Mage())
        # Defender: Mage, Level 1
        defender = Character("Defender", Mage())
        
        # Manually setting a temporary relative defense (e.g., 20% reduction)
        defender.defense_relative = 0.20
        
        # Formula: (Intelligence * 1.0) * (1 - 0.20) = 27 * 0.8 = 21.6 -> 21
        calc = DamageCalculator()
        damage = calc.calculate_magical(attacker, defender)
        
        self.assertEqual(damage, 21)

    def test_minimum_damage_is_zero(self):
        attacker = Character("Weakling", Mage()) # Int 27, but let's say physical attack
        defender = Character("Tank", Warrior())
        defender.defense_absolute = 999
        
        calc = DamageCalculator()
        damage = calc.calculate_physical(attacker, defender)
        
        self.assertEqual(damage, 0)

if __name__ == '__main__':
    unittest.main()
