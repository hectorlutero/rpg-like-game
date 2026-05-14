import random
import math
from typing import Tuple, List, Optional
from src.logic.pathfinding import PathfindingEngine
from src.logic.los import LineOfSight

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
            
            current_tx = int(entity.position.x // world.tile_size)
            current_ty = int(entity.position.y // world.tile_size)
            
            target_tx = current_tx + dx
            target_ty = current_ty + dy
            
            if world.move_interactable(current_tx, current_ty, target_tx, target_ty):
                entity.position.x = target_tx * world.tile_size + (world.tile_size // 2)
                entity.position.y = target_ty * world.tile_size + (world.tile_size // 2)

class PursuitBehavior(AIBehavior):
    def __init__(self, player, los_range: float = 5.0, leash_range: float = 10.0, move_interval: float = 0.5):
        self.player = player
        self.los_range = los_range
        self.leash_range = leash_range
        self.move_interval = move_interval
        self.timer = 0.0
        
        self.pathfinding = PathfindingEngine()
        self.los = LineOfSight()
        
        self.spawn_pos: Optional[Tuple[int, int]] = None
        self.cached_path: List[Tuple[int, int]] = []
        self.last_target_pos: Optional[Tuple[int, int]] = None
        self.is_pursuing = False
        self.is_returning = False

    def _get_grid_pos(self, position, tile_size) -> Tuple[int, int]:
        return int(position.x // tile_size), int(position.y // tile_size)

    def update(self, entity, world, dt: float):
        if self.spawn_pos is None:
            self.spawn_pos = self._get_grid_pos(entity.position, world.tile_size)
            
        self.timer += dt
        if self.timer < self.move_interval:
            return
            
        self.timer = 0.0
        
        current_tx, current_ty = self._get_grid_pos(entity.position, world.tile_size)
        player_tx, player_ty = self._get_grid_pos(self.player.position, world.tile_size)
        
        dist_to_player = math.sqrt((current_tx - player_tx)**2 + (current_ty - player_ty)**2)
        dist_to_spawn = math.sqrt((current_tx - self.spawn_pos[0])**2 + (current_ty - self.spawn_pos[1])**2)
        
        # 1. Check for Leashing (Return to spawn)
        if dist_to_spawn > self.leash_range:
            self.is_pursuing = False
            self.is_returning = True
            self.cached_path = [] # Force recalculation for return
            
        if self.is_returning:
            if (current_tx, current_ty) == self.spawn_pos:
                self.is_returning = False
                self.cached_path = []
                return
            self._move_towards(entity, world, self.spawn_pos)
            return

        # 2. Check for Pursuit activation via LoS
        def is_opaque(x, y):
            return world.grid[y][x] == 1
            
        has_los = self.los.has_los((current_tx, current_ty), (player_tx, player_ty), is_opaque, max_distance=self.los_range)
        
        if has_los:
            self.is_pursuing = True
            
            # Recalculate path ONLY if path is empty OR target moved
            if not self.cached_path or self.last_target_pos != (player_tx, player_ty):
                self.last_target_pos = (player_tx, player_ty)
                
                def is_walkable(x, y):
                    if not (0 <= x < world.width and 0 <= y < world.height):
                        return False
                    if world.grid[y][x] == 1:
                        return False
                    return True
                    
                self.cached_path = self.pathfinding.find_path((current_tx, current_ty), (player_tx, player_ty), is_walkable)
            
        if self.is_pursuing:
            if self.cached_path:
                next_step = self.cached_path.pop(0)
                if world.move_interactable(current_tx, current_ty, next_step[0], next_step[1]):
                    entity.position.x = next_step[0] * world.tile_size + (world.tile_size // 2)
                    entity.position.y = next_step[1] * world.tile_size + (world.tile_size // 2)
                else:
                    # Blocked, clear path to recalculate next time
                    self.cached_path = []
            else:
                # No path or reached target, check LoS again
                if not has_los:
                    self.is_pursuing = False

    def _move_towards(self, entity, world, target_tx_ty):
        current_tx, current_ty = self._get_grid_pos(entity.position, world.tile_size)
        
        if not self.cached_path:
            def is_walkable(x, y):
                if not (0 <= x < world.width and 0 <= y < world.height): return False
                return world.grid[y][x] == 0
            self.cached_path = self.pathfinding.find_path((current_tx, current_ty), target_tx_ty, is_walkable)
            
        if self.cached_path:
            next_step = self.cached_path.pop(0)
            if world.move_interactable(current_tx, current_ty, next_step[0], next_step[1]):
                entity.position.x = next_step[0] * world.tile_size + (world.tile_size // 2)
                entity.position.y = next_step[1] * world.tile_size + (world.tile_size // 2)
            else:
                self.cached_path = []

class AIController:
    def __init__(self, behavior: AIBehavior):
        self.behavior = behavior

    def update(self, entity, world, dt: float):
        if self.behavior:
            self.behavior.update(entity, world, dt)
