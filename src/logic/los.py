import math
from typing import Callable, Tuple

Point = Tuple[int, int]

class LineOfSight:
    def _get_distance(self, a: Point, b: Point) -> float:
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def has_los(self, start: Point, end: Point, is_opaque: Callable[[int, int], bool], max_distance: float = 999) -> bool:
        """
        Returns True if there are no opaque tiles between start and end.
        Uses Bresenham's line algorithm to trace tiles.
        """
        dist = self._get_distance(start, end)
        if dist > max_distance:
            return False
            
        x0, y0 = start
        x1, y1 = end
        
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        
        while True:
            # We check if CURRENT tile is opaque.
            # Usually, we don't check the start tile if the entity itself is there.
            # But we must check the target tile and everything in between.
            if (x0, y0) != start:
                if is_opaque(x0, y0):
                    return False
            
            if x0 == x1 and y0 == y1:
                break
                
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy
                
        return True
