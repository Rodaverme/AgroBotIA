"""
Módulo: problema.py

Descripción: 
    Este módulo define las funciones necesarias para representar y manipular el problema de búsqueda del AgroBot.

Autor: Agarcia07  
Versión: 1.0
"""

# Imports
from estado import Estado

def crear_estado_inicial(mundo):
    """
    Crea el estado inicial del problema a partir del mundo dado.

    Parámetros:
        mundo (Mundo): Una instancia de la clase Mundo que representa el entorno del problema.

    Retorna:
        Estado: Una instancia de la clase Estado que representa el estado inicial del problema.
    """
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
    """
    Genera los estados sucesores a partir del estado actual.

    Parámetros:
        estado (Estado): El estado actual.
        mundo (Mundo): Una instancia de la clase Mundo que representa el entorno del problema.

    Retorna:
        list: Una lista de tuplas, donde cada tupla contiene un estado sucesor y su costo.
    """
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
    """
    Verifica si el estado es un estado meta.

    Parámetros:
        estado (Estado): El estado a verificar.

    Retorna:
        bool: True si el estado es un estado meta, False en caso contrario.
    """
    return not estado.cultivos_pendientes

def clave_estado(estado):
    """
    Genera una clave única para un estado, útil para evitar ciclos.

    Parámetros:
        estado (Estado): El estado para el cual se generará la clave.

    Retorna:
        tuple: Una tupla que representa la clave única del estado.
    """
    return (
        estado.posicion,
        estado.cultivos_pendientes,
        estado.fertilizante,
        estado.combustible,
    )