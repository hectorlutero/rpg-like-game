import unittest
from src.ui.scenes import SceneManager, Scene, GameContext

class MockScene(Scene):
    def __init__(self):
        self.updated = False
        self.handled = False
        self.drawn = False

    def update(self, dt): self.updated = True
    def handle_event(self, event): self.handled = True
    def draw(self, screen): self.drawn = True

class TestSceneManager(unittest.TestCase):
    def setUp(self):
        self.context = GameContext(None, None)
        self.manager = SceneManager(self.context)

    def test_stack_operations(self):
        scene1 = MockScene()
        scene2 = MockScene()
        
        # Test Push
        self.manager.push(scene1)
        self.assertEqual(self.manager.active_scene, scene1)
        self.assertEqual(len(self.manager.stack), 1)
        
        self.manager.push(scene2)
        self.assertEqual(self.manager.active_scene, scene2)
        self.assertEqual(len(self.manager.stack), 2)
        
        # Test Pop
        popped = self.manager.pop()
        self.assertEqual(popped, scene2)
        self.assertEqual(self.manager.active_scene, scene1)
        
        # Test Change Scene (clears stack)
        scene3 = MockScene()
        self.manager.change_scene(scene3)
        self.assertEqual(self.manager.active_scene, scene3)
        self.assertEqual(len(self.manager.stack), 1)

    def test_delegation(self):
        scene = MockScene()
        self.manager.push(scene)
        
        self.manager.update(1.0)
        self.assertTrue(scene.updated)
        
        self.manager.handle_event(None)
        self.assertTrue(scene.handled)
        
        self.manager.draw(None)
        self.assertTrue(scene.drawn)

    def test_empty_stack_safety(self):
        # Nao deve crashar se a pilha estiver vazia
        self.manager.update(1.0)
        self.manager.handle_event(None)
        self.manager.draw(None)
        self.assertIsNone(self.manager.active_scene)
        self.assertEqual(self.manager.pop(), None)

if __name__ == "__main__":
    unittest.main()
