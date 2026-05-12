import unittest
from src.models.world import World, Position
from src.models.interaction import Interactable

class MockInteractable(Interactable):
    def __init__(self, name):
        self.name = name
    def on_interact(self, context):
        return f"Interacted with {self.name}"

class TestWorldInteraction(unittest.TestCase):
    def setUp(self):
        grid = [[0 for _ in range(10)] for _ in range(10)]
        self.world = World(grid, tile_size=32)

    def test_register_and_get_interactable(self):
        obj = MockInteractable("Chest")
        # Registra no tile (5, 5)
        self.world.add_interactable(5, 5, obj)
        
        # Busca no tile (5, 5)
        found = self.world.get_interactable_at(5, 5)
        self.assertEqual(found.name, "Chest")
        
        # Busca em tile vazio
        empty = self.world.get_interactable_at(0, 0)
        self.assertIsNone(empty)

    def test_pixel_to_tile_interaction(self):
        obj = MockInteractable("NPC")
        self.world.add_interactable(2, 2, obj) # Tile (2, 2) = pixels (64, 64)
        
        # Simula busca por pixel
        found = self.world.get_interactable_at_pixel(70, 70)
        self.assertEqual(found.name, "NPC")

if __name__ == "__main__":
    unittest.main()
