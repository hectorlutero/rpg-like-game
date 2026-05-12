import pygame
from src.ui.scenes import Scene
from src.models.dialogue import DialogueManager
from src.models.combat import CombatManager
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import Position

class ExplorationScene(Scene):
    def __init__(self, manager, npc, enemy_pos):
        self.manager = manager
        self.context = manager.context
        self.npc = npc
        self.enemy_pos = enemy_pos
        self.active_dialogue = None
        self.active_speaker = "Mundo"
        self.selected_choice_index = 0
        self.player_speed = 4

    def handle_event(self, event):
        # Only process events if this is the active scene
        if self.manager.active_scene != self:
            return

        if event.type == pygame.KEYDOWN:
            if self.active_dialogue:
                choices = self.active_dialogue.get_current_choices()
                if choices:
                    choice_list = list(choices.keys())
                    if event.key == pygame.K_UP: self.selected_choice_index = (self.selected_choice_index - 1) % len(choice_list)
                    elif event.key == pygame.K_DOWN: self.selected_choice_index = (self.selected_choice_index + 1) % len(choice_list)
                    elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        self.active_dialogue.make_choice(choice_list[self.selected_choice_index])
                        self.selected_choice_index = 0
                else:
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        self.active_dialogue.next_line()
                        if self.active_dialogue.is_finished(): self.active_dialogue = None
            else:
                if event.key in [pygame.K_e, pygame.K_SPACE]:
                    # Nova lógica direcional baseada em tiles
                    tx = int(self.context.player.position.x // self.context.world.tile_size)
                    ty = int(self.context.player.position.y // self.context.world.tile_size)
                    
                    if self.context.player.facing_direction == "N": ty -= 1
                    elif self.context.player.facing_direction == "S": ty += 1
                    elif self.context.player.facing_direction == "W": tx -= 1
                    elif self.context.player.facing_direction == "E": tx += 1
                    
                    target = self.context.world.get_interactable_at(tx, ty)
                    if target:
                        # Define quem está falando (NPC tem nome, Baú/Livro usa Mundo)
                        self.active_speaker = target.name if hasattr(target, 'name') else "Mundo"
                        
                        result = target.on_interact(self.context)
                        
                        # Se for uma string (feedback), mostramos como um diálogo simples
                        if isinstance(result, str):
                            self.active_dialogue = DialogueManager([result])
                        
                        # Se o resultado for um DialogueManager, ativamos o diálogo
                        elif isinstance(result, DialogueManager):
                            self.active_dialogue = result
                        
                        # Se for uma cena (combate), fazemos o push
                        elif isinstance(result, Scene):
                            self.manager.push(result)
                
                # Save/Load/Rest
                if event.key == pygame.K_k: # K for Keep (Save)
                    if self.context.save_manager.save_game(self.context):
                        print("Jogo Salvo com Sucesso!")
                
                elif event.key == pygame.K_r: # R for Rest
                    self.context.player.rest()
                    print("Você descansou. HP, Mana e Energia restaurados!")

                elif event.key == pygame.K_l: # L for Load
                    save_data = self.context.save_manager.load_game()
                    if save_data:
                        self.context.player.position.x = save_data['position']['x']
                        self.context.player.position.y = save_data['position']['y']
                        self.context.player.hp = save_data['hp']
                        self.context.player.xp = save_data['xp']
                        self.context.player.energy = save_data.get('energy', 3)
                        self.context.player.skills = set(save_data.get('skills', []))
                        print("Jogo Carregado!")
                elif event.key in [pygame.K_m, pygame.K_TAB]:
                    from src.ui.menu_scene import MenuScene
                    self.manager.push(MenuScene(self.manager))

    def update(self, dt):
        # Only process movement if this is the active scene
        if self.manager.active_scene != self:
            return

        if not self.active_dialogue:
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -self.player_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = self.player_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -self.player_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = self.player_speed
            
            if dx != 0 or dy != 0:
                if self.context.world.can_move_to(self.context.player, self.context.player.position.x + dx, self.context.player.position.y + dy):
                    self.context.player.position.move(dx, dy)
                    self.context.player.update_orientation(dx, dy)

    def draw(self, screen):
        # Draw Map
        for y, row in enumerate(self.context.world.grid):
            for x, tile in enumerate(row):
                if tile == 1: pygame.draw.rect(screen, (100, 100, 100), (x*32, y*32, 32, 32))
                else: pygame.draw.rect(screen, (50, 50, 50), (x*32, y*32, 32, 32), 1)
        
        # Draw all interactables in the world (simple visualization)
        for (tx, ty), obj in self.context.world.interactables.items():
            from src.models.interaction import MagicBook, TrainingObject, Chest
            from src.models.combat import EnemyInteractable
            from src.ui.shop_scene import Shopkeeper
            
            x_pos, y_pos = tx * 32, ty * 32

            if isinstance(obj, EnemyInteractable):
                # Inimigos são quadrados vermelhos
                pygame.draw.rect(screen, (200, 50, 50), (x_pos, y_pos, 32, 32))
                # Detalhe para diferenciar (olhos pequenos)
                pygame.draw.rect(screen, (255, 255, 255), (x_pos + 6, y_pos + 10, 4, 4))
                pygame.draw.rect(screen, (255, 255, 255), (x_pos + 22, y_pos + 10, 4, 4))
            
            elif isinstance(obj, MagicBook):
                pygame.draw.rect(screen, (150, 50, 255), (x_pos + 8, y_pos + 8, 16, 16))
            elif isinstance(obj, TrainingObject):
                pygame.draw.rect(screen, (150, 100, 50), (x_pos + 4, y_pos + 4, 24, 24))
            elif isinstance(obj, Chest):
                # Sincroniza estado com o contexto antes de desenhar
                is_open = obj.check_open(self.context)
                color = (255, 200, 0) if not is_open else (80, 40, 0)
                pygame.draw.rect(screen, color, (x_pos + 6, y_pos + 6, 20, 20))
                if not is_open:
                    pygame.draw.rect(screen, (0, 0, 0), (x_pos + 6, y_pos + 14, 20, 2), 1)
            elif isinstance(obj, Shopkeeper):
                pygame.draw.rect(screen, (180, 180, 50), (x_pos + 4, y_pos + 4, 24, 24))
                pygame.draw.rect(screen, (255, 255, 255), (x_pos + 10, y_pos + 8, 4, 4)) # Olhos
                pygame.draw.rect(screen, (255, 255, 255), (x_pos + 18, y_pos + 8, 4, 4))
            
            from src.models.dialogue import NPC
            if isinstance(obj, NPC):
                # NPCs são quadrados verdes
                pygame.draw.rect(screen, (50, 200, 50), (x_pos, y_pos, 32, 32))

        # Player (Blue Square)
        px, py = self.context.player.position.x, self.context.player.position.y
        pygame.draw.rect(screen, (0, 100, 255), (px - 16, py - 16, 32, 32))
        
        # Direction Indicator (Small yellow dot/line)
        indicator_color = (255, 255, 0)
        if self.context.player.facing_direction == "N":
            pygame.draw.rect(screen, indicator_color, (px - 4, py - 16, 8, 4))
        elif self.context.player.facing_direction == "S":
            pygame.draw.rect(screen, indicator_color, (px - 4, py + 12, 8, 4))
        elif self.context.player.facing_direction == "W":
            pygame.draw.rect(screen, indicator_color, (px - 16, py - 4, 4, 8))
        elif self.context.player.facing_direction == "E":
            pygame.draw.rect(screen, indicator_color, (px + 12, py - 4, 4, 8))
        
        # Draw Dialogue
        if self.active_dialogue:
            pygame.draw.rect(screen, (0, 0, 0), (50, 400, 700, 150))
            pygame.draw.rect(screen, (255, 255, 255), (50, 400, 700, 150), 2)
            
            # Speaker
            self._draw_text(screen, self.active_speaker + ":", 70, 415, size=20, color=(200, 200, 50), align="left")
            
            # Texto com suporte a quebra de linha (\n)
            text_lines = self.active_dialogue.get_current_line().split("\n")
            for i, line in enumerate(text_lines):
                self._draw_text(screen, line, 70, 445 + (i * 25), size=20, align="left")
            
            # Choices
            choices = self.active_dialogue.get_current_choices()
            if choices:
                for i, choice_text in enumerate(choices.keys()):
                    color = (255, 255, 0) if i == self.selected_choice_index else (200, 200, 200)
                    # Desloca choices para baixo se houver múltiplas linhas de texto
                    y_pos = 480 + (len(text_lines)-1)*20 + (i * 25)
                    self._draw_text(screen, f"> {choice_text}", 100, y_pos, size=18, color=color, align="left")

        # UI Overlay (Energy)
        self._draw_text(screen, f"Energia: {self.context.player.energy}/3", 20, 20, size=20, color=(255, 255, 0), align="left")
