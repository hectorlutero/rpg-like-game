import pytest

def create_grid_walkable_func(grid_map: list[str]):
    """Helper to convert a string array map into a walkable callable."""
    height = len(grid_map)
    width = len(grid_map[0]) if height > 0 else 0

    def is_walkable(x: int, y: int) -> bool:
        if not (0 <= x < width and 0 <= y < height):
            return False
        return grid_map[y][x] != "#"
    return is_walkable

def test_find_path_clear_straight():
    from src.logic.pathfinding import PathfindingEngine
    engine = PathfindingEngine()
    
    grid = [
        ".....",
        ".....",
        ".....",
    ]
    is_walkable = create_grid_walkable_func(grid)
    
    path = engine.find_path((0, 1), (4, 1), is_walkable)
    assert path == [(1, 1), (2, 1), (3, 1), (4, 1)]

def test_find_path_u_shape_obstacle():
    from src.logic.pathfinding import PathfindingEngine
    engine = PathfindingEngine()
    
    grid = [
        ".....",
        ".###.",
        ".#.#.",
        "....."
    ]
    is_walkable = create_grid_walkable_func(grid)
    
    start = (2, 2)
    target = (2, 0)
    
    path = engine.find_path(start, target, is_walkable)
    
    assert len(path) == 8
    assert path[-1] == target
    assert (2, 3) in path 
    for x, y in path:
        assert grid[y][x] != "#"

def test_find_path_unreachable():
    from src.logic.pathfinding import PathfindingEngine
    engine = PathfindingEngine()
    
    grid = [
        ".....",
        ".###.",
        ".#.#.",
        ".###."
    ]
    is_walkable = create_grid_walkable_func(grid)
    
    # Start inside the closed box
    start = (2, 2)
    # Target is outside
    target = (2, 0)
    
    path = engine.find_path(start, target, is_walkable)
    
    # Should fail gracefully and return an empty list
    assert path == []

def test_find_path_target_impassable():
    from src.logic.pathfinding import PathfindingEngine
    engine = PathfindingEngine()
    
    grid = [
        ".....",
        ".....",
        "..#..",
    ]
    is_walkable = create_grid_walkable_func(grid)
    
    path = engine.find_path((0, 0), (2, 2), is_walkable)
    
    # Should fail gracefully and return an empty list
    assert path == []
