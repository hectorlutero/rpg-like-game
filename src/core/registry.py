import json
import os
from src.models.interaction import Chest, MagicBook, TrainingObject, Portal
from src.models.dialogue import NPC
from src.models.combat import EnemyInteractable
from src.ui.shop_scene import Shopkeeper

class EntityRegistry:
    def __init__(self, data_path):
        self.data_path = data_path
        self.prefabs = self._load_data()
        self._type_map = {
            "Chest": Chest,
            "NPC": NPC,
            "MagicBook": MagicBook,
            "TrainingObject": TrainingObject,
            "Enemy": EnemyInteractable,
            "Shopkeeper": Shopkeeper,
            "Portal": Portal
        }

    def _load_data(self):
        if not os.path.exists(self.data_path):
            return {}
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_prefab(self, entity_id):
        return self.prefabs.get(entity_id)

    def spawn(self, entity_id, **overrides):
        prefab = self.get_prefab(entity_id)
        if not prefab:
            return None
        
        entity_type = prefab.get("type")
        cls = self._type_map.get(entity_type)
        if not cls:
            return None
            
        # Merge data from prefab with overrides
        data = prefab.get("data", {}).copy()
        data.update(overrides)
        
        # Convert "position" dict to Position object if present
        if "position" in data and isinstance(data["position"], dict):
            from src.models.world import Position
            data["position"] = Position(data.get("position", {}).get("x", 0), 
                                       data.get("position", {}).get("y", 0))

        return cls(**data)

    def spawn_to_map(self, entity_id, world, tx, ty, **overrides):
        """Spawns an entity and adds it to the world at tile coordinates (tx, ty)."""
        entity = self.spawn(entity_id, **overrides)
        if entity:
            world.add_interactable(tx, ty, entity)
        return entity
