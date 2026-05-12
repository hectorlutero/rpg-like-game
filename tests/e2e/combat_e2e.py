import os
import sys

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests.e2e.e2e_base import E2EBase
from src.models.combat import CombatManager
from src.models.character import Character
from src.models.classes import Warrior
from src.ui.combat_scene import CombatScene
from src.models.world import Position

def main():
    tester = E2EBase("E2E: Combat Test (Toxic Worm)")
    
    # Setup specific state
    enemy = Character("Verme Tóxico", Warrior(), level=2)
    enemy.skills.add("Picada Venenosa")
    enemy.hp = 100
    
    cm = CombatManager(tester.context.party, [enemy], gold_reward=50, xp_reward=200)
    scene = CombatScene(tester.manager, cm, Position(0, 0))
    
    tester.run(scene)

if __name__ == "__main__":
    main()
