import pygame
import sys
import os

from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World
from src.models.persistence import SaveManager
from src.ui.scenes import GameContext, SceneManager
from src.ui.title_scene import TitleScene
from src.core.registry import EntityRegistry
from src.core.orchestrator import WorldOrchestrator
from src.core.state import GlobalState
from src.core.signals import SignalBus
from src.core.audio import SoundManager
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
    save_manager = SaveManager("savegame")
    signal_bus = SignalBus()
    audio = SoundManager("data/audio_config.json")
    signal_bus.subscribe_all(audio.on_signal)
    
    # Try to load audio settings from last save (slot 0)
    last_save = save_manager.load_game(0)
    if last_save and 'audio' in last_save:
        for group, vol in last_save['audio'].items():
            audio.set_volume(group, vol)
    
    # --- 2. Minimal State Init for Title Screen ---
    global_state = GlobalState()
    # Dummy player and world for context initialization
    player = Character("Herói", Warrior())
    world = World([[1]*10]*10) # Minimal dummy world
    
    quest_manager = QuestManager(global_state, signal_bus)
    quest_manager.load_quests("data/quests.json")
    signal_bus.subscribe_all(quest_manager.on_event)
    
    notification_manager = NotificationManager()
    signal_bus.subscribe("QUEST_UPDATED", notification_manager.on_quest_updated)
    signal_bus.subscribe("QUEST_COMPLETED", notification_manager.on_quest_completed)

    # --- 3. World & Orchestration ---
    orchestrator = WorldOrchestrator(registry, global_state)
        
    # --- 4. Context & Director ---
    context = GameContext(player, world)
    context.global_state = global_state
    context.save_manager = save_manager
    context.orchestrator = orchestrator
    context.screen = screen
    context.signal_bus = signal_bus
    context.quest_manager = quest_manager
    context.notification_manager = notification_manager
    context.audio = audio
    context.play_time = 0.0
    
    api = MapAPI(context)
    director = DirectorEngine(context, api)
    context.director = director
    quest_manager.director = director
    quest_manager.game_context = context
    
    manager = SceneManager(context)
    context.scene_manager = manager
    
    # --- 5. Initial Scene: Title Screen ---
    manager.push(TitleScene(manager))
    
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
        
        # Only advance time and director logic if in Exploration (in-game)
        from src.ui.exploration_scene import ExplorationScene
        if isinstance(manager.active_scene, ExplorationScene):
            context.play_time += dt
            director.update(dt)
        
        # Draw
        screen.fill((0, 0, 0))
        manager.draw(screen)
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
