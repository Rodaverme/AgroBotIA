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

def Busqueda_no_informada_por_amplitud(mundo):
    
    inicio = time.perf_counter()

    # Estructura FIFO (Cola) para BFS
    frontera = deque()
    estado_inicial = crear_estado_inicial(mundo)
    nodos_expandidos = 0

    # Se encola: (estado_actual, camino_de_posiciones, costo_acumulado)
    frontera.append((estado_inicial, [estado_inicial.posicion], 0))

    # Para evitar ciclos repetidos
    visitados = {clave_estado(estado_inicial)}

    while frontera:
        estado_actual, camino_actual, costo_actual = frontera.popleft()

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

        # Expansión de sucesores usando el módulo del dominio
        for sucesor, costo_sucesor in generar_sucesores(estado_actual, mundo):
            clave_sucesor = clave_estado(sucesor)

            if clave_sucesor not in visitados:
                visitados.add(clave_sucesor)
                frontera.append((
                    sucesor, 
                    camino_actual + [sucesor.posicion], 
                    costo_actual + costo_sucesor
                ))

    return None  # No se encontró solución


# Ejecución del algoritmo si se ejecuta este archivo directamente
if __name__ == "__main__":
    from pathlib import Path
    ruta = Path(__file__).resolve().parent.parent.parent / "data" / "Prueba1.txt"
    mundo = Mundo.desde_archivo(ruta)
    resultado = Busqueda_no_informada_por_amplitud(mundo)
    
    if resultado:
        print("=== RESULTADO BFS ===")
        print(f"Profundidad: {resultado.profundidad}")
        print(f"Nodos expandidos: {resultado.nodos_expandidos}")
        print(f"Costo: {resultado.costo}")
        print(f"Tiempo: {resultado.tiempo_ejecucion:.6f} s")