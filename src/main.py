import pygame
import sys
import os

from src.models.character import Character
from src.models.classes import Warrior, Mage, Rogue
from src.models.world import World, Position
from src.models.persistence import SaveManager
from src.ui.scenes import GameContext, SceneManager
from src.ui.exploration_scene import ExplorationScene
from src.core.registry import EntityRegistry
from src.core.orchestrator import WorldOrchestrator
from src.core.state import GlobalState
from src.core.signals import SignalBus
from src.logic.director import DirectorEngine, MapAPI
from src.logic.quest_manager import QuestManager
from src.ui.notifications import NotificationManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("RPG Classic - LEGO Engine")
    clock = pygame.time.Clock()
    
    # --- 1. System Init ---
    registry = EntityRegistry("data/entities.json")
    save_manager = SaveManager("savegame.json")
    save_data = save_manager.load_game()
    signal_bus = SignalBus()
    
    # --- 2. State & Player Init ---
    player = None
    global_state = GlobalState()
    
    if save_data:
        # Load Global State
        if 'global_state' in save_data:
            global_state = GlobalState.from_dict(save_data['global_state'])
        elif 'opened_chests' in save_data:
            for cid in save_data['opened_chests']:
                global_state.set_entity_delta(cid, {"_is_open": True})
        
        # Load Player
        char_class = save_manager.class_map.get(save_data.get('class', 'Warrior'), Warrior)()
        player = Character(save_data['name'], char_class, level=save_data['level'])
        player.hp = save_data['hp']
        player.xp = save_data['xp']
        player.energy = save_data.get('energy', 3)
        player.gold = save_data.get('gold', 0)
        player.skills = set(save_data.get('skills', []))
        player.inventory.items = save_data.get('inventory', [])
        
        # Load Equipment
        from src.models.items import EQUIPMENT_DATA
        eq_data = save_data.get('equipment', {})
        for slot, item_name in eq_data.items():
            if item_name in EQUIPMENT_DATA:
                player.equipment[slot] = EQUIPMENT_DATA[item_name]

        player.position.x = save_data['position']['x']
        player.position.y = save_data['position']['y']
    else:
        # New Game
        player = Character("Herói", Warrior())
        player.position.x, player.position.y = 64, 64
        player.gold = 50
        from src.models.items import EQUIPMENT_DATA
        player.equip_item(EQUIPMENT_DATA["Espada de Ferro"])

    quest_manager = QuestManager(global_state, signal_bus)
    quest_manager.load_quests("data/quests.json")
    signal_bus.subscribe_all(quest_manager.on_event)
    
    notification_manager = NotificationManager()
    signal_bus.subscribe("QUEST_UPDATED", notification_manager.on_quest_updated)
    signal_bus.subscribe("QUEST_COMPLETED", notification_manager.on_quest_completed)

    # --- 3. World & Orchestration ---
    orchestrator = WorldOrchestrator(registry, global_state)
    world = orchestrator.load_map("data/maps/starting_village.json")
    if not world:
        # Fallback if map file is missing
        world = World([[1]*25] + [[1]+[0]*23+[1]]*18 + [[1]*25])
        
    # --- 4. Context & Director ---
    context = GameContext(player, world)
    context.global_state = global_state
    context.save_manager = save_manager
    context.orchestrator = orchestrator
    context.screen = screen
    context.signal_bus = signal_bus
    context.quest_manager = quest_manager
    context.notification_manager = notification_manager
    
    api = MapAPI(context)
    director = DirectorEngine(context, api)
    context.director = director
    quest_manager.director = director
    
    manager = SceneManager(context)
    context.scene_manager = manager
    
    # --- 5. Initial Scene ---
    # We find an NPC to pass to ExplorationScene (compatibility)
    # This will be refactored further in the future
    initial_npc = world.get_interactable_at(12, 9)
    manager.push(ExplorationScene(manager, initial_npc, None))
    
    # --- 6. Game Loop ---
    while context.running:
        dt = clock.tick(60) / 1000.0
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                context.running = False
            manager.handle_event(event)
        
        # Update
        manager.update(dt)
        director.update(dt)
        
        # Draw
        screen.fill((30, 30, 30))
        manager.draw(screen)
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
