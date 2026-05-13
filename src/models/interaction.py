import pygame

class Interactable:
    """Interface base para qualquer objeto que possa ser ativado pelo Herói."""
    def on_interact(self, context):
        """
        Executa a ação de interação.
        :param context: GameContext do jogo para acesso a herói, cenas, etc.
        """
        raise NotImplementedError("Subclasses de Interactable devem implementar on_interact")

    def draw(self, screen, context, pos):
        """
        Desenha o objeto no mapa.
        :param screen: Superfície do Pygame.
        :param context: GameContext (pode ser necessário para estado).
        :param pos: Tupla (x, y) em pixels.
        """
        # Default fallback: um quadrado cinza
        pygame.draw.rect(screen, (150, 150, 150), (pos[0], pos[1], 32, 32))

class TransitionRequest:
    """Dados para solicitar uma troca de mapa."""
    def __init__(self, target_map, target_tag):
        self.target_map = target_map
        self.target_tag = target_tag


class MagicBook(Interactable):
    def __init__(self, skill_name, int_threshold, min_level=1, **kwargs):
        self.skill_name = skill_name
        self.int_threshold = int_threshold
        self.min_level = min_level

    def on_interact(self, context):
        player = context.player
        
        # Se já aprendeu, não faz nada
        if self.skill_name in player.skills:
            return "Você já dominou este conhecimento."

        # Requisito de Energia
        if player.energy <= 0:
            return "Você está exausto demais para estudar."

        current_int = player.get_attribute('inteligencia')

        # Se atingiu o threshold e nível, aprende
        if current_int >= self.int_threshold:
            if player.level >= self.min_level:
                player.skills.add(self.skill_name)
                player.energy -= 1
                return f"Você aprendeu a magia {self.skill_name}!"
            else:
                return f"Seu nível é baixo demais para compreender esta magia (Requer Nvl {self.min_level})."

        # Se está abaixo do threshold, ganha +1 de INT (no base_stat para persistir)
        player.base_stats['inteligencia'] += 1
        player.energy -= 1
        
        # Checa se após o ganho, aprendeu
        if player.get_attribute('inteligencia') >= self.int_threshold and player.level >= self.min_level:
            player.skills.add(self.skill_name)
            return f"Sua compreensão aumentou e você aprendeu {self.skill_name}!"
        
        return f"Sua inteligência aumentou ao estudar {self.skill_name}."

    def draw(self, screen, context, pos):
        pygame.draw.rect(screen, (150, 50, 255), (pos[0] + 8, pos[1] + 8, 16, 16))

class TrainingObject(Interactable):
    def __init__(self, name, attribute_key, **kwargs):
        self.name = name
        self.attribute_key = attribute_key

    def on_interact(self, context):
        player = context.player
        if player.energy <= 0:
            return "Você está exausto demais para treinar."
        
        player.base_stats[self.attribute_key] += 1
        player.energy -= 1
        
        # Nome amigável para o feedback
        attr_display = self.attribute_key.capitalize()
        if self.attribute_key == "forca": attr_display = "Força"
        elif self.attribute_key == "inteligencia": attr_display = "Inteligência"
        
        return f"Seu treino de {self.name} foi produtivo! Sua {attr_display} aumentou."

    def draw(self, screen, context, pos):
        pygame.draw.rect(screen, (150, 100, 50), (pos[0] + 4, pos[1] + 4, 24, 24))

class Chest(Interactable):
    def __init__(self, items=None, gold=0, chest_id=None, custom_msg=None, **kwargs):
        self.items = items or [] # List of Item names or objects
        self.gold = gold
        self.chest_id = chest_id # Essential for persistence
        self.custom_msg = custom_msg
        self._is_open = kwargs.get("_is_open", False)

    @property
    def is_open(self):
        return self._is_open

    def check_open(self, context):
        """Checks if the chest is open, syncing with context if needed."""
        if self._is_open:
            return True
        if context and self.chest_id in context.opened_chests:
            self._is_open = True
            return True
        return False

    def on_interact(self, context):
        if self.check_open(context):
            return "O baú está vazio."
        
        player = context.player
        self._is_open = True
        
        # Track in context for persistence
        if self.chest_id:
            context.global_state.set_entity_delta(self.chest_id, {"_is_open": True, "gold": 0, "items": []})

        msg = self.custom_msg or "Você abriu o baú!"
        if self.gold > 0:
            player.gold += self.gold
            msg += f"\nGanhou {self.gold} G!"
        
        for item in self.items:
            # item can be a string (name) or an object with a .name attribute
            item_name = item if isinstance(item, str) else item.name
            player.receive_item(item_name, context.signal_bus)
            msg += f"\nEncontrou {item_name}!"
            
        return msg

    def draw(self, screen, context, pos):
        is_open = self.check_open(context)
        color = (255, 200, 0) if not is_open else (80, 40, 0)
        pygame.draw.rect(screen, color, (pos[0] + 6, pos[1] + 6, 20, 20))
        if not is_open:
            pygame.draw.rect(screen, (0, 0, 0), (pos[0] + 6, pos[1] + 14, 20, 2), 1)


class Portal(Interactable):
    def __init__(self, target_map, target_tag, require_interaction=False, **kwargs):
        self.target_map = target_map
        self.target_tag = target_tag
        self.require_interaction = require_interaction
        self.name = kwargs.get("name", "Portal")

    def on_interact(self, context):
        """Triggers the transition request."""
        return TransitionRequest(self.target_map, self.target_tag)

    def draw(self, screen, context, pos):
        # Draw a blue outline for debugging/visibility in development
        pygame.draw.rect(screen, (0, 100, 255), (pos[0] + 4, pos[1] + 4, 24, 24), 2)


class SelectionManager:
    """Gerenciador universal de navegação em listas (menus, combate, etc)."""
    def __init__(self, options=None):
        self.options = options or []
        self.index = 0

    def set_options(self, options):
        """Define novas opções e reseta o índice."""
        self.options = options
        self.index = 0

    def next(self):
        """Move para o próximo item (com wrap-around)."""
        if not self.options: return
        self.index = (self.index + 1) % len(self.options)

    def prev(self):
        """Move para o item anterior (com wrap-around)."""
        if not self.options: return
        self.index = (self.index - 1) % len(self.options)

    @property
    def current_item(self):
        """Retorna o item selecionado no momento."""
        if 0 <= self.index < len(self.options):
            return self.options[self.index]
        return None


class InteractionManager:
    """Orquestrador de lógica de interação (Deep Module)."""
    def __init__(self, context, scene_manager):
        self.context = context
        self.scene_manager = scene_manager
        self.active_dialogue = None
        self.active_speaker = "Mundo"
        self.selected_index = 0
        self.requested_transition = None

    @property
    def is_active(self):
        return self.active_dialogue is not None

    def interact(self):
        player = self.context.player
        world = self.context.world
        
        tx = int(player.position.x // world.tile_size)
        ty = int(player.position.y // world.tile_size)
        
        if player.facing_direction == "N": ty -= 1
        elif player.facing_direction == "S": ty += 1
        elif player.facing_direction == "W": tx -= 1
        elif player.facing_direction == "E": tx += 1
        
        target = world.get_interactable_at(tx, ty)
        if target:
            self.active_speaker = target.name if hasattr(target, 'name') else "Mundo"
            
            # Signal the interaction
            if self.context.signal_bus:
                self.context.signal_bus.emit("INTERACT", target=self.active_speaker)

            result = target.on_interact(self.context)
            
            from src.models.dialogue import DialogueManager
            from src.ui.scenes import Scene
            
            if isinstance(result, str):
                self.active_dialogue = DialogueManager([result])
            elif isinstance(result, DialogueManager):
                self.active_dialogue = result
            elif isinstance(result, Scene):
                self.scene_manager.push(result)
            elif isinstance(result, TransitionRequest):
                self.requested_transition = result
            
            self.selected_index = 0

    def handle_event(self, event):
        if not self.active_dialogue:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: self.process_command("up")
            elif event.key == pygame.K_DOWN: self.process_command("down")
            elif event.key in [pygame.K_SPACE, pygame.K_RETURN]: self.process_command("space")

    def process_command(self, cmd):
        if not self.active_dialogue:
            return

        choices = self.active_dialogue.get_current_choices()
        if choices:
            choice_list = list(choices.keys())
            if cmd == "up":
                self.selected_index = (self.selected_index - 1) % len(choice_list)
            elif cmd == "down":
                self.selected_index = (self.selected_index + 1) % len(choice_list)
            elif cmd in ["confirm", "space"]:
                self.active_dialogue.make_choice(choice_list[self.selected_index])
                self.selected_index = 0
        else:
            if cmd in ["confirm", "space"]:
                self.active_dialogue.next_line()
        
        if self.active_dialogue and self.active_dialogue.is_finished():
            self.active_dialogue = None

    def get_view_model(self):
        if not self.active_dialogue:
            return None
        
        choices = self.active_dialogue.get_current_choices()
        return {
            "speaker": self.active_speaker,
            "text": self.active_dialogue.get_current_line(),
            "choices": list(choices.keys()) if choices else [],
            "selected_index": self.selected_index
        }
