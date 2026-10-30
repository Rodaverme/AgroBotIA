import time
import heapq
from agrobot.domain.mundo import Mundo
from agrobot.busqueda.Costo.resultado import ResultadoBusqueda
from agrobot.domain.problema import (
    crear_estado_inicial,
    generar_sucesores,
    es_meta,
    clave_estado,
)

def distancia_manhattan (pos1, pos2):
    """calculamos la heuristica mediante la formula
    h(n) = (|fi - f2| + |c1 - c2|)/2
    Tomamos el resultado de las diferencias absolutas
    y luego las dividimos entre dos"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

#print(distancia_manhattan((1,3),(4,7)))

def heuristica(estado, mundo):
    if not estado.cultivos_pendientes:
        return 0.0

    pos_actual = estado.posicion

    if estado.combustible == 0 and mundo.avioneta:
        base_h = distancia_manhattan(pos_actual, mundo.avioneta)

    elif estado.fertilizante == 0 and mundo.deposito:
        dist_al_deposito = distancia_manhattan(pos_actual, mundo.deposito)
        dist_deposito_a_cultivo = distancia_manhattan(pos_actual, mundo.deposito)
        dist_deposito_a_cultivo = min(distancia_manhattan(mundo.deposito, c) for c in estado.cultivos_pendientes)
        base_h = dist_al_deposito + dist_deposito_a_cultivo

    else:
        base_h = min(
            distancia_manhattan(pos_actual, c) for c in estado.cultivos_pendientes
        )

    #verifica si en el mundo hay avioneta y divide distancia manhattan en 2
    if mundo.avioneta:
        return base_h / 2.0
    else:
        return float(base_h)

def busqueda_Avara(mundo):

    tiempo_inicio = time.time()

    estado_inicial = crear_estado_inicial(mundo)

    contador = 0

    h_init = heuristica(estado_inicial, mundo)
    frontera = []
    heapq.heappush(frontera, (h_init, contador, estado_inicial, [estado_inicial.posicion], 0, 0))

    visitados = set()
    nodos_expandidos = 0

    while frontera:
        #extraemos el nodo con menor heuristica h(n) con heapq.heappop
        h_val, _, estado_actual, camino, costo_actual, profundidad = heapq.heappop(frontera)

        clave = clave_estado (estado_actual)
        if clave in visitados:
            continue

        visitados.add(clave)

        #en caso de que se encuentre la meta
        if es_meta (estado_actual):
            tiempo_ejecucion = time.time() - tiempo_inicio
            return ResultadoBusqueda(
                camino=camino,
                costo=costo_actual,
                nodos_expandidos=nodos_expandidos,
                profundidad=profundidad,
                tiempo_ejecucion=tiempo_ejecucion
            )

        nodos_expandidos += 1

        #generar sucesores 
        for nuevo_estado, costo_paso in generar_sucesores(estado_actual, mundo):
            nueva_clave = clave_estado(nuevo_estado)

            if nueva_clave not in visitados:
                h_sucesor = heuristica (nuevo_estado, mundo)
                contador +=1

                nuevo_camino = camino + [nuevo_estado.posicion]
                nuevo_costo = costo_actual + costo_paso
                nueva_profundidad = profundidad +1

                #ordenamos la frontera unicamente por h_sucesor
                heapq.heappush(
                    frontera,
                    (h_sucesor, contador, nuevo_estado, nuevo_camino, nuevo_costo, nueva_profundidad)
                )

    tiempo_ejecucion = time.time() - tiempo_inicio
    return ResultadoBusqueda(
        camino=[],
        costo=None,
        nodos_expandidos=nodos_expandidos,
        profundidad=0,
        tiempo_ejecucion=tiempo_ejecucion
    )
