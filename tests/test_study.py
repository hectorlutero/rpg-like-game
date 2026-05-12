import unittest
from src.models.character import Character
from src.models.classes import Warrior
from src.models.interaction import Interactable
from src.ui.scenes import GameContext

# We'll implement MagicBook next
from src.models.interaction import MagicBook

class NeutralClass:
    def __init__(self):
        self.initial_stats = {'inteligencia': 5}
        self.multipliers = {'inteligencia': 1.0}
        self.gain_rates = {'inteligencia': 0.0}

class TestStudySystem(unittest.TestCase):
    def setUp(self):
        self.player = Character("Hero", NeutralClass())
        self.player.level = 1
        self.player.base_stats['inteligencia'] = 5
        self.player.energy = 3
        self.ctx = GameContext(self.player, None)

    def test_study_increases_int(self):
        # Livro que exige 10 de INT
        book = MagicBook("Fireball", int_threshold=10, min_level=1)
        
        # Primeira leitura
        book.on_interact(self.ctx)
        self.assertEqual(self.player.get_attribute('inteligencia'), 6)
        self.assertEqual(self.player.energy, 2)
        self.assertNotIn("Fireball", self.player.skills)

    def test_learn_magic_at_threshold(self):
        # Herói já tem 9 de INT
        self.player.base_stats['inteligencia'] = 9
        book = MagicBook("Fireball", int_threshold=10, min_level=1)
        
        # Leitura que atinge o threshold
        book.on_interact(self.ctx)
        self.assertEqual(self.player.get_attribute('inteligencia'), 10)
        self.assertIn("Fireball", self.player.skills)

    def test_no_gain_beyond_threshold(self):
        # Herói já tem 10 de INT e já sabe a magia
        self.player.base_stats['inteligencia'] = 10
        self.player.skills.add("Fireball")
        book = MagicBook("Fireball", int_threshold=10, min_level=1)
        
        energy_before = self.player.energy
        book.on_interact(self.ctx)
        
        # Não deve ganhar mais INT nem gastar energia
        self.assertEqual(self.player.get_attribute('inteligencia'), 10)
        self.assertEqual(self.player.energy, energy_before)

    def test_energy_requirement(self):
        self.player.energy = 0
        book = MagicBook("Fireball", int_threshold=10, min_level=1)
        
        book.on_interact(self.ctx)
        self.assertEqual(self.player.get_attribute('inteligencia'), 5) # Não mudou

if __name__ == "__main__":
    unittest.main()
