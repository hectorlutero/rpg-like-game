import unittest
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World, Position
from src.models.interaction import Interactable
from src.ui.scenes import GameContext

class MockInteractable(Interactable):
    def __init__(self):
        self.called = False
    def on_interact(self, context):
        self.called = True

class TestInteractionTrigger(unittest.TestCase):
    def setUp(self):
        grid = [[0 for _ in range(10)] for _ in range(10)]
        self.world = World(grid)
        self.player = Character("Hero", Warrior())
        self.context = GameContext(self.player, self.world)

    def test_get_target_tile(self):
        # Herói no tile (5, 5) olhando para o Norte
        self.player.position.x = 5 * 32
        self.player.position.y = 5 * 32
        self.player.facing_direction = "N"
        
        # O tile alvo deve ser (5, 4)
        tx = int(self.player.position.x // 32)
        ty = int(self.player.position.y // 32)
        
        target_x, target_y = tx, ty
        if self.player.facing_direction == "N": target_y -= 1
        
        self.assertEqual((target_x, target_y), (5, 4))

    def test_successful_interaction_trigger(self):
        # Coloca objeto no (5, 4)
        obj = MockInteractable()
        self.world.add_interactable(5, 4, obj)
        
        # Herói no (5, 5) olhando para o Norte
        self.player.position.x = 5 * 32
        self.player.position.y = 5 * 32
        self.player.facing_direction = "N"
        
        # Simula lógica de gatilho
        tx = int(self.player.position.x // 32)
        ty = int(self.player.position.y // 32)
        if self.player.facing_direction == "N": ty -= 1
        elif self.player.facing_direction == "S": ty += 1
        elif self.player.facing_direction == "W": tx -= 1
        elif self.player.facing_direction == "E": tx += 1
        
        target = self.world.get_interactable_at(tx, ty)
        if target:
            target.on_interact(self.context)
            
        self.assertTrue(obj.called)

if __name__ == "__main__":
    unittest.main()
