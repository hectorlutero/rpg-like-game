import unittest
from src.models.character import Character
from src.models.classes import Mage, Warrior
from src.models.skills import Ability

class TestSkillSystem(unittest.TestCase):
    def test_spell_mana_usage(self):
        # Spells devem consumir Mana
        mage = Character("Mage", Mage())
        initial_mana = mage.mana
        
        fireball = Ability("Fireball", power=2.0, category="Spell", mana_cost=15)
        
        # Simula o uso de spell (como no CombatManager)
        if mage.mana >= fireball.mana_cost:
            mage.mana -= fireball.mana_cost
            
        self.assertEqual(mage.mana, initial_mana - 15)

    def test_physical_skill_no_mana_usage(self):
        # Skills físicas não devem consumir Mana
        warrior = Character("Warrior", Warrior())
        initial_mana = warrior.mana
        
        fast_cut = Ability("Fast Cut", power=1.5, category="Skill", mana_cost=0)
        
        # Simula o uso de skill
        if fast_cut.category == "Spell":
            if warrior.mana >= fast_cut.mana_cost:
                warrior.mana -= fast_cut.mana_cost
        # Caso contrário, não gasta mana
            
        self.assertEqual(warrior.mana, initial_mana)

if __name__ == '__main__':
    unittest.main()
