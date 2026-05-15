import pygame

class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class World:
    def __init__(self, grid, tile_size=32, tileset_id=None):
        self.grid = grid # List of lists
        self.tile_size = tile_size
        self.tileset_id = tileset_id
        self.width = len(grid[0]) if grid else 0
        self.height = len(grid) if grid else 0
        self.interactables = {} # {(tile_x, tile_y): object}

    def add_interactable(self, tx, ty, obj):
        self.interactables[(tx, ty)] = obj

    def remove_interactable(self, tx, ty):
        if (tx, ty) in self.interactables:
            del self.interactables[(tx, ty)]

    def get_interactable_at(self, tx, ty):
        return self.interactables.get((tx, ty))

    def move_interactable(self, from_tx, from_ty, to_tx, to_ty):
        """
        Attempts to move an interactable from one tile to another.
        Rejects movement and returns False if the target is out of bounds,
        a solid wall, or already occupied by another interactable.
        Returns True if successful.
        """
        if (from_tx, from_ty) not in self.interactables:
            return False

        if to_tx < 0 or to_tx >= self.width or to_ty < 0 or to_ty >= self.height:
            return False

        if self.grid[to_ty][to_tx] == 1: # 1 means solid wall
            return False

        if (to_tx, to_ty) in self.interactables:
            return False

        # Move the entity in the dictionary
        entity = self.interactables.pop((from_tx, from_ty))
        self.interactables[(to_tx, to_ty)] = entity
        return True

    def get_interactable_at_pixel(self, px, py):
        tx = int(px // self.tile_size)
        ty = int(py // self.tile_size)
        return self.get_interactable_at(tx, ty)

    def is_collision(self, rect, ignore_entity=None):
        """Checks if a Rect overlaps solid tiles or is out of bounds."""
        # 1. Bounds check
        if rect.left < 0 or rect.right > self.width * self.tile_size or \
           rect.top < 0 or rect.bottom > self.height * self.tile_size:
            return True

        # 2. Tile check
        # Get range of tiles covered by the rect
        start_x = int(rect.left // self.tile_size)
        end_x = int((rect.right - 1) // self.tile_size)
        start_y = int(rect.top // self.tile_size)
        end_y = int((rect.bottom - 1) // self.tile_size)

        for ty in range(start_y, end_y + 1):
            for tx in range(start_x, end_x + 1):
                if self.grid[ty][tx] == 1:
                    return True

        # 3. Entity check
        for obj in self.interactables.values():
            if obj == ignore_entity:
                continue
            
            # Check if object has a hitbox
            if hasattr(obj, "get_hitbox"):
                obj_hitbox = obj.get_hitbox()
                if rect.colliderect(obj_hitbox):
                    return True
            else:
                # Fallback to tile-based collision if no hitbox method (legacy/simple objects)
                # This part is optional but keeps backward compatibility
                pass

        return False

    def can_move_to(self, entity, target_x, target_y):
        """
        Checks if the entity can move to the target center position (pixel-based).
        Uses hitboxes for high precision.
        """
        # Create a temporary Position object for calculation
        target_pos = Position(target_x, target_y)
        
        # Get the hitbox the entity would have at that position
        if hasattr(entity, "get_hitbox"):
            try:
                rect = entity.get_hitbox(position=target_pos)
            except TypeError:
                # Fallback if get_hitbox doesn't accept position argument yet
                rect = entity.get_hitbox()
                # Manually adjust rect for target position if it's not the same
                # (This is a safety fallback)
                pass
        else:
            # Legacy fallback: full tile centered at target
            half = self.tile_size // 2
            margin = 2
            rect = pygame.Rect(target_x - half + margin, target_y - half + margin, 
                               self.tile_size - 2*margin, self.tile_size - 2*margin)

        # Check for collision in the world (solid tiles + other entities)
        # We ignore the entity itself
        return not self.is_collision(rect, ignore_entity=entity)
