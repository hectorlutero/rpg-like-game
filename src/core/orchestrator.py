import json
import os
from src.models.world import World

class WorldOrchestrator:
    def __init__(self, registry):
        self.registry = registry

    def load_map(self, map_path):
        if not os.path.exists(map_path):
            return None
            
        with open(map_path, 'r', encoding='utf-8') as f:
            map_data = json.load(f)
            
        grid = map_data.get("grid", [])
        world = World(grid)
        
        entities_data = map_data.get("entities", [])
        for ent_info in entities_data:
            entity_id = ent_info.get("id")
            tx = ent_info.get("x")
            ty = ent_info.get("y")
            overrides = ent_info.get("overrides", {}).copy()
            
            # Inject calculated position (Registry will convert to Position object)
            if "position" not in overrides:
                overrides["position"] = {
                    "x": tx * world.tile_size + world.tile_size // 2,
                    "y": ty * world.tile_size + world.tile_size // 2
                }
            
            self.registry.spawn_to_map(entity_id, world, tx, ty, **overrides)
            
        return world
