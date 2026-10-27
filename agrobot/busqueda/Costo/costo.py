"""
Módulo: costo.py

Descripción:
    Este módulo implementa el algoritmo de búsqueda de costo uniforme para el problema del AgroBot.

Autor: Agarcia07
Versión: 1.0
"""

# Imports
import heapq
import time
from itertools import count
from agrobot.domain.mundo import Mundo
from agrobot.busqueda.Costo.resultado import ResultadoBusqueda
from agrobot.domain.problema import (
    crear_estado_inicial,
    generar_sucesores,
    es_meta,
    clave_estado,
)

def busqueda_costo_uniforme(mundo):
    """
    Implementa el algoritmo de búsqueda de costo uniforme para encontrar el camino óptimo en el problema del AgroBot.

    Parámetros:
        mundo (Mundo): Una instancia de la clase Mundo que representa el entorno del problema.

    Retorna:
        ResultadoBusqueda: El resultado de la búsqueda si se encuentra una solución.
        None: En caso contrario.
    """
    inicio = time.perf_counter()

    contador = count()  # Contador para desempatar nodos con el mismo costo
    frontera = []  # Cola de prioridad para los nodos a explorar
    estado_inicial = crear_estado_inicial(mundo)
    nodos_expandidos = 0  # Contador de nodos expandidos

    heapq.heappush(
        frontera, 
        (0, next(contador), estado_inicial, [estado_inicial.posicion])
    )

    mejores_costos = {
        clave_estado(estado_inicial): 0
    }

    while frontera:
        costo_actual, desempate, estado_actual, camino_actual = heapq.heappop(frontera)

        if clave_estado(estado_actual) in mejores_costos and costo_actual > mejores_costos[clave_estado(estado_actual)]:
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
                heapq.heappush(
                    frontera, 
                    (nuevo_costo, next(contador), sucesor, camino_actual + [sucesor.posicion])
                )    

    return None # No se encontró solución

# Ejecución del algoritmo si se ejecuta este archivo directamente
if __name__ == "__main__":
    from pathlib import Path
    ruta = Path(__file__).resolve().parent[2]/"data"/"Prueba1.txt"
    mundo = Mundo.desde_archivo(ruta)
    