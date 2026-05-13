import json
import os
from src.models.world import World

class WorldOrchestrator:
    def __init__(self, registry, global_state=None):
        self.registry = registry
        self.global_state = global_state
        self.current_tags = {}

    def load_map(self, map_path):
        if not os.path.exists(map_path):
            return None
            
        with open(map_path, 'r', encoding='utf-8') as f:
            map_data = json.load(f)
            
        grid = map_data.get("grid", [])
        world = World(grid)
        
        self.current_tags = map_data.get("tags", {})
        
        entities_data = map_data.get("entities", [])
        for ent_info in entities_data:
            entity_id = ent_info.get("id")
            tx = ent_info.get("x")
            ty = ent_info.get("y")
            overrides = ent_info.get("overrides", {}).copy()
            
            # Inject calculated position
            if "position" not in overrides:
                overrides["position"] = {
                    "x": tx * world.tile_size + world.tile_size // 2,
                    "y": ty * world.tile_size + world.tile_size // 2
                }
            
            # Apply deltas if available
            unique_id = overrides.get("chest_id") or overrides.get("entity_id")
            
            if self.global_state and unique_id:
                delta = self.global_state.get_entity_delta(unique_id)
                if delta:
                    overrides.update(delta)

            self.registry.spawn_to_map(entity_id, world, tx, ty, **overrides)
            
        return world

    def update_ai(self, world, dt):
        """Ticks AI reasoning for all entities in the world."""
        # Make a copy of values to avoid 'dictionary changed size during iteration' 
        # although move_interactable doesn't change dict size, just values.
        # But it's safer.
        for entity in list(world.interactables.values()):
            if hasattr(entity, "ai") and entity.ai:
                entity.ai.update(entity, world, dt)

    def get_tag_position(self, tag_name):
        """Returns the tile coordinates (tx, ty) for a given tag."""
        tag = self.current_tags.get(tag_name)
        if tag:
            return tag.get("x"), tag.get("y")
        return None, None
