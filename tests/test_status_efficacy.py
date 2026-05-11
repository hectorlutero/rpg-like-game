import unittest
from src.models.character import Character
from src.models.classes import Mage, Warrior
from src.models.combat import DamageCalculator

class TestStatusEfficacy(unittest.TestCase):
    def test_status_application_chance(self):
        # Attacker: Mage, Level 1, Intelligence 27
        attacker = Character("Attacker", Mage())
        # Defender: Warrior, Level 1, Intelligence 4
        defender = Character("Defender", Warrior())
        
        calc = DamageCalculator()
        # Formula idea: chance = 50% + (Attacker_Int - Defender_Int)
        # 50 + (27 - 4) = 73%
        chance = calc.calculate_status_chance(attacker, defender, base_chance=50)
        
        self.assertEqual(chance, 73)

    def test_status_resistance_from_defender(self):
        attacker = Character("Attacker", Mage()) # Int 27
        defender = Character("Defender", Mage())   # Int 27
        
        calc = DamageCalculator()
        # 50 + (27 - 27) = 50%
        chance = calc.calculate_status_chance(attacker, defender, base_chance=50)
        
        self.assertEqual(chance, 50)

if __name__ == '__main__':
    unittest.main()
