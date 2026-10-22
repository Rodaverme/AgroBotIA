import heapq
import time
from itertools import count
from mundo import Mundo

class ResultadoBusqueda:
    def __init__(
        self,
        camino,
        costo,
        nodos_expandidos,
        profundidad,
        tiempo_ejecucion
    ):
        self.camino = camino
        self.costo = costo
        self.nodos_expandidos = nodos_expandidos
        self.profundidad = profundidad
        self.tiempo_ejecucion = tiempo_ejecucion

class Estado:
    def __init__(
        self,
        posicion,
        cultivos_pendientes,
        fertilizante,
        combustible,
    ):
        self.posicion = posicion
        self.cultivos_pendientes = cultivos_pendientes
        self.fertilizante = fertilizante
        self.combustible = combustible

def crear_estado_inicial(mundo):
    """Crea el estado inicial a partir del mundo."""
    posicion_inicial = mundo.agrobot
    cultivos_pendientes = frozenset(mundo.cultivos_secos)
    fertilizante = 0
    combustible = None 
        
    return Estado(
        posicion_inicial, 
        cultivos_pendientes, 
        fertilizante, 
        combustible
    )

def generar_sucesores(estado, mundo):
    """Genera los estados sucesores a partir del estado actual."""
    sucesores = []
    fila, columna = estado.posicion

    vecinos = mundo.vecinos(fila, columna)

    for vecino in vecinos:

        if vecino == mundo.deposito:
            nuevo_fertilizante = 2
        else:
            nuevo_fertilizante = estado.fertilizante

        nuevos_cultivos = estado.cultivos_pendientes

        if vecino in estado.cultivos_pendientes and nuevo_fertilizante > 0:
            nuevos_cultivos = estado.cultivos_pendientes - {vecino}
            nuevo_fertilizante -= 1

        nuevo_combustible = estado.combustible

        if vecino == mundo.avioneta and estado.combustible is None:
            nuevo_combustible = 30
        elif estado.combustible is not None and estado.combustible > 0:
            nuevo_combustible = estado.combustible - 1

        if estado.combustible is not None and estado.combustible > 0:
            costo = 0.5
        else:
            costo = 1

        nuevo_estado = Estado(
            posicion=vecino,
            cultivos_pendientes=nuevos_cultivos,
            fertilizante=nuevo_fertilizante,
            combustible=nuevo_combustible,
        )
        sucesores.append((nuevo_estado, costo))

    return sucesores

def es_meta(estado):
    """Verifica si el estado es un estado meta."""
    return not estado.cultivos_pendientes

def clave_estado(estado):
    """Genera una clave única para un estado, útil para evitar ciclos."""
    return (
        estado.posicion,
        estado.cultivos_pendientes,
        estado.fertilizante,
        estado.combustible,
    )

def busqueda_costo_uniforme(mundo):

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

if __name__ == "__main__":
    mundo = Mundo.desde_archivo("Prueba1.txt")
    resultado = busqueda_costo_uniforme(mundo)

    if resultado is not None:
        print("Costo:", resultado.costo)
        print("Nodos expandidos:", resultado.nodos_expandidos)
        print("Profundidad:", resultado.profundidad)
        print("Tiempo:", resultado.tiempo_ejecucion)
        print("Camino:", resultado.camino)
    else:
        print("No se encontró solución")