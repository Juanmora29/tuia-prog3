from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node
from typing import Tuple
from ..search.gbfs import GreedyBestFirstSearch


class AStarSearch:
    @staticmethod
    def search(
        grid: Grid
    ) -> Solution:

        start = grid.start
        node = Node("", start, 0)
        alcanzados = {start: 0}
        frontera = PriorityQueueFrontier()

        # PRIORIDAD = heurística de la posición de inicio
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
                    # 3) PRIORIDAD = heurística de la posición del sucesor
                    frontera.add(nuevo, n.cost + GreedyBestFirstSearch.heuristica_manhattan(estado, grid))

        return NoSolution(alcanzados)
