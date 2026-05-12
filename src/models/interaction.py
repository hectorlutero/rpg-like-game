class Interactable:
    """Interface base para qualquer objeto que possa ser ativado pelo Herói."""
    def on_interact(self, context):
        """
        Executa a ação de interação.
        :param context: GameContext do jogo para acesso a herói, cenas, etc.
        """
        raise NotImplementedError("Subclasses de Interactable devem implementar on_interact")

class MagicBook(Interactable):
    def __init__(self, skill_name, int_threshold, min_level=1):
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

class TrainingObject(Interactable):
    def __init__(self, name, attribute_key):
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
