import unittest
from src.models.character import Character
from src.models.classes import Mage, Warrior

# We will create Skill in src/models/skills.py
try:
    from src.models.skills import Skill, SkillRegistry
except ImportError:
    Skill = None
    SkillRegistry = None

class TestSkillSystem(unittest.TestCase):
    def test_skill_unlock_by_intelligence(self):
        # A character should unlock a skill if intelligence >= threshold
        mage = Character("Mage", Mage()) # Int Level 1 = 27
        
        # Skill with threshold 20
        fireball = Skill(name="Fireball", int_threshold=20, mana_cost=10)
        
        registry = SkillRegistry()
        registry.add_skill(fireball)
        
        unlocked_skills = registry.get_available_skills(mage)
        self.assertIn(fireball, unlocked_skills)

    def test_skill_locked_if_low_intelligence(self):
        warrior = Character("Warrior", Warrior()) # Int Level 1: (5 + (1*0.5)) * 0.9 = 4.95 -> 4
        
        fireball = Skill(name="Fireball", int_threshold=20, mana_cost=10)
        registry = SkillRegistry()
        registry.add_skill(fireball)
        
        unlocked_skills = registry.get_available_skills(warrior)
        self.assertNotIn(fireball, unlocked_skills)

    def test_spell_consumes_mana(self):
        mage = Character("Mage", Mage()) # Mana Level 1: (100 + (1*10)) * 1.5 = 165
        initial_mana = mage.get_attribute('mana')
        
        # We need a way to track CURRENT mana vs MAX mana
        mage.current_mana = initial_mana
        
        spell = Skill(name="Fireball", int_threshold=20, mana_cost=15)
        mage.use_spell(spell)
        
        self.assertEqual(mage.current_mana, initial_mana - 15)

if __name__ == '__main__':
    unittest.main()
