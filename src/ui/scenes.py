class GameContext:
    """O Estado Global do jogo. Contém os dados que persistem entre cenas."""
    def __init__(self, player, world):
        self.player = player
        self.world = world
        self.party = [player]
        self.save_manager = None # Será injetado no main
        self.running = True

class Scene:
    """Interface base para todas as cenas do jogo."""
    def handle_event(self, event):
        pass
    
    def update(self, dt):
        pass
    
    def draw(self, screen):
        pass

class SceneManager:
    """Gerencia a pilha (stack) de cenas."""
    def __init__(self, context):
        self.context = context
        self.stack = []

    def push(self, scene):
        """Adiciona uma nova cena ao topo da pilha."""
        self.stack.append(scene)

    def pop(self):
        """Remove a cena do topo."""
        if self.stack:
            return self.stack.pop()
        return None

    def change_scene(self, scene):
        """Substitui a cena atual (limpa a pilha)."""
        self.stack = [scene]

    @property
    def active_scene(self):
        return self.stack[-1] if self.stack else None

    def handle_event(self, event):
        if self.active_scene:
            self.active_scene.handle_event(event)

    def update(self, dt):
        if self.active_scene:
            self.active_scene.update(dt)

    def draw(self, screen):
        # Desenha todas as cenas na pilha (de baixo para cima)
        # Isso permite que menus sobreponham o mapa
        for scene in self.stack:
            scene.draw(screen)
