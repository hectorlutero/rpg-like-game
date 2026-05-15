import pygame
from src.ui.scenes import Scene
from src.models.interaction import SelectionManager
from src.logic.difficulty import DifficultyManager

class DifficultySelectionScene(Scene):
    def __init__(self, manager, callback):
        self.manager = manager
        self.context = manager.context
        self.callback = callback
        self.options = [DifficultyManager.EASY, DifficultyManager.NORMAL, DifficultyManager.HARD]
        self.selector = SelectionManager(self.options)
        self.selector.index = 1 # Normal por padrão

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            inputs = self.context.inputs
            if inputs.is_action_just_pressed(inputs.InputAction.UP, event):
                self.selector.prev()
            elif inputs.is_action_just_pressed(inputs.InputAction.DOWN, event):
                self.selector.next()
            elif inputs.is_action_just_pressed(inputs.InputAction.CONFIRM, event):
                diff_choice = self.selector.current_item
                self.context.difficulty_manager = DifficultyManager(diff_choice)
                self.callback()

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((20, 20, 40))
        self._draw_text(screen, "SELECIONE A DIFICULDADE", 400, 150, size=32, color=(255, 215, 0))
        
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selector.index else (100, 100, 100)
            prefix = "> " if i == self.selector.index else "  "
            self._draw_text(screen, f"{prefix}{option}", 400, 250 + i*50, size=24, color=color)
            
            if i == self.selector.index:
                desc = ""
                if option == DifficultyManager.EASY: 
                    desc = "Inimigos com -20% HP/Dano. Recompensas +20%."
                elif option == DifficultyManager.NORMAL: 
                    desc = "Equilíbrio padrão para aventureiros."
                elif option == DifficultyManager.HARD: 
                    desc = "Inimigos com +50% HP e +30% Dano. Recompensas -20%."
                self._draw_text(screen, desc, 400, 450, size=18, color=(180, 180, 180))
        
        self._draw_text(screen, "SETAS: Navegar | ENTER: Confirmar", 400, 550, size=16, color=(150, 150, 150))
