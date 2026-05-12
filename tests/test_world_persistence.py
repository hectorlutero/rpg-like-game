import unittest
import os
import json
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World, Position
from src.models.interaction import Chest
from src.models.persistence import SaveManager
from src.ui.scenes import GameContext

class TestWorldPersistence(unittest.TestCase):
    def setUp(self):
        self.save_file = "test_world_save.json"
        self.manager = SaveManager(self.save_file)
        self.player = Character("Hero", Warrior())
        self.world = World([[0]*10 for _ in range(10)])
        self.ctx = GameContext(self.player, self.world)

    def tearDown(self):
        if os.path.exists(self.save_file):
            os.remove(self.save_file)

    def test_chest_state_persistence(self):
        # 1. Cria um baú e abre ele
        chest = Chest(chest_id="persistent_chest_1")
        # No novo sistema, basta adicionar ao contexto e o baú se auto-sincroniza
        self.ctx.opened_chests.add("persistent_chest_1")
        
        # 2. Salva o contexto
        self.manager.save_game(self.ctx)
        
        # 3. Simula um novo jogo carregando os dados
        loaded_data = self.manager.load_game()
        self.assertIn("persistent_chest_1", loaded_data['opened_chests'])
        
        # 4. Verifica se a lógica de reconstrução funciona
        new_ctx = GameContext(self.player, self.world)
        new_ctx.opened_chests = set(loaded_data.get('opened_chests', []))
        
        # O baú no mapa deve responder ao estado carregado via check_open
        test_chest = Chest(chest_id="persistent_chest_1")
        is_open = test_chest.check_open(new_ctx)
            
        self.assertTrue(is_open)
        self.assertTrue(test_chest.is_open)

if __name__ == "__main__":
    unittest.main()
