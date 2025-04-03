from ..models.grid import Grid
from ..models.frontier import StackFrontier, PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored = {} 
        
        # Add the node to the explored dictionary
        explored[node.state] = True
        
        frontera = PriorityQueueFrontier()
        frontera.add(node, node.cost)
        alcanzados = {}
        alcanzados[node.state] = node.cost

        while True:
            if frontera.is_empty():
                return NoSolution(alcanzados)
            n = frontera.pop()
            if grid.end == n.state:
                return Solution(n, alcanzados)
            succesors = grid.get_neighbours(n.state)
            for accion, estado in succesors.items():
                costo_sucesor = n.cost + grid.get_cost(estado)
                if estado not in alcanzados or costo_sucesor < alcanzados[estado]:
                    nuevo = Node('', estado, costo_sucesor, n, accion)
                    alcanzados[estado] = costo_sucesor
                    frontera.add(nuevo, costo_sucesor)
