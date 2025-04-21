from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node
from typing import Tuple


class AStarSearch:
    @staticmethod
    def search(
        grid: Grid,
        h = None
    ) -> Solution:
        # heurística Manhattan por defecto
        if h is None:
            def default_h(coord: Tuple[int, int]) -> float:
                x, y = coord
                gx, gy = grid.end
                return abs(x - gx) + abs(y - gy)
            h = default_h

        start = grid.start
        node = Node("", start, 0)
        alcanzados = {start: 0}
        frontera = PriorityQueueFrontier()

        # PRIORIDAD = heurística de la posición de inicio
        frontera.add(node, h(start))

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
                    frontera.add(nuevo, n.cost + h(estado))

        return NoSolution(alcanzados)
