import unittest
from src.models.world import Position

# We will create NPC and Dialogue classes in src/models/dialogue.py
try:
    from src.models.dialogue import NPC, DialogueManager
except ImportError:
    NPC = None
    DialogueManager = None

class TestDialogueSystem(unittest.TestCase):
    def test_npc_proximity(self):
        npc = NPC(name="Ancião", position=Position(100, 100))
        player_pos = Position(110, 110)
        
        # NPC should be interactable within 32 pixels
        self.assertTrue(npc.is_near(player_pos, distance=32))
        
        # Too far
        far_player = Position(200, 200)
        self.assertFalse(npc.is_near(far_player, distance=32))

    def test_dialogue_flow(self):
        lines = ["Olá, viajante!", "O clima está ótimo hoje.", "Adeus!"]
        manager = DialogueManager(lines)
        
        self.assertEqual(manager.get_current_line(), "Olá, viajante!")
        self.assertFalse(manager.is_finished())
        
        manager.next_line()
        self.assertEqual(manager.get_current_line(), "O clima está ótimo hoje.")
        
        manager.next_line()
        manager.next_line()
        self.assertTrue(manager.is_finished())

    def test_dialogue_with_choices(self):
        # Format: (text, choices_dict)
        # Choice dict: {choice_text: next_index_or_branch}
        dialogue_data = {
            0: {"text": "Você quer uma poção?", "choices": {"Sim": 1, "Não": 2}},
            1: {"text": "Aqui está sua poção!", "choices": None},
            2: {"text": "Tudo bem, até logo.", "choices": None}
        }
        manager = DialogueManager(dialogue_data, start_index=0)
        
        self.assertEqual(manager.get_current_line(), "Você quer uma poção?")
        manager.make_choice("Sim")
        self.assertEqual(manager.get_current_line(), "Aqui está sua poção!")

if __name__ == '__main__':
    unittest.main()
