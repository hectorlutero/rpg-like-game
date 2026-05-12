import unittest
from unittest.mock import MagicMock
from src.models.interaction import InteractionManager
from src.models.dialogue import DialogueManager
from src.ui.scenes import GameContext

class TestInteractionManager(unittest.TestCase):
    def setUp(self):
        self.player = MagicMock()
        self.world = MagicMock()
        self.context = GameContext(self.player, self.world)
        self.scene_manager = MagicMock()
        self.manager = InteractionManager(self.context, self.scene_manager)

    def test_initial_state(self):
        self.assertFalse(self.manager.is_active)
        self.assertIsNone(self.manager.get_view_model())

    def test_interact_with_nothing(self):
        self.world.get_interactable_at.return_value = None
        self.manager.interact()
        self.assertFalse(self.manager.is_active)

    def test_interact_with_simple_feedback(self):
        target = MagicMock()
        target.on_interact.return_value = "Feedback message"
        target.name = "NPC"
        self.world.get_interactable_at.return_value = target
        
        self.manager.interact()
        
        self.assertTrue(self.manager.is_active)
        vm = self.manager.get_view_model()
        self.assertEqual(vm['speaker'], "NPC")
        self.assertEqual(vm['text'], "Feedback message")
        self.assertEqual(vm['choices'], [])

    def test_interact_with_dialogue_manager(self):
        dm = DialogueManager(["Line 1", "Line 2"])
        target = MagicMock()
        target.on_interact.return_value = dm
        target.name = "Guide"
        self.world.get_interactable_at.return_value = target
        
        self.manager.interact()
        
        self.assertTrue(self.manager.is_active)
        vm = self.manager.get_view_model()
        self.assertEqual(vm['text'], "Line 1")
        
        # Advance dialogue
        self.manager.process_command("confirm")
        vm = self.manager.get_view_model()
        self.assertEqual(vm['text'], "Line 2")
        self.assertTrue(self.manager.is_active)
        
        # Finish dialogue
        self.manager.process_command("confirm")
        self.assertFalse(self.manager.is_active)

    def test_dialogue_with_choices(self):
        data = {
            "start": {"text": "Choose?", "choices": {"Yes": "agreed", "No": "denied"}},
            "agreed": {"text": "Agreed"},
            "denied": {"text": "Denied"}
        }
        dm = DialogueManager(data, start_index="start")
        
        target = MagicMock()
        target.on_interact.return_value = dm
        self.world.get_interactable_at.return_value = target
        
        self.manager.interact()
        vm = self.manager.get_view_model()
        self.assertEqual(len(vm['choices']), 2)
        self.assertEqual(vm['selected_index'], 0)
        
        # Navigate
        self.manager.process_command("down")
        vm = self.manager.get_view_model()
        self.assertEqual(vm['selected_index'], 1)
        
        # Confirm choice
        self.manager.process_command("confirm")
        vm = self.manager.get_view_model()
        self.assertEqual(vm['text'], "Denied")

if __name__ == "__main__":
    unittest.main()
