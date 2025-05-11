"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo. Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from time import time
from problem import OptProblem
from collections import deque 


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Buscamos la acción que genera el sucesor con mayor valor objetivo
            act, succ_val = problem.max_action(actual)

            # Retornar si estamos en un maximo local:
            # el valor objetivo del sucesor es menor o igual al del estado actual
            if succ_val <= value:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            actual = problem.result(actual, act)
            value = succ_val
            self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""

    def __init__(self,max_iters=1000):
        super().__init__()
        self.max_iters = max_iters  # nuevo parámetro

    def solve(self, problem: OptProblem):
        #incio de contador
        start = time()

        #establecemos el nodo inicial y su valor objetivo
        actual = problem.init
        value = problem.obj_val(actual)

        #establecemos una variable que va a guardar el estado con mejor valor objt 
        best = actual
        best_val = value

        #iteramos en base la max iters que seteamos
        while self.niters < self.max_iters:

            #obtenemos la accion y el valor objetivo del sucesor
            act, succ_val = problem.max_action(actual)

            #si el valor obj del sucesor es mejor o igual que el valor del estado actual
            if succ_val <= value:
                # Reinicio aleatorio
                actual = problem.random_reset()
                value = problem.obj_val(actual)
            else:
                #si no, actualizamos el valor del estado actual 
                actual = problem.result(actual, act)
                value = succ_val

                #si el valor obj es mejor que el que estado que tenemos guardado
                #como mejor, lo remplazamos
                if value > best_val:
                    best = actual
                    best_val = value

            self.niters += 1
            self.tour = best
            self.value = best_val
            self.time = time() - start


class Tabu(LocalSearch):
    """Algoritmo de búsqueda tabú."""

    def __init__(self, umbral=500):
        super().__init__()
        self.umbral = umbral
        

    def solve(self, problem: OptProblem):
        #incio de contador
        start = time()

        #establecemos el nodo inicial y su valor objetivo
        actual = problem.init
        value = problem.obj_val(actual)

        #establecemos una variable que va a guardar el estado con mejor valor objt 
        best = actual
        best_val = value

        tabu_len = int(0.75*problem.G.number_of_nodes())  # problem.G.number_of_nodes()) me trae la cantidad de nodos con la cual inicia el problema.
                                                         # se puede cambiar el 0.75 para obtener mejores resultados

        #nuestra lista tabu es una cola de doble extremo
        #permite agregar o quitar elementos tanto de un extremo como del otro
        tabu_list = deque(maxlen=tabu_len)
        sin_mejora = 0

        while True:
            #Modificamos max action en problem.py para que pueda recivir nuestra lista tabu
            act, succ_val = problem.max_action(actual, tabu_list)
            sucesor = problem.result(actual, act)

            if succ_val > best_val:
                sin_mejora = 0 # reiniciamos el contador por que mejoramos el best value
                best = sucesor
                best_val = succ_val
            else:
                 sin_mejora += 1 #si el valor obj no es mejor que el best value que tenemos, sumamos 1 a la variable sin mejora
                 if sin_mejora == self.umbral: #y si llegamos al umbral, cortamos
                    break
            
            
            tabu_list.append(act)
            actual = sucesor

            self.niters += 1
            self.tour = best
            self.value = best_val
            self.time = time() - start


