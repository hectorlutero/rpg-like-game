import os
import sys

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests.e2e.e2e_base import E2EBase
from src.ui.shop_scene import ShopScene

def main():
    tester = E2EBase("E2E: Shop Test")
    
    # Setup specific state: Player with Gold
    tester.player.gold = 500
    
    shop_items = ["Espada de Ferro", "Armadura de Couro", "Poção de Vida", "Antídoto"]
    scene = ShopScene(tester.manager, "Mercador E2E", shop_items)
    
    tester.run(scene)

if __name__ == "__main__":
    main()
