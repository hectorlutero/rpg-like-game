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
        # Defender: Warrior, Level 1
        defender = Character("Defender", Warrior())
        
        # Equip defensive item to set defense_absolute
        from src.models.items import Equipment
        shield = Equipment("Shield", "Desc", slot="shield", bonuses={'defesa_absoluta': 5})
        defender.equip_item(shield)
        
        # Formula: (Strength * 1.0) - Defense = 18 - 5 = 13
        calc = DamageCalculator()
        damage = calc.calculate_physical(attacker, defender)
        
        self.assertEqual(damage, 13)

    def test_magical_damage_relative_defense(self):
        # Attacker: Mage, Level 1, Intelligence 27
        attacker = Character("Attacker", Mage())
        # Defender: Mage, Level 1
        defender = Character("Defender", Mage())
        
        # Equip item to set relative defense (20% reduction)
        from src.models.items import Equipment
        cape = Equipment("Cape", "Desc", slot="armor", bonuses={'defesa_relativa': 0.20})
        defender.equip_item(cape)
        
        # Formula: (Intelligence * 1.0) * (1 - 0.20) = 27 * 0.8 = 21.6 -> 21
        calc = DamageCalculator()
        damage = calc.calculate_magical(attacker, defender)
        
        self.assertEqual(damage, 21)

    def test_minimum_damage_is_zero(self):
        attacker = Character("Weakling", Mage()) # Int 27
        defender = Character("Tank", Warrior())
        
        # Super armor
        from src.models.items import Equipment
        god_armor = Equipment("God Armor", "Desc", slot="armor", bonuses={'defesa_absoluta': 999})
        defender.equip_item(god_armor)
        
        calc = DamageCalculator()
        damage = calc.calculate_physical(attacker, defender)
        
        self.assertEqual(damage, 0)

if __name__ == '__main__':
    unittest.main()
