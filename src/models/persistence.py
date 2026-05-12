import json
import os

from src.models.classes import Warrior, Mage, Rogue

class SaveManager:
    def __init__(self, filename="savegame.json"):
        self.filename = filename
        self.class_map = {
            "Warrior": Warrior,
            "Mage": Mage,
            "Rogue": Rogue
        }

    def save_game(self, player):
        """Serializes player data to a JSON file."""
        try:
            data = {
                "name": player.name,
                "class": player.character_class.__class__.__name__,
                "level": player.level,
                "hp": player.hp,
                "mana": player.mana,
                "xp": player.xp,
                "energy": player.energy,
                "skills": list(player.skills),
                "position": {
                    "x": player.position.x,
                    "y": player.position.y
                }
            }
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self):
        """Loads data from the JSON file."""
        if not os.path.exists(self.filename):
            return None
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
