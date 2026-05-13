class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class World:
    def __init__(self, grid, tile_size=32):
        self.grid = grid # List of lists
        self.tile_size = tile_size
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

    def can_move_to(self, entity, target_x, target_y):
        # A entidade tem 32x32 e o centro é (target_x, target_y)
        # Vamos checar os 4 cantos da caixa de colisão.
        # Usamos uma pequena margem (2px) para a colisão não ser "travada" demais.
        half = self.tile_size // 2
        margin = 2
        
        corners = [
            (target_x - half + margin, target_y - half + margin), # Top-Left
            (target_x + half - margin, target_y - half + margin), # Top-Right
            (target_x - half + margin, target_y + half - margin), # Bottom-Left
            (target_x + half - margin, target_y + half - margin)  # Bottom-Right
        ]

        for cx, cy in corners:
            grid_x = int(cx // self.tile_size)
            grid_y = int(cy // self.tile_size)

            # Check bounds
            if grid_x < 0 or grid_x >= self.width or grid_y < 0 or grid_y >= self.height:
                return False

            # Check if tile is solid (1 = solid)
            if self.grid[grid_y][grid_x] == 1:
                return False

            # Check for interactables (NPCs, Enemies, etc.)
            if (grid_x, grid_y) in self.interactables:
                return False

        return True
