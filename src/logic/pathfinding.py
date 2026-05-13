import heapq
from typing import Callable, Tuple, List, Dict, Optional

Point = Tuple[int, int]

class PathfindingEngine:
    def __init__(self):
        # Allow only 4-directional movement as per "game remains strictly 4-directional"
        self.directions = [
            (0, -1), # up
            (1, 0),  # right
            (0, 1),  # down
            (-1, 0)  # left
        ]

    def _manhattan_distance(self, a: Point, b: Point) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start: Point, target: Point, is_walkable: Callable[[int, int], bool]) -> List[Point]:
        if not is_walkable(target[0], target[1]):
            return []
            
        if start == target:
            return []

        open_set = []
        count = 0
        
        # open_set elements: (f_score, count, node)
        heapq.heappush(open_set, (0, count, start))
        
        came_from: Dict[Point, Point] = {}
        
        g_score: Dict[Point, int] = {start: 0}
        
        # We don't actually need f_score dict, just g_score and the heuristic for the heap
        
        while open_set:
            current_f, _, current = heapq.heappop(open_set)
            
            if current == target:
                return self._reconstruct_path(came_from, current)
                
            for dx, dy in self.directions:
                neighbor = (current[0] + dx, current[1] + dy)
                
                if not is_walkable(neighbor[0], neighbor[1]):
                    continue
                    
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    
                    f_score = tentative_g_score + self._manhattan_distance(neighbor, target)
                    count += 1
                    heapq.heappush(open_set, (f_score, count, neighbor))
                    
        return []

    def _reconstruct_path(self, came_from: Dict[Point, Point], current: Point) -> List[Point]:
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path
