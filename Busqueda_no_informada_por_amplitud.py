import time
from collections import deque


def cargar_mundo(ruta_archivo):
    """Carga la matriz del mundo y extrae las posiciones iniciales."""
    tablero = []
    with open(ruta_archivo, 'r') as f:
        for linea in f:
            linea_limpia = linea.strip()
            if linea_limpia:
                tablero.append([int(x) for x in linea_limpia.split()])
    
    pos_agrobot = None
    deposito = None
    avioneta = None
    cultivos = set()

    for r in range(len(tablero)):
        for c in range(len(tablero[0])):
            val = tablero[r][c]
            if val == 2:
                pos_agrobot = (r, c)
            elif val == 4:
                deposito = (r, c)
            elif val == 5:
                avioneta = (r, c)
            elif val == 3:
                cultivos.add((r, c))

    
    return tablero, pos_agrobot, deposito, avioneta, frozenset(cultivos)
# ==============================================================================



def bfs_agrobot(tablero, inicio, deposito, avioneta, cultivos_iniciales):

    tiempo_inicio = time.time()
    filas = len(tablero)
    columnas = len(tablero[0])

    # Estado: (r, c, fertilizante, combustible_avioneta, en_avioneta, cultivos_pendientes)
    estado_inicial = (inicio[0], inicio[1], 0, 30, False, cultivos_iniciales)

    # La cola almacena tuplas: (estado_actual, camino_de_coordenadas)
    cola = deque([(estado_inicial, [inicio])])
    
    visitados = {estado_inicial}
    nodos_expandidos = 0
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izq, Der

    while cola:
        estado_actual, camino = cola.popleft()
        r, c, fert, comb, en_av, cultivos_pend = estado_actual
        nodos_expandidos += 1

        # Prueba de Objetivo: Se fertilizaron todos los cultivos secos
        if len(cultivos_pend) == 0:
            tiempo_fin = time.time()
            return {
                "solucion": camino,
                "profundidad": len(camino) - 1,
                "nodos_expandidos": nodos_expandidos,
                "tiempo_computo": tiempo_fin - tiempo_inicio
            }

        # Expansión de nodos
        for dr, dc in movimientos:
            nr, nc = r + dr, c + dc

            # Validar límites de la matriz 
            if 0 <= nr < filas and 0 <= nc < columnas and tablero[nr][nc] != 1:
                
                nuevo_fert = fert
                nuevo_comb = comb
                nuevo_en_av = en_av
                nuevos_cultivos = set(cultivos_pend)

                # Regla 1: Subirse a la Avioneta 
                if (nr, nc) == avioneta:
                    nuevo_en_av = True

                # Consumo de combustible si va en avioneta
                if nuevo_en_av:
                    if nuevo_comb > 0:
                        nuevo_comb -= 1
                    else:
                        nuevo_en_av = False  # Combustible agotado

                # Regla 2: Depósito de Fertilizante -> Recarga a 2
                if (nr, nc) == deposito:
                    nuevo_fert = 2

                # Regla 3: Cultivo Seco -> Aplicar fertilizante si posee
                if (nr, nc) in nuevos_cultivos and nuevo_fert > 0:
                    nuevo_fert -= 1
                    nuevos_cultivos.remove((nr, nc))

                nuevo_estado = (nr, nc, nuevo_fert, nuevo_comb, nuevo_en_av, frozenset(nuevos_cultivos))

                if nuevo_estado not in visitados:
                    visitados.add(nuevo_estado)
                    cola.append((nuevo_estado, camino + [(nr, nc)]))

    tiempo_fin = time.time()
    return {
        "solucion": None,
        "profundidad": 0,
        "nodos_expandidos": nodos_expandidos,
        "tiempo_computo": tiempo_fin - tiempo_inicio
    }



if __name__ == "__main__":
    
  
    archivo = "Prueba1.txt"
    tablero, inicio, deposito, avioneta, cultivos_iniciales = cargar_mundo(archivo)
   

    # RUN
    resultado = bfs_agrobot(tablero, inicio, deposito, avioneta, cultivos_iniciales)

    # REPORTE EN CONSOLA
    print("==========================================")
    print("   REPORTE DE BÚSQUEDA POR AMPLITUD (BFS) ")
    print("==========================================")
    if resultado["solucion"]:
        print(f" Nodos expandidos : {resultado['nodos_expandidos']}")
        print(f" Profundidad árbol: {resultado['profundidad']}")
        print(f" Tiempo de cómputo: {resultado['tiempo_computo']:.6f} segundos")
        print("------------------------------------------")
        print(f" Ruta encontrada  : {resultado['solucion']}")
    else:
        print(" No se encontró una solución válida.")
    print("==========================================")