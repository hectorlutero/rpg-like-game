import unittest
import os
import json
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import Position

# We will create this class next
from src.models.persistence import SaveManager

class TestPersistence(unittest.TestCase):
    def setUp(self):
        self.save_file = "test_save.json"
        self.manager = SaveManager(self.save_file)
        self.player = Character("Test Hero", Warrior())
        self.player.position = Position(100, 200)
        self.player.hp = 50
        self.player.xp = 75

    def tearDown(self):
        if os.path.exists(self.save_file):
            os.remove(self.save_file)

    def test_save_and_load_character(self):
        # Create a mock context
        class MockContext:
            def __init__(self, player):
                self.player = player
                self.opened_chests = set()
        
        ctx = MockContext(self.player)
        
        # Save the context
        success = self.manager.save_game(ctx)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(self.save_file))

        # Load into a new object
        loaded_data = self.manager.load_game()
        self.assertIsNotNone(loaded_data)
        
        # Verify stats
        self.assertEqual(loaded_data['name'], "Test Hero")
        self.assertEqual(loaded_data['level'], 1)
        self.assertEqual(loaded_data['hp'], 50)
        self.assertEqual(loaded_data['xp'], 75)
        self.assertEqual(loaded_data['position']['x'], 100)
        self.assertEqual(loaded_data['position']['y'], 200)

if __name__ == "__main__":
    unittest.main()
