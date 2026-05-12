import os
import sys

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests.e2e.e2e_base import E2EBase
from src.ui.menu_scene import MenuScene

def main():
    tester = E2EBase("E2E: Inventory Test")
    
    # Setup specific state: Backpack full of items
    tester.player.hp = 20 # To test healing
    tester.player.inventory.add_item("Poção de Vida")
    tester.player.inventory.add_item("Poção de Mana")
    tester.player.inventory.add_item("Antídoto")
    tester.player.inventory.add_item("Espada de Ferro")
    tester.player.inventory.add_item("Anel de Resistência")
    
    # Also add status to test curing
    tester.player.status_effects['poison'] = {'duration': 5, 'potency': 5}
    
    scene = MenuScene(tester.manager)
    tester.run(scene)

if __name__ == "__main__":
    main()
