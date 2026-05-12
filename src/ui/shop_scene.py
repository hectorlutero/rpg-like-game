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
        self.state = "BUY" # BUY or SELL
        self.message = f"Bem-vindo à loja de {shop_name}!"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                self.manager.pop()
            elif event.key == pygame.K_UP: self.selector.prev()
            elif event.key == pygame.K_DOWN: self.selector.next()
            elif event.key == pygame.K_TAB:
                self._toggle_mode()
            elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                if self.state == "BUY":
                    self._buy_item()
                else:
                    self._sell_item()

    def _toggle_mode(self):
        if self.state == "BUY":
            self.state = "SELL"
            # In SELL mode, items are what the player has (unique items)
            player_items = sorted(list(set(self.context.player.inventory.items)))
            self.selector = SelectionManager(player_items)
            self.message = "O que deseja vender? (50% do valor)"
        else:
            self.state = "BUY"
            self.selector = SelectionManager(self.items)
            self.message = "O que deseja comprar?"

    def _get_item_data(self, name):
        from src.models.items import EQUIPMENT_DATA, CONSUMABLE_DATA
        return EQUIPMENT_DATA.get(name) or CONSUMABLE_DATA.get(name)

    def _buy_item(self):
        item_name = self.selector.current_item
        item = self._get_item_data(item_name)
        
        if not item:
            self.message = "Item não encontrado."
            return

        if self.context.player.gold >= item.price:
            self.context.player.gold -= item.price
            self.context.player.inventory.add_item(item_name)
            self.message = f"Comprou {item_name} por {item.price} G!"
        else:
            self.message = "Ouro insuficiente!"

    def _sell_item(self):
        item_name = self.selector.current_item
        if not item_name: return

        item = self._get_item_data(item_name)
        if not item: return

        sell_price = item.price // 2
        self.context.player.gold += sell_price
        self.context.player.inventory.remove_item(item_name)
        
        # Refresh selector
        player_items = sorted(list(set(self.context.player.inventory.items)))
        self.selector = SelectionManager(player_items)
        self.message = f"Vendeu {item_name} por {sell_price} G!"

    def update(self, dt):
        pass

    def draw(self, screen):
        # Overlay
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(240)
        overlay.fill((30, 20, 10))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (215, 180, 50), (100, 50, 600, 500), 3)
        title = f"LOJA: {self.shop_name} ({self.state})"
        self._draw_text(screen, title, 400, 80, size=32, color=(255, 215, 0))
        self._draw_text(screen, f"Seu Ouro: {self.context.player.gold} G", 400, 120, color=(255, 255, 255))
        
        # Lista de Itens
        y_item = 180
        current_options = self.selector.options
        for i, name in enumerate(current_options):
            item = self._get_item_data(name)
            color = (255, 255, 0) if i == self.selector.index else (200, 200, 200)
            prefix = "> " if i == self.selector.index else "  "
            
            if self.state == "BUY":
                price_str = f"{item.price} G" if item else "???"
            else:
                price_str = f"{item.price // 2} G" if item else "???"
            
            self._draw_text(screen, f"{prefix}{name}", 150, y_item, color=color, align="left")
            self._draw_text(screen, price_str, 550, y_item, color=color, align="right")
            y_item += 40

        if not current_options and self.state == "SELL":
            self._draw_text(screen, "Você não tem itens para vender.", 400, 300, color=(150, 150, 150))

        # Feedback
        pygame.draw.rect(screen, (0, 0, 0), (120, 450, 560, 60))
        self._draw_text(screen, self.message, 400, 480, size=18, color=(200, 200, 200), align="center")
        self._draw_text(screen, "TAB: Mudar Modo | ESPAÇO: Confirmar | ESC: Sair", 400, 530, size=16, color=(150, 150, 150), align="center")
