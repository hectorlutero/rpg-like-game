import unittest
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World, Position
from src.models.interaction import Chest
from src.models.items import Equipment
from src.ui.scenes import GameContext, SceneManager

class TestInteractablesLogic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import pygame
        pygame.font.init()

    def setUp(self):
        self.player = Character("Hero", Warrior())
        self.world = World([[0]*10 for _ in range(10)])
        self.context = GameContext(self.player, self.world)
        self.context.scene_manager = SceneManager(self.context)

    def test_chest_interaction_gold_and_item(self):
        item = Equipment("Test Item", "Desc", slot="accessory")
        chest = Chest(items=[item], gold=50, chest_id="test_id")
        
        # Primeira interação
        msg = chest.on_interact(self.context)
        
        self.assertTrue(chest.is_open)
        self.assertEqual(self.player.gold, 50)
        self.assertIn("Test Item", self.player.inventory.items)
        self.assertIn("test_id", self.context.opened_chests)
        self.assertIn("Você abriu o baú", msg)

    def test_chest_cannot_be_opened_twice(self):
        chest = Chest(gold=50)
        chest.on_interact(self.context) # Abre primeira vez
        
        self.player.gold = 0 # Reseta ouro para teste
        msg = chest.on_interact(self.context)
        
        self.assertEqual(self.player.gold, 0) # Não ganhou de novo
        self.assertIn("vazio", msg)

    def test_shopkeeper_interaction_returns_scene(self):
        from src.ui.shop_scene import Shopkeeper, ShopScene
        keeper = Shopkeeper("Merchant", ["Espada de Ferro"])
        
        result = keeper.on_interact(self.context)
        
        self.assertIsInstance(result, ShopScene)
        self.assertEqual(result.shop_name, "Merchant")

    def test_enemy_interaction_rewards(self):
        from src.models.combat import EnemyInteractable
        from src.ui.combat_scene import CombatScene
        
        enemy_trigger = EnemyInteractable("Slime", Warrior(), 1, Position(0,0), gold_yield=10, xp_yield=20)
        result = enemy_trigger.on_interact(self.context)
        
        self.assertIsInstance(result, CombatScene)
        # Verifica se o CombatManager recebeu as recompensas
        self.assertEqual(result.combat_manager.gold_reward, 10)
        self.assertEqual(result.combat_manager.xp_reward, 20)

if __name__ == "__main__":
    unittest.main()
