import random
from typing import Tuple

class AIBehavior:
    def update(self, entity, world, dt: float):
        pass

class StaticBehavior(AIBehavior):
    def update(self, entity, world, dt: float):
        pass

class RandomWanderBehavior(AIBehavior):
    def __init__(self, move_interval: float = 2.0):
        self.move_interval = move_interval
        self.timer = 0.0
        
    def _get_random_direction(self) -> Tuple[int, int]:
        return random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

    def update(self, entity, world, dt: float):
        self.timer += dt
        if self.timer >= self.move_interval:
            self.timer = 0.0
            
            dx, dy = self._get_random_direction()
            
            # Convert pixel position to grid position
            # Interactables are centered at (tx * 32 + 16, ty * 32 + 16)
            current_tx = int(entity.position.x // world.tile_size)
            current_ty = int(entity.position.y // world.tile_size)
            
            target_tx = current_tx + dx
            target_ty = current_ty + dy
            
            # Attempt to claim tile
            if world.move_interactable(current_tx, current_ty, target_tx, target_ty):
                # Update visual position (instantly for now, visual_offset is Issue #70 territory)
                entity.position.x = target_tx * world.tile_size + (world.tile_size // 2)
                entity.position.y = target_ty * world.tile_size + (world.tile_size // 2)

class AIController:
    def __init__(self, behavior: AIBehavior):
        self.behavior = behavior

    def update(self, entity, world, dt: float):
        if self.behavior:
            self.behavior.update(entity, world, dt)
