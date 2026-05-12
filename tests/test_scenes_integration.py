import unittest
import pygame
from src.ui.scenes import GameContext, SceneManager
from src.ui.exploration_scene import ExplorationScene
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World, Position

class TestScenesIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.font.init()
        # Precisamos de uma tela pequena para o Pygame não reclamar
        cls.screen = pygame.display.set_mode((1, 1), pygame.HIDDEN)

    def setUp(self):
        self.player = Character("Hero", Warrior())
        self.player.position = Position(32, 32) # Tile (1,1)
        # Grid 10x10 livre
        self.world = World([[0]*10 for _ in range(10)])
        self.context = GameContext(self.player, self.world)
        self.context.save_manager = None # Mock
        self.manager = SceneManager(self.context)
        
        from src.models.dialogue import NPC
        mock_npc = NPC("Test", Position(64, 64))
        self.scene = ExplorationScene(self.manager, mock_npc, Position(100, 100))
        self.manager.push(self.scene)

    def test_keyboard_movement_integration(self):
        # Simula apertar a tecla 'D' (Direita)
        # No ExplorationScene, o movimento real acontece no update() checando get_pressed
        # Mas vamos testar se a cena responde ao ciclo de update
        
        initial_x = self.player.position.x
        
        # Mock do pygame.key.get_pressed
        # Como K_RIGHT tem um valor imenso (1073...), usamos um mock esperto
        original_get_pressed = pygame.key.get_pressed
        
        class MockKeyArray:
            def __getitem__(self, key):
                return 1 if key in [pygame.K_RIGHT, pygame.K_d] else 0
        
        pygame.key.get_pressed = lambda: MockKeyArray()
        
        # Roda um frame de update (dt = 1.0)
        # player_speed = 4, então deve mover 4 pixels
        self.scene.update(1.0)
        
        self.assertEqual(self.player.position.x, initial_x + 4)
        self.assertEqual(self.player.facing_direction, "E")
        
        # Restaura o original
        pygame.key.get_pressed = original_get_pressed

    def test_menu_open_event(self):
        # Simula o evento KEYDOWN para abrir o menu
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_m})
        
        self.scene.handle_event(event)
        
        # Verifica se o MenuScene foi empilhado
        from src.ui.menu_scene import MenuScene
        self.assertIsInstance(self.manager.active_scene, MenuScene)

    def test_interaction_trigger_event(self):
        # Coloca um baú na frente do herói (Hero está no 1,1 olhando Sul, vamos pôr no 1,2)
        from src.models.interaction import Chest
        chest = Chest(chest_id="test_chest")
        self.world.add_interactable(1, 2, chest)
        self.player.facing_direction = "S"
        
        # Evento Espaço
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE})
        self.scene.handle_event(event)
        
        # Verifica se o diálogo do baú foi ativado na cena via InteractionManager
        self.assertTrue(self.scene.interaction_manager.is_active)
        self.assertTrue(chest.is_open)

    def test_rendering_no_crash(self):
        # Testa se o draw roda sem crashar em diferentes estados
        
        # 1. Estado Normal
        self.scene.draw(self.screen)
        
        # 2. Com Diálogo Ativo
        from src.models.dialogue import DialogueManager
        self.scene.interaction_manager.active_dialogue = DialogueManager(["Linha 1\nLinha 2"])
        self.scene.draw(self.screen)
        
        # 3. Com Menu Aberto
        from src.ui.menu_scene import MenuScene
        menu = MenuScene(self.manager)
        menu.draw(self.screen)

if __name__ == "__main__":
    unittest.main()
