import unittest
from src.models.character import Character
from src.models.classes import Warrior
from src.models.interaction import TrainingObject
from src.ui.scenes import GameContext

class TestTrainingSystem(unittest.TestCase):
    def setUp(self):
        self.player = Character("Hero", Warrior())
        self.player.energy = 3
        self.ctx = GameContext(self.player, None)

    def test_strength_training(self):
        initial_str = self.player.base_stats['forca']
        dummy = TrainingObject("Força", "forca")
        
        msg = dummy.on_interact(self.ctx)
        self.assertEqual(self.player.base_stats['forca'], initial_str + 1)
        self.assertEqual(self.player.energy, 2)
        self.assertIn("Sua Força aumentou", msg)

    def test_agility_training(self):
        initial_agi = self.player.base_stats['agilidade']
        treadmill = TrainingObject("Agilidade", "agilidade")
        
        dummy_msg = treadmill.on_interact(self.ctx)
        self.assertEqual(self.player.base_stats['agilidade'], initial_agi + 1)
        self.assertEqual(self.player.energy, 2)

    def test_training_requires_energy(self):
        self.player.energy = 0
        initial_str = self.player.base_stats['forca']
        dummy = TrainingObject("Força", "forca")
        
        msg = dummy.on_interact(self.ctx)
        self.assertEqual(self.player.base_stats['forca'], initial_str)
        self.assertIn("exausto", msg)

if __name__ == "__main__":
    unittest.main()
