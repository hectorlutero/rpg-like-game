import os
import pygame
from tests.e2e.e2e_base import E2EBase
from src.ui.menu_scene import MenuScene

def main():
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    tester = E2EBase("E2E: Inventory Visual Capture")
    
    tester.player.hp = 20
    tester.player.inventory.add_item("Poção de Vida")
    tester.player.inventory.add_item("Poção de Mana")
    tester.player.inventory.add_item("Espada de Ferro")
    
    scene = MenuScene(tester.manager)
    
    # Run to the inventory tab
    tester.manager.push(scene)
    tester.manager.update(0.1)
    
    # Simulate right arrow key to switch to INVENTÁRIO tab
    event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})
    tester.manager.handle_event(event)
    tester.manager.update(0.1)
    
    tester.run(scene, auto_exit_after=10, screenshot_path="inventory_visual.png")

if __name__ == "__main__":
    main()
