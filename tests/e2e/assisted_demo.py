import pygame
import time
from src.models.character import Character
from src.models.classes import Warrior
from src.models.world import World
from src.ui.scenes import GameContext, SceneManager
from src.ui.shop_scene import ShopScene
from src.ui.menu_scene import MenuScene

class AssistedTester:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("ROBÔ RPG: Assistindo a Automação")
        self.clock = pygame.time.Clock()
        
        self.world = World([[0]*25 for _ in range(20)])
        self.player = Character("Robô_Tester", Warrior())
        self.player.gold = 200
        self.player.hp = 50
        
        self.context = GameContext(self.player, self.world)
        self.manager = SceneManager(self.context)
        
        # Sequência de comandos: (tempo_em_segundos, tecla, descrição)
        self.script = [
            (1.0, None, "Iniciando Demonstração..."),
            (2.0, pygame.K_DOWN, "Navegando na Loja (Baixo)"),
            (2.5, pygame.K_DOWN, "Navegando na Loja (Baixo)"),
            (3.5, pygame.K_SPACE, "Comprando Poção de Vida"),
            (4.5, pygame.K_TAB, "Alternando para modo VENDA"),
            (5.5, pygame.K_SPACE, "Vendendo a Poção"),
            (6.5, pygame.K_TAB, "Voltando para modo COMPRA"),
            (7.5, pygame.K_ESCAPE, "Saindo da Loja"),
            (8.5, None, "Abrindo Menu de Inventário"),
            # Note: We'll push MenuScene in code below
            (9.5, pygame.K_RIGHT, "Mudando para Aba de Inventário"),
            (10.5, pygame.K_DOWN, "Selecionando Item"),
            (11.5, pygame.K_SPACE, "Usando Item"),
            (13.0, None, "Demo Finalizada!")
        ]
        self.start_time = time.time()
        self.script_index = 0

    def run(self):
        # Inicia na Loja
        shop_items = ["Espada de Ferro", "Armadura de Couro", "Poção de Vida"]
        self.manager.push(ShopScene(self.manager, "Mercador do Futuro", shop_items))
        
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            elapsed = time.time() - self.start_time
            
            # Processa Script
            if self.script_index < len(self.script):
                target_time, key, desc = self.script[self.script_index]
                if elapsed >= target_time:
                    print(f"[ROBÔ]: {desc}")
                    if key:
                        event = pygame.event.Event(pygame.KEYDOWN, {'key': key})
                        self.manager.handle_event(event)
                    
                    # Lógica especial para trocar de cena no meio do script
                    if desc == "Abrindo Menu de Inventário":
                        self.manager.push(MenuScene(self.manager))
                    
                    self.script_index += 1

            # Eventos Manuais (para fechar)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    running = False

            self.manager.update(dt)
            self.screen.fill((20, 20, 20))
            self.manager.draw(self.screen)
            
            # Overlay de status do Robô
            font = pygame.font.SysFont("Arial", 18)
            status_text = f"AÇÃO ATUAL: {self.script[min(self.script_index, len(self.script)-1)][2]}"
            surf = font.render(status_text, True, (255, 255, 0))
            self.screen.blit(surf, (10, 10))
            
            pygame.display.flip()
            
            if self.script_index >= len(self.script) and elapsed > 15:
                running = False

        pygame.quit()

if __name__ == "__main__":
    demo = AssistedTester()
    demo.run()
