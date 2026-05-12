import os
import pygame
from tests.e2e.e2e_base import E2EBase
from src.ui.shop_scene import ShopScene

def main():
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    tester = E2EBase("E2E: Shop Visual Capture")
    
    tester.player.gold = 500
    shop_items = ["Espada de Ferro", "Armadura de Placas", "Poção de Vida"]
    scene = ShopScene(tester.manager, "Mercador de Teste", shop_items)
    
    tester.manager.push(scene)
    tester.manager.update(0.1)
    
    tester.run(scene, auto_exit_after=10, screenshot_path="shop_visual.png")

if __name__ == "__main__":
    main()
