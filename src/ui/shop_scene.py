import pygame
from src.ui.scenes import Scene
from src.models.interaction import SelectionManager, Interactable

class Shopkeeper(Interactable):
    def __init__(self, name, inventory_items):
        self.name = name
        self.inventory_items = inventory_items # List of item names

    def on_interact(self, context):
        return ShopScene(context.scene_manager, self.name, self.inventory_items)

class ShopScene(Scene):
    def __init__(self, manager, shop_name, items):
        self.manager = manager
        self.context = manager.context
        self.shop_name = shop_name
        self.items = items
        self.selector = SelectionManager(items)
        self.message = f"Bem-vindo à loja de {shop_name}!"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                self.manager.pop()
            elif event.key == pygame.K_UP: self.selector.prev()
            elif event.key == pygame.K_DOWN: self.selector.next()
            elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                self._buy_item()

    def _buy_item(self):
        from src.models.items import EQUIPMENT_DATA
        item_name = self.selector.current_item
        item = EQUIPMENT_DATA.get(item_name)
        
        if not item:
            self.message = "Item não encontrado."
            return

        if self.context.player.gold >= item.price:
            self.context.player.gold -= item.price
            self.context.player.inventory.add_item(item_name)
            self.message = f"Comprou {item_name} por {item.price} G!"
        else:
            self.message = "Ouro insuficiente!"

    def update(self, dt):
        pass

    def draw(self, screen):
        # Overlay
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(240)
        overlay.fill((30, 20, 10))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (215, 180, 50), (100, 50, 600, 500), 3)
        self._draw_text(screen, f"LOJA: {self.shop_name}", 400, 80, size=32, color=(255, 215, 0))
        self._draw_text(screen, f"Seu Ouro: {self.context.player.gold} G", 400, 120, color=(255, 255, 255))
        
        # Lista de Itens
        from src.models.items import EQUIPMENT_DATA
        y_item = 180
        for i, name in enumerate(self.items):
            item = EQUIPMENT_DATA.get(name)
            color = (255, 255, 0) if i == self.selector.index else (200, 200, 200)
            prefix = "> " if i == self.selector.index else "  "
            price_str = f"{item.price} G" if item else "???"
            
            self._draw_text(screen, f"{prefix}{name}", 150, y_item, color=color, align="left")
            self._draw_text(screen, price_str, 550, y_item, color=color, align="right")
            y_item += 40

        # Feedback
        pygame.draw.rect(screen, (0, 0, 0), (120, 450, 560, 60))
        self._draw_text(screen, self.message, 400, 480, size=18, color=(200, 200, 200))
        self._draw_text(screen, "ESPAÇO: Comprar | ESC: Sair", 400, 530, size=16, color=(150, 150, 150))

    def _draw_text(self, screen, text, x, y, size=24, color=(255, 255, 255), align="center"):
        font = pygame.font.SysFont("Arial", size)
        surf = font.render(text, True, color)
        rect = surf.get_rect()
        if align == "center": rect.center = (x, y)
        elif align == "left": rect.midleft = (x, y)
        elif align == "right": rect.midright = (x, y)
        screen.blit(surf, rect)
