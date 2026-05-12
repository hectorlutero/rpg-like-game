import unittest
from src.models.character import Character
from src.models.classes import Warrior

# We will create World and Movement system in src/models/world.py
try:
    from src.models.world import World, Position
except ImportError:
    World = None
    Position = None

class TestMovement(unittest.TestCase):
    def test_character_starts_at_origin(self):
        hero = Character("Hero", Warrior())
        # We need to attach a position to the character
        hero.position = Position(0, 0)
        self.assertEqual(hero.position.x, 0)
        self.assertEqual(hero.position.y, 0)

    def test_move_right(self):
        hero = Character("Hero", Warrior())
        hero.position = Position(0, 0)
        
        # Simple move logic: move(dx, dy)
        hero.position.move(10, 0)
        self.assertEqual(hero.position.x, 10)
        self.assertEqual(hero.position.y, 0)

    def test_collision_with_solid_tile(self):
        # Create a 3x3 map where (1,0) is solid
        grid = [
            [0, 1, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        world = World(grid, tile_size=32)
        hero = Character("Hero", Warrior())
        # Coloca o herói no centro do tile (0,0) -> (16, 16)
        hero.position = Position(16, 16)
        
        # Tenta mover para o centro do tile (1,0) -> (48, 16)
        # O tile (1,0) é sólido, então deve bloquear.
        can_move = world.can_move_to(hero, 48, 16)
        self.assertFalse(can_move)
        
        # Tenta mover para o centro do tile (0,1) -> (16, 48)
        # O tile (0,1) é passável, deve permitir.
        can_move = world.can_move_to(hero, 16, 48)
        self.assertTrue(can_move)

if __name__ == '__main__':
    unittest.main()
