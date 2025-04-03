from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

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
        
        # Return if the node contains a goal state
        if node.state == grid.end:
            return Solution(node, explored)
        
        frontera = StackFrontier()
        frontera.add(node)
        expandidos = {}
        
        while True:
            if frontera.is_empty():
                return NoSolution(expandidos)
            n = frontera.remove()
            if n.state in expandidos:
                continue
            expandidos[n.state] = True
            successors = grid.get_neighbours(n.state)
            for accion, estado in successors.items():
                if estado not in expandidos:
                    nuevo = Node('',estado, n.cost + grid.get_cost(estado) , n, accion)
                    if estado == grid.end:
                        return Solution(nuevo, expandidos)
                    frontera.add(nuevo)
