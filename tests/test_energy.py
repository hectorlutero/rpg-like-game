import unittest
from src.models.character import Character
from src.models.classes import Warrior

class TestEnergySystem(unittest.TestCase):
    def setUp(self):
        self.player = Character("Hero", Warrior())

    def test_energy_initialization(self):
        # Deve começar com 3 de energia
        self.assertEqual(self.player.energy, 3)

    def test_consume_energy(self):
        self.player.energy -= 1
        self.assertEqual(self.player.energy, 2)
        
        # Não deve permitir energia negativa
        self.player.energy = -5
        self.assertEqual(self.player.energy, 0)

    def test_full_rest_recovery(self):
        # Simula desgaste
        self.player.hp = 10
        self.player.mana = 2
        self.player.energy = 0
        
        # Descansa
        self.player.rest()
        
        # Verifica recuperação total
        self.assertEqual(self.player.hp, self.player.max_hp)
        self.assertEqual(self.player.mana, self.player.max_mana)
        self.assertEqual(self.player.energy, 3)

if __name__ == "__main__":
    unittest.main()
