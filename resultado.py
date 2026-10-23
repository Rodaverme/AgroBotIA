class ResultadoBusqueda:
    """Representa el resultado de una búsqueda, incluyendo el camino encontrado, costo total, nodos expandidos, profundidad y tiempo de ejecución."""

    def __init__(
        self,
        camino,
        costo,
        nodos_expandidos,
        profundidad,
        tiempo_ejecucion
    ):
        """
        Inicializa un resultado de búsqueda.

        Args:
            camino (list): El camino encontrado.
            costo (int or None): El costo total del camino encontrado o None si no aplica.
            nodos_expandidos (int): El número de nodos expandidos durante la búsqueda.
            profundidad (int): La profundidad del camino encontrado.
            tiempo_ejecucion (float): El tiempo de ejecución de la búsqueda.
        """
        self.camino = camino
        self.costo = costo
        self.nodos_expandidos = nodos_expandidos
        self.profundidad = profundidad
        self.tiempo_ejecucion = tiempo_ejecucion