import unittest
from src.models.character import Character
from src.models.classes import Warrior
from src.models.party import Party

class TestExperienceSystem(unittest.TestCase):
    def test_character_level_up(self):
        hero = Character("Hero", Warrior())
        # Let's say 100 XP is needed for Level 2
        hero.gain_xp(100)
        self.assertEqual(hero.level, 2)
        self.assertEqual(hero.xp, 0) # Remainder after level up

    def test_party_shared_xp(self):
        party = Party()
        hero1 = Character("H1", Warrior())
        hero2 = Character("H2", Warrior())
        party.add_member(hero1)
        party.add_member(hero2)
        
        # 100 XP shared between 2 members = 50 each
        party.gain_xp(100)
        self.assertEqual(hero1.xp, 50)
        self.assertEqual(hero2.xp, 50)

if __name__ == '__main__':
    unittest.main()
