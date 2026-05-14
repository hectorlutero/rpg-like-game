import pytest
from src.logic.pathfinding import PathfindingEngine # Maybe I should move helpers to a common test utils?

def create_grid_is_opaque(grid_map: list[str]):
    height = len(grid_map)
    width = len(grid_map[0]) if height > 0 else 0
    def is_opaque(x, y):
        if not (0 <= x < width and 0 <= y < height):
            return True # Out of bounds is opaque
        return grid_map[y][x] == "#"
    return is_opaque

def test_los_clear_horizontal():
    from src.logic.los import LineOfSight
    los = LineOfSight()
    
    grid = [
        ".......",
        ".......",
        ".......",
    ]
    is_opaque = create_grid_is_opaque(grid)
    
    # Act & Assert
    assert los.has_los((0, 1), (6, 1), is_opaque) is True

def test_los_blocked_by_wall():
    from src.logic.los import LineOfSight
    los = LineOfSight()
    
    grid = [
        ".......",
        "...#...",
        ".......",
    ]
    is_opaque = create_grid_is_opaque(grid)
    
    # Act & Assert
    assert los.has_los((0, 1), (6, 1), is_opaque) is False

def test_los_diagonal_clear():
    from src.logic.los import LineOfSight
    los = LineOfSight()
    
    grid = [
        ".......",
        ".......",
        ".......",
        ".......",
    ]
    is_opaque = create_grid_is_opaque(grid)
    
    # (0,0) to (3,3)
    assert los.has_los((0, 0), (3, 3), is_opaque) is True

def test_los_diagonal_blocked():
    from src.logic.los import LineOfSight
    los = LineOfSight()
    
    grid = [
        ".......",
        ".#.....",
        "..#....",
        ".......",
    ]
    is_opaque = create_grid_is_opaque(grid)
    
    # (0,0) to (3,3) should pass through (1,1) or (2,2) or nearby
    assert los.has_los((0, 0), (3, 3), is_opaque) is False

def test_los_range_limit():
    from src.logic.los import LineOfSight
    los = LineOfSight()
    
    grid = [
        "..........",
    ]
    is_opaque = create_grid_is_opaque(grid)
    
    # Distance is 5 tiles
    assert los.has_los((0, 0), (5, 0), is_opaque, max_distance=10) is True
    assert los.has_los((0, 0), (5, 0), is_opaque, max_distance=4) is False
