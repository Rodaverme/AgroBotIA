"""
Módulo: A_estrella.py

Descripción:
    Este módulo implementa el algoritmo de búsqueda A* para el problema del AgroBot.

Autor: Agarcia07
Versión: 1.0
"""

# Imports
import heapq
import time
from itertools import count
from agrobot.busqueda.Costo.resultado import ResultadoBusqueda
from agrobot.busqueda.Avara.Avara import heuristica
from agrobot.domain.problema import (
    crear_estado_inicial,
    generar_sucesores,
    es_meta,
    clave_estado
)

def busqueda_A_estrella(mundo):

    """
    Implementa el algoritmo de búsqueda A* para encontrar el camino óptimo en el problema del AgroBot.

    Parámetros:
        mundo (Mundo): Una instancia de la clase Mundo que representa el entorno del problema.

    Retorna:
        ResultadoBusqueda: El resultado de la búsqueda si se encuentra una solución.
        None: En caso contrario.
    """

    inicio = time.perf_counter()

    contador = count() # Contador para desempatar nodos con la misma prioridad
    frontera = [] # Cola de prioridad para los nodos a explorar
    estado_inicial = crear_estado_inicial(mundo)
    nodos_expandidos = 0 # Contador de nodos expandidos

    heapq.heappush(
        frontera, 
        (heuristica(estado_inicial, mundo), next(contador), 0, estado_inicial, [estado_inicial.posicion])
    )

    mejores_costos = {
        clave_estado(estado_inicial): 0
    }

    while frontera:
        prioridad_actual, desempate, costo_actual, estado_actual, camino_actual = heapq.heappop(frontera)

        if costo_actual > mejores_costos[clave_estado(estado_actual)]:
            continue

        if es_meta(estado_actual):
            return ResultadoBusqueda(
                camino = camino_actual,
                costo = costo_actual,
                nodos_expandidos = nodos_expandidos,
                profundidad = len(camino_actual) - 1,
                tiempo_ejecucion = time.perf_counter() - inicio
            )

        nodos_expandidos += 1

        for sucesor, costo_sucesor in generar_sucesores(estado_actual, mundo):
            nuevo_costo = costo_actual + costo_sucesor
            clave_sucesor = clave_estado(sucesor)

            if clave_sucesor not in mejores_costos or nuevo_costo < mejores_costos[clave_sucesor]:
                mejores_costos[clave_sucesor] = nuevo_costo
                nueva_prioridad = nuevo_costo + heuristica(sucesor, mundo)

                heapq.heappush(
                    frontera, 
                    (nueva_prioridad, next(contador), nuevo_costo, sucesor, camino_actual + [sucesor.posicion])
                )

    return None  # No se encontró solución