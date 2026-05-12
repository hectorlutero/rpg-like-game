import os
import pygame
from tests.e2e.e2e_base import E2EBase
from src.models.combat import CombatManager
from src.models.character import Character
from src.models.classes import Warrior
from src.ui.combat_scene import CombatScene
from src.models.world import Position

def main():
    # Force headless driver for script capture
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    
    tester = E2EBase("E2E: Combat Visual Capture")
    
    enemy = Character("Verme Tóxico", Warrior(), level=2)
    enemy.skills.add("Picada Venenosa")
    enemy.hp = 100
    
    cm = CombatManager(tester.context.party, [enemy], gold_reward=50, xp_reward=200)
    scene = CombatScene(tester.manager, cm, Position(0, 0))
    
    # Run for 10 frames and capture
    tester.run(scene, auto_exit_after=10, screenshot_path="combat_visual.png")

if __name__ == "__main__":
    main()
