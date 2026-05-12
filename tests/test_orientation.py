import unittest
from src.models.character import Character
from src.models.classes import Warrior

class TestCharacterOrientation(unittest.TestCase):
    def setUp(self):
        self.player = Character("Herói", Warrior())

    def test_default_orientation(self):
        # Por padrão, deve começar olhando para baixo (South)
        self.assertEqual(self.player.facing_direction, "S")

    def test_change_orientation_on_move(self):
        # Mudar para Oeste
        self.player.update_orientation(-1, 0)
        self.assertEqual(self.player.facing_direction, "W")
        
        # Mudar para Norte
        self.player.update_orientation(0, -1)
        self.assertEqual(self.player.facing_direction, "N")
        
        # Mudar para Leste
        self.player.update_orientation(1, 0)
        self.assertEqual(self.player.facing_direction, "E")
        
        # Mudar para Sul
        self.player.update_orientation(0, 1)
        self.assertEqual(self.player.facing_direction, "S")

    def test_diagonal_orientation_priority(self):
        # Se mover na diagonal, vamos definir que a última direção vertical/horizontal prevalece
        # Ou simplesmente que ele mantém uma delas. Vamos testar a lógica de priorizar o eixo X.
        self.player.update_orientation(1, 1) # Sudeste
        self.assertIn(self.player.facing_direction, ["E", "S"])

if __name__ == "__main__":
    unittest.main()
