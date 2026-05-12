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

    # --- Setup Context and Manager ---
    player = None # placeholder
    if save_data:
        char_class = save_manager.class_map.get(save_data['class'], Warrior)()
        player = Character(save_data['name'], char_class, level=save_data['level'])
        player.hp = save_data['hp']
        player.xp = save_data['xp']
        player.energy = save_data.get('energy', 3)
        player.gold = save_data.get('gold', 0)
        player.skills = set(save_data.get('skills', []))
        player.inventory.items = save_data.get('inventory', [])
        
        # Carrega Equipamentos
        from src.models.items import EQUIPMENT_DATA
        eq_data = save_data.get('equipment', {})
        for slot, item_name in eq_data.items():
            if item_name in EQUIPMENT_DATA:
                player.equipment[slot] = EQUIPMENT_DATA[item_name]

        player.position.x = save_data['position']['x']
        player.position.y = save_data['position']['y']
        print(f"Jogo carregado: {player.name}")
    else:
        player = Character("Herói", Warrior())
        player.position.x, player.position.y = 64, 64
        # Teste inicial
        from src.models.items import EQUIPMENT_DATA
        player.gold = 50
        player.equip_item(EQUIPMENT_DATA["Espada de Ferro"])

    context = GameContext(player, world)
    context.save_manager = save_manager
    context.screen = screen
    
    # Restaura estado do mundo
    if save_data:
        context.opened_chests = set(save_data.get('opened_chests', []))

    manager = SceneManager(context)
    context.scene_manager = manager
    
    # Define NPCs e Inimigos
    npc = NPC("Guarda", Position(400, 300), {
        0: {"text": "Olá! Sistema de interação direcional ativado.", "choices": {"Incrível": 1, "Top": 1}},
        1: {"text": "Agora você só fala comigo se estiver de frente!", "choices": None}
    })
    world.add_interactable(400 // 32, 300 // 32, npc)

    from src.models.combat import EnemyInteractable
    enemy_pos = Position(200, 400)
    # Slime agora dá 30 de Ouro e 150 de XP
    enemy_trigger = EnemyInteractable("Slime", Warrior(), 1, enemy_pos, gold_yield=30, xp_yield=150)
    world.add_interactable(200 // 32, 400 // 32, enemy_trigger)

    # TESTE STATUS: Verme Tóxico (Veneno)
    tox_pos = Position(300, 400)
    toxic_worm = EnemyInteractable("Verme Tóxico", Warrior(), 2, tox_pos, gold_yield=50, xp_yield=200)
    # Adicionamos a habilidade de veneno ao inimigo manualmente para o teste
    # No futuro isso pode vir de um registro de inimigos
    def setup_toxic_worm(context):
        from src.ui.combat_scene import CombatScene
        from src.models.character import Character
        from src.models.combat import CombatManager
        enemy = Character("Verme Tóxico", Warrior(), level=2)
        enemy.skills.add("Picada Venenosa")
        cm = CombatManager(context.party, [enemy], gold_reward=50, xp_reward=200)
        return CombatScene(context.scene_manager, cm, tox_pos)
    toxic_worm.on_interact = setup_toxic_worm
    world.add_interactable(300 // 32, 400 // 32, toxic_worm)

    # TESTE STATUS: Eletroslime (Paralisia)
    elec_pos = Position(400, 400)
    elec_slime = EnemyInteractable("Eletroslime", Warrior(), 2, elec_pos, gold_yield=50, xp_yield=200)
    def setup_elec_slime(context):
        from src.ui.combat_scene import CombatScene
        from src.models.character import Character
        from src.models.combat import CombatManager
        enemy = Character("Eletroslime", Warrior(), level=2)
        enemy.skills.add("Faísca Paralisante")
        cm = CombatManager(context.party, [enemy], gold_reward=50, xp_reward=200)
        return CombatScene(context.scene_manager, cm, elec_pos)
    elec_slime.on_interact = setup_elec_slime
    world.add_interactable(400 // 32, 400 // 32, elec_slime)

    # NOVO: Mercador
    from src.ui.shop_scene import Shopkeeper
    merchant = Shopkeeper("Mercador Errante", ["Espada de Ferro", "Armadura de Couro", "Anel de Inteligência", "Poção de Vida", "Antídoto"])
    # Coloca o mercador no tile (8, 10)
    world.add_interactable(8, 10, merchant)

    # Livros e Objetos de Treino
    from src.models.interaction import MagicBook, TrainingObject, Chest
    from src.models.items import EQUIPMENT_DATA
    
    fireball_book = MagicBook("Bola de Fogo", int_threshold=10, min_level=1)
    world.add_interactable(150 // 32, 100 // 32, fireball_book)

    fast_cut_book = MagicBook("Corte Rápido", int_threshold=5, min_level=1)
    world.add_interactable(100 // 32, 200 // 32, fast_cut_book)

    poison_book = MagicBook("Picada Venenosa", int_threshold=0, min_level=1)
    world.add_interactable(50 // 32, 200 // 32, poison_book)

    dummy = TrainingObject("Boneco de Treino", "forca")
    world.add_interactable(300 // 32, 100 // 32, dummy)

    # NOVO: Baú de Tesouro
    chest = Chest(item=EQUIPMENT_DATA["Escudo de Madeira"], gold=100, chest_id="spawn_chest_1")
    if "spawn_chest_1" in context.opened_chests:
        chest.is_open = True
    world.add_interactable(500 // 32, 100 // 32, chest)

    # Baú de Teste de Status
    status_chest = Chest(item=EQUIPMENT_DATA["Anel de Resistência"], gold=0, chest_id="status_test_chest")
    if "status_test_chest" in context.opened_chests:
        status_chest.is_open = True
    world.add_interactable(550 // 32, 100 // 32, status_chest)

    # NOVO: Baú de Poções para Teste
    def setup_potion_chest(context):
        from src.models.dialogue import DialogueManager
        if "potion_test_chest" not in context.opened_chests:
            context.player.inventory.add_item("Poção de Vida")
            context.player.inventory.add_item("Poção de Mana")
            context.player.inventory.add_item("Antídoto")
            context.opened_chests.add("potion_test_chest")
            return "Você encontrou Poções de Vida, Mana e Antídoto!"
        return "O baú já foi saqueado."
    
    potion_chest = Chest(item=None, gold=0, chest_id="potion_test_chest")
    potion_chest.on_interact = setup_potion_chest
    world.add_interactable(600 // 32, 100 // 32, potion_chest)
    
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
