import os
import pygame
import pytest
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World
from src.ui.scenes import GameContext, SceneManager
from src.ui.shop_scene import ShopScene

# Configure Pygame to use a dummy video driver for headless testing
os.environ['SDL_VIDEODRIVER'] = 'dummy'

class UITester:
    def __init__(self):
        pygame.init()
        # Even with dummy driver, we need a surface to avoid some internal Pygame errors
        self.screen = pygame.display.set_mode((800, 600))
        self.world = World([[0]*10 for _ in range(10)])
        self.player = Character("Tester", Warrior())
        self.context = GameContext(self.player, self.world)
        self.manager = SceneManager(self.context)

    def post_key(self, key):
        """Simulates a key press event."""
        event = pygame.event.Event(pygame.KEYDOWN, {'key': key})
        self.manager.handle_event(event)
        # Update scene to process logic
        self.manager.update(0.1)

def test_shop_ui_flow_automated():
    tester = UITester()
    tester.player.gold = 100
    
    shop_items = ["Poção de Vida", "Espada de Ferro"]
    scene = ShopScene(tester.manager, "Mercador Teste", shop_items)
    tester.manager.push(scene)
    
    # 1. Test Buying "Poção de Vida" (First item, just press Space)
    tester.post_key(pygame.K_SPACE)
    
    assert tester.player.gold == 80 # 100 - 20
    assert "Poção de Vida" in tester.player.inventory.items
    assert "Comprou Poção de Vida" in scene.message
    
    # 2. Test Navigation: Select "Espada de Ferro" (Down then Space)
    tester.post_key(pygame.K_DOWN)
    tester.post_key(pygame.K_SPACE)
    
    assert tester.player.gold == 30 # 80 - 50
    assert "Espada de Ferro" in tester.player.inventory.items
    
    # 3. Test Selling: Toggle mode (TAB)
    tester.post_key(pygame.K_TAB)
    assert scene.state == "SELL"
    
    # In SELL mode, the selector is rebuilt with player items. 
    # Player has ["Espada de Ferro", "Poção de Vida"] (sorted alphabetically in ShopScene)
    # Selector should be on "Espada de Ferro"
    
    tester.post_key(pygame.K_SPACE) # Sell "Espada de Ferro"
    
    # Sell price is 50% (50 // 2 = 25)
    assert tester.player.gold == 55 # 30 + 25
    assert "Espada de Ferro" not in tester.player.inventory.items
    assert "Vendeu Espada de Ferro" in scene.message

    pygame.quit()
