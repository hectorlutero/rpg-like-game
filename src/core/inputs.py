from enum import Enum, auto
import pygame

class InputAction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    CONFIRM = auto()
    CANCEL = auto()
    INTERACT = auto()
    MENU = auto()
    TOGGLE_MODE = auto()
    QUICK_SAVE = auto()
    QUICK_LOAD = auto()

class InputManager:
    InputAction = InputAction
    
    def __init__(self):
        self.presets = {
            "Standard": {
                InputAction.UP: [pygame.K_UP],
                InputAction.DOWN: [pygame.K_DOWN],
                InputAction.LEFT: [pygame.K_LEFT],
                InputAction.RIGHT: [pygame.K_RIGHT],
                InputAction.CONFIRM: [pygame.K_SPACE, pygame.K_RETURN],
                InputAction.CANCEL: [pygame.K_ESCAPE],
                InputAction.INTERACT: [pygame.K_SPACE, pygame.K_e],
                InputAction.MENU: [pygame.K_m, pygame.K_TAB],
                InputAction.TOGGLE_MODE: [pygame.K_TAB],
                InputAction.QUICK_SAVE: [pygame.K_F5],
                InputAction.QUICK_LOAD: [pygame.K_F9],
            },
            "WASD": {
                InputAction.UP: [pygame.K_w],
                InputAction.DOWN: [pygame.K_s],
                InputAction.LEFT: [pygame.K_a],
                InputAction.RIGHT: [pygame.K_d],
                InputAction.CONFIRM: [pygame.K_SPACE, pygame.K_RETURN],
                InputAction.CANCEL: [pygame.K_ESCAPE],
                InputAction.INTERACT: [pygame.K_SPACE, pygame.K_e],
                InputAction.MENU: [pygame.K_m, pygame.K_TAB],
                InputAction.TOGGLE_MODE: [pygame.K_TAB],
                InputAction.QUICK_SAVE: [pygame.K_F5],
                InputAction.QUICK_LOAD: [pygame.K_F9],
            }
        }
        self.current_preset = "Standard"
        self.mapping = self.presets[self.current_preset].copy()

    def set_preset(self, preset_name):
        if preset_name in self.presets:
            self.current_preset = preset_name
            self.mapping = self.presets[preset_name].copy()

    def is_action_pressed(self, action, keys=None):
        if keys is None:
            try:
                if pygame.display.get_init():
                    keys = pygame.key.get_pressed()
                else:
                    return False
            except pygame.error:
                return False
        
        target_keys = self.mapping.get(action, [])
        for k in target_keys:
            if keys[k]:
                return True
        return False

    def is_action_just_pressed(self, action, event):
        if event.type != pygame.KEYDOWN:
            return False
        
        target_keys = self.mapping.get(action, [])
        return event.key in target_keys
