import pygame
import math
from src.models.interaction import Interactable

class NPC(Interactable):
    def __init__(self, name, position, dialogue_data=None):
        self.name = name
        self.position = position
        self.dialogue_data = dialogue_data

    def on_interact(self, context):
        """Returns a DialogueManager to be used by the scene."""
        return DialogueManager(self.dialogue_data)

    def is_near(self, other_position, distance=32):
        dx = self.position.x - other_position.x
        dy = self.position.y - other_position.y
        return math.sqrt(dx*dx + dy*dy) <= distance

    def draw(self, screen, context, pos):
        # NPCs são quadrados verdes
        pygame.draw.rect(screen, (50, 200, 50), (pos[0] + 4, pos[1] + 4, 24, 24))
        # Chapéu ou detalhe
        pygame.draw.rect(screen, (255, 255, 255), (pos[0] + 10, pos[1] + 2, 12, 4))

class DialogueManager:
    def __init__(self, data, start_index=0):
        self.data = data
        self.current_index = start_index
        self.finished = False
        
        # Determine if data is a list (linear) or dict (branching)
        self.is_branching = isinstance(data, dict)

    def get_current_line(self):
        if self.finished:
            return ""
        if self.is_branching:
            return self.data[self.current_index]["text"]
        else:
            return self.data[self.current_index]

    def get_current_choices(self):
        if self.is_branching and not self.finished:
            return self.data[self.current_index].get("choices")
        return None

    def next_line(self):
        if self.is_branching:
            # For branching, next_line only works if there are no choices
            choices = self.get_current_choices()
            if not choices:
                self.finished = True
        else:
            self.current_index += 1
            if self.current_index >= len(self.data):
                self.finished = True

    def make_choice(self, choice_text):
        choices = self.get_current_choices()
        if choices and choice_text in choices:
            self.current_index = choices[choice_text]
        else:
            self.finished = True

    def is_finished(self):
        return self.finished
