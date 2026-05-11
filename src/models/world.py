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

    def can_move_to(self, entity, target_x, target_y):
        # Convert pixel coordinates to grid coordinates
        grid_x = int(target_x // self.tile_size)
        grid_y = int(target_y // self.tile_size)

        # Check bounds
        if grid_x < 0 or grid_x >= self.width or grid_y < 0 or grid_y >= self.height:
            return False

        # Check if tile is solid (1 = solid)
        if self.grid[grid_y][grid_x] == 1:
            return False

        return True
