import pygame
import sys
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World, Position
from src.models.dialogue import NPC
from src.models.persistence import SaveManager
from src.ui.scenes import GameContext, SceneManager
from src.ui.exploration_scene import ExplorationScene

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("RPG Classic - Refactored")
    clock = pygame.time.Clock()
    
    # --- Data Init ---
    map_grid = [[0 for _ in range(25)] for _ in range(20)]
    for i in range(25): map_grid[0][i] = map_grid[19][i] = 1
    for i in range(20): map_grid[i][0] = map_grid[i][24] = 1
    world = World(map_grid, tile_size=32)
    
    save_manager = SaveManager("savegame.json")
    save_data = save_manager.load_game()

    if save_data:
        # Simplificando reconstrução para o refactor
        char_class = save_manager.class_map.get(save_data['class'], Warrior)()
        player = Character(save_data['name'], char_class, level=save_data['level'])
        player.hp = save_data['hp']
        player.xp = save_data['xp']
        player.energy = save_data.get('energy', 3)
        player.skills = set(save_data.get('skills', []))
        player.position.x = save_data['position']['x']
        player.position.y = save_data['position']['y']
        print(f"Jogo carregado: {player.name}")
    else:
        player = Character("Herói", Warrior())
        player.position.x, player.position.y = 64, 64

    # --- Setup Context and Manager ---
    context = GameContext(player, world)
    context.save_manager = save_manager
    context.screen = screen # Para facilitar acesso na UI
    
    manager = SceneManager(context)
    context.scene_manager = manager # Para que interactables possam fazer push de cenas
    
    # Define NPCs e Inimigos iniciais registrados no MUNDO
    npc = NPC("Guarda", Position(400, 300), {
        0: {"text": "Olá! Sistema de interação direcional ativado.", "choices": {"Incrível": 1, "Top": 1}},
        1: {"text": "Agora você só fala comigo se estiver de frente!", "choices": None}
    })
    # Registra o NPC no tile correspondente (400/32 = 12.5 -> tile 12, 300/32 = 9.3 -> tile 9)
    world.add_interactable(400 // 32, 300 // 32, npc)

    from src.models.combat import EnemyInteractable
    enemy_pos = Position(200, 400)
    enemy_trigger = EnemyInteractable("Slime", Warrior(), 1, enemy_pos)
    world.add_interactable(200 // 32, 400 // 32, enemy_trigger)

    # Livro de Magia
    from src.models.interaction import MagicBook
    fireball_book = MagicBook("Bola de Fogo", int_threshold=10, min_level=1)
    world.add_interactable(150 // 32, 100 // 32, fireball_book) # Perto do início

    # Livro de Skill Física (Corte Rápido)
    fast_cut_book = MagicBook("Corte Rápido", int_threshold=5, min_level=1)
    world.add_interactable(100 // 32, 200 // 32, fast_cut_book)

    from src.models.interaction import TrainingObject
    dummy = TrainingObject("Boneco de Treino", "forca")
    world.add_interactable(300 // 32, 100 // 32, dummy)
    
    # Inicia com a cena de exploração
    manager.push(ExplorationScene(manager, npc, enemy_pos))
    
    # --- Game Loop ---
    while context.running:
        dt = clock.tick(60) / 1000.0
        
        # 1. Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                context.running = False
            manager.handle_event(event)
        
        # 2. Update
        manager.update(dt)
        
        # 3. Draw
        screen.fill((30, 30, 30))
        manager.draw(screen)
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
