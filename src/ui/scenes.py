from src.core.state import GlobalState

class GameContext:
    """O Estado Global do jogo. Contém os dados que persistem entre cenas."""
    def __init__(self, player, world):
        self.player = player
        self.world = world
        self.party = [player]
        self.save_manager = None # Será injetado no main
        self.running = True
        self.global_state = GlobalState()
        
    @property
    def opened_chests(self):
        """Backward compatibility for opened_chests."""
        # This is a bit tricky because the old code expects a set of IDs.
        # We can scan deltas for _is_open=True
        ids = set()
        for eid, delta in self.global_state.deltas.items():
            if delta.get("_is_open"):
                ids.add(eid)
        return ids

    @opened_chests.setter
    def opened_chests(self, value):
        """Allows setting opened chests via a collection of IDs."""
        for cid in value:
            self.global_state.set_entity_delta(cid, {"_is_open": True})

class Scene:
    """Interface base para todas as cenas do jogo."""
    def handle_event(self, event):
        pass
    
    def update(self, dt):
        pass
    
    def draw(self, screen):
        pass

    def _draw_text(self, screen, text, x, y, size=24, color=(255, 255, 255), align="center"):
        import pygame
        font = pygame.font.SysFont("Arial", size)
        surf = font.render(text, True, color)
        rect = surf.get_rect()
        if align == "center": rect.center = (x, y)
        elif align == "left": rect.midleft = (x, y)
        elif align == "right": rect.midright = (x, y)
        else: rect.topleft = (x, y)
        screen.blit(surf, rect)

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
