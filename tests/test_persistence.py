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
        self.save_base = "test_save"
        self.manager = SaveManager(self.save_base)
        self.player = Character("Test Hero", Warrior())
        self.player.position = Position(100, 200)
        self.player.hp = 50
        self.player.xp = 75

    def tearDown(self):
        for i in range(6):
            filename = self.manager._get_filename(i)
            if os.path.exists(filename):
                os.remove(filename)

    def test_save_and_load_character(self):
        # Create a mock context
        class MockContext:
            def __init__(self, player):
                self.player = player
                self.opened_chests = set()
                self.world = type('obj', (object,), {'map_name': 'Test Map'})
                self.play_time = 100.5
        
        ctx = MockContext(self.player)
        
        # Save to slot 1
        success = self.manager.save_game(ctx, slot=1)
        self.assertTrue(success)
        self.assertTrue(os.path.exists("test_save_1.json"))

        # Load from slot 1
        loaded_data = self.manager.load_game(slot=1)
        self.assertIsNotNone(loaded_data)
        
        # Verify stats
        self.assertEqual(loaded_data['name'], "Test Hero")
        self.assertEqual(loaded_data['level'], 1)
        self.assertEqual(loaded_data['hp'], 50)
        self.assertEqual(loaded_data['xp'], 75)
        self.assertEqual(loaded_data['position']['x'], 100)
        self.assertEqual(loaded_data['position']['y'], 200)
        self.assertEqual(loaded_data['play_time'], 100.5)

    def test_metadata_slots(self):
        class MockContext:
            def __init__(self, player, level, time):
                self.player = player
                self.player.level = level
                self.play_time = time
                self.world = type('obj', (object,), {'map_name': 'Map ' + str(level)})
    
        player1 = Character("Hero 1", Warrior())
        player2 = Character("Hero 2", Warrior())
        
        ctx1 = MockContext(player1, 1, 10.0)
        ctx2 = MockContext(player2, 5, 50.0)
        
        self.manager.save_game(ctx1, slot=1)
        self.manager.save_game(ctx2, slot=2)
        
        metadata = self.manager.get_slots_metadata()
        self.assertIn(1, metadata)
        self.assertIn(2, metadata)
        self.assertEqual(metadata[1]['level'], 1)
        self.assertEqual(metadata[2]['level'], 5)
        self.assertEqual(metadata[1]['play_time'], 10.0)
        self.assertEqual(metadata[2]['play_time'], 50.0)

if __name__ == "__main__":
    unittest.main()
