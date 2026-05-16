import json
from src.models.world import Position

class CutsceneParser:
    def __init__(self, api):
        self.api = api

    def parse_action(self, action):
        action_type = action.get("type")
        
        if action_type == "dialogue":
            return self.api.say(action.get("text", ""))
        
        elif action_type == "move":
            entity_id = action.get("entity")
            target_data = action.get("target")
            target_pos = Position(target_data["x"], target_data["y"])
            speed = action.get("speed", 2)
            
            # We need a way to get the entity from the API
            entity = self.api.get_entity(entity_id)
            if entity:
                return self.api.move_to(entity, target_pos, speed)
            return None
            
        elif action_type == "wait":
            return ("wait", action.get("duration", 1.0))
            
        elif action_type == "sound":
            return ("sound", action.get("id"))
            
        elif action_type == "animate":
            return ("animate", action.get("entity"), action.get("animation"))
            
        elif action_type == "camera":
            return ("camera", action.get("target"), action.get("speed"))

        elif action_type == "flag":
            return ("flag", action.get("name"), action.get("value"))

        return None

    def create_generator(self, script_data):
        for action in script_data:
            parsed = self.parse_action(action)
            if parsed:
                # If it's a tuple that the director already handles, yield it
                # Some actions might need to be awaited
                yield parsed

    def load_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return self.create_generator(data)
