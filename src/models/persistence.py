import json
import os

from src.models.classes import Warrior, Mage, Rogue

class Inventory:
    def __init__(self, items=None):
        self.items = items or []

    def add_item(self, item_name):
        self.items.append(item_name)

    def remove_item(self, item_name):
        if item_name in self.items:
            self.items.remove(item_name)

class SaveManager:
    def __init__(self, filename="savegame.json"):
        self.filename = filename
        self.class_map = {
            "Warrior": Warrior,
            "Mage": Mage,
            "Rogue": Rogue
        }

    def save_game(self, context):
        """Serializes player and world data to a JSON file."""
        # Protection: No saving while a script is busy
        if hasattr(context, "director") and context.director and context.director.is_busy():
            print("Cannot save while a script is running.")
            return False

        player = context.player
        try:
            data = {
                "name": player.name,
                "class": player.character_class.__class__.__name__,
                "level": player.level,
                "hp": player.hp,
                "mana": player.mana,
                "xp": player.xp,
                "energy": player.energy,
                "gold": player.gold,
                "skills": list(player.skills),
                "inventory": player.inventory.items,
                "equipment": {slot: (item.name if item else None) for slot, item in player.equipment.items()},
                "global_state": context.global_state.to_dict() if hasattr(context, "global_state") else {},
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
