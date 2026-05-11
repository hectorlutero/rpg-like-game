import unittest
from src.models.character import Character
from src.models.classes import Warrior, Mage, Rogue

# Assuming we'll have a Party class in src/models/party.py
try:
    from src.models.party import Party
except ImportError:
    Party = None

class TestPartySystem(unittest.TestCase):
    def test_add_members_to_party(self):
        party = Party()
        hero1 = Character("Warrior", Warrior())
        hero2 = Character("Mage", Mage())
        
        party.add_member(hero1)
        party.add_member(hero2)
        
        self.assertEqual(len(party.members), 2)

    def test_party_max_size(self):
        party = Party()
        for i in range(5):
            party.add_member(Character(f"Hero {i}", Rogue()))
            
        self.assertEqual(len(party.members), 4) # Max size reached

    def test_shared_experience(self):
        party = Party()
        hero1 = Character("H1", Warrior())
        hero2 = Character("H2", Mage())
        party.add_member(hero1)
        party.add_member(hero2)
        
        # We need an experience system first, but let's assume a gain_xp method
        # and that the level increments when XP reaches a threshold.
        # This behavior might be too complex for now, so let's start with 
        # just adding members and basic state.
        pass

if __name__ == '__main__':
    unittest.main()
