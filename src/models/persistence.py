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
    def __init__(self, base_filename="savegame"):
        self.base_filename = base_filename
        self.class_map = {
            "Warrior": Warrior,
            "Mage": Mage,
            "Rogue": Rogue
        }

    def _get_filename(self, slot):
        if slot == 0:
            return f"{self.base_filename}.json"
        return f"{self.base_filename}_{slot}.json"

    def save_game(self, context, slot=0):
        """Serializes player and world data to a JSON file."""
        import datetime
        # Protection: No saving while a script is busy
        if hasattr(context, "director") and context.director and context.director.is_busy():
            print("Cannot save while a script is running.")
            return False

        player = context.player
        filename = self._get_filename(slot)
        
        try:
            metadata = {
                "slot": slot,
                "timestamp": datetime.datetime.now().isoformat(),
                "play_time": getattr(context, "play_time", 0.0),
                "level": player.level,
                "location": context.world.map_name if hasattr(context.world, "map_name") else "Unknown"
            }
            
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
                "difficulty": context.difficulty_manager.difficulty if hasattr(context, "difficulty_manager") else "Normal",
                "equipment": {slot_name: (item.name if item else None) for slot_name, item in player.equipment.items()},
                "global_state": context.global_state.to_dict() if hasattr(context, "global_state") else {},
                "audio": context.audio.volumes if hasattr(context, "audio") and context.audio else {},
                "position": {
                    "x": player.position.x,
                    "y": player.position.y
                },
                "play_time": getattr(context, "play_time", 0.0)
            }
            
            full_data = {
                "metadata": metadata,
                "data": data
            }
            
            with open(filename, 'w') as f:
                json.dump(full_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self, slot=0):
        """Loads data from the JSON file."""
        filename = self._get_filename(slot)
        if not os.path.exists(filename):
            return None
        try:
            with open(filename, 'r') as f:
                full_data = json.load(f)
                # Handle legacy format or new format
                if "metadata" in full_data and "data" in full_data:
                    return full_data["data"]
                return full_data
        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    def get_slots_metadata(self, max_slots=5):
        """Returns a list of metadata for all available save slots."""
        slots = {}
        # Legacy check
        legacy_file = f"{self.base_filename}.json"
        if os.path.exists(legacy_file):
            try:
                with open(legacy_file, 'r') as f:
                    data = json.load(f)
                    if "metadata" in data:
                        slots[0] = data["metadata"]
                    else:
                        slots[0] = {"slot": 0, "level": data.get("level", 1), "play_time": data.get("play_time", 0.0)}
            except:
                pass

        for i in range(1, max_slots + 1):
            filename = self._get_filename(i)
            if os.path.exists(filename):
                try:
                    with open(filename, 'r') as f:
                        data = json.load(f)
                        if "metadata" in data:
                            slots[i] = data["metadata"]
                except:
                    pass
        return slots
