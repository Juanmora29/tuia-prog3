from typing import Optional, Callable, Tuple
from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

class GreedyBestFirstSearch:
    @staticmethod
    def heuristica_manhattan(coord: Tuple[int, int], grid) -> float:
                x, y = coord
                gx, gy = grid.end
                return abs(x - gx) + abs(y - gy)
    
    def search(
        grid: Grid
    ) -> Solution:
      
        start = grid.start
        node = Node("", start, 0)
        alcanzados = {start: 0}
        frontera = PriorityQueueFrontier()
        frontera.add(node, GreedyBestFirstSearch.heuristica_manhattan(start, grid))

        while not frontera.is_empty():
            n = frontera.pop()
            if n.state == grid.end:
                return Solution(n, alcanzados)

            for accion, estado in grid.get_neighbours(n.state).items():
                if estado not in alcanzados:
                    costo_sucesor = n.cost + grid.get_cost(estado)
                    alcanzados[estado] = costo_sucesor
                    nuevo = Node("", estado, costo_sucesor, n, accion)
                    frontera.add(nuevo, GreedyBestFirstSearch.heuristica_manhattan(estado, grid))

        return NoSolution(alcanzados)
    
    
            
    
    
