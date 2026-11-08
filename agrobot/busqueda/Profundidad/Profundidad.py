import time
from collections import deque
from agrobot.domain.mundo import Mundo
from agrobot.busqueda.Costo.resultado import ResultadoBusqueda
from agrobot.domain.problema import (
    crear_estado_inicial,
    generar_sucesores,
    es_meta,
    clave_estado,
)

def Busqueda_no_informada_por_profundidad(mundo):
    inicio = time.perf_counter()

    frontera = deque()
    estado_inicial = crear_estado_inicial(mundo)
    nodos_expandidos = 0

    # Apilamos: (estado_actual, camino_de_posiciones, costo_acumulado, conjunto_camino_visitados)
    frontera.append((estado_inicial, [estado_inicial.posicion], 0, {clave_estado(estado_inicial)}))

    while frontera:
        estado_actual, camino_actual, costo_actual, visitados_camino = frontera.pop()

        # Prueba de objetivo
        if es_meta(estado_actual):
            return ResultadoBusqueda(
                camino=camino_actual,
                costo=costo_actual,
                nodos_expandidos=nodos_expandidos,
                profundidad=len(camino_actual) - 1,
                tiempo_ejecucion=time.perf_counter() - inicio
            )

        nodos_expandidos += 1

        for sucesor, costo_sucesor in generar_sucesores(estado_actual, mundo):
            clave_sucesor = clave_estado(sucesor)

            # Evita ciclos dentro de la misma rama activa
            if clave_sucesor not in visitados_camino:
                nuevo_visitados = set(visitados_camino)
                nuevo_visitados.add(clave_sucesor)
                
                frontera.append((
                    sucesor, 
                    camino_actual + [sucesor.posicion], 
                    costo_actual + costo_sucesor,
                    nuevo_visitados
                ))

    return None