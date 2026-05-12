import unittest
from src.ui.scenes import GameContext

# Classe base que vamos criar
class Interactable:
    def on_interact(self, context):
        raise NotImplementedError

class MockObject(Interactable):
    def __init__(self):
        self.interacted = False
    def on_interact(self, context):
        self.interacted = True

class TestInteractable(unittest.TestCase):
    def test_interactable_interface(self):
        obj = MockObject()
        ctx = None # Mock do contexto
        obj.on_interact(ctx)
        self.assertTrue(obj.interacted)

if __name__ == "__main__":
    unittest.main()
