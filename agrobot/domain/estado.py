class Estado:
    """Representa un estado en el problema con posición, cultivos pendientes, fertilizante y combustible."""

    def __init__(
        self,
        posicion,
        cultivos_pendientes,
        fertilizante,
        combustible,
    ):
        """
        Inicializa un estado.

        Args:
            posicion (tuple): La posición actual del robot (fila, columna).
            cultivos_pendientes (frozenset): Un conjunto de posiciones de cultivos secos pendientes.
            fertilizante (int): La cantidad de fertilizante disponible.
            combustible (int or None): La cantidad de combustible disponible o None si no se ha recogido.
        """
        self.posicion = posicion
        self.cultivos_pendientes = cultivos_pendientes
        self.fertilizante = fertilizante
        self.combustible = combustible
        