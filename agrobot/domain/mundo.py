import json
import sys
from collections import defaultdict

# Ajusta el significado de cada valor según tu problema
LIBRE, OBSTACULO, AGROBOT, CULTIVO_SECO, DEPOSITO, AVIONETA = range(6)

SIGNIFICADO = {
    LIBRE: "casilla libre",
    OBSTACULO: "obstáculo",
    AGROBOT: "AgroBot",
    CULTIVO_SECO: "cultivo seco",
    DEPOSITO: "depósito de fertilizante",
    AVIONETA: "avioneta",
}


class Mundo:
    def __init__(self, matriz):
        if not matriz:
            raise ValueError("La matriz está vacía")
        ancho = len(matriz[0])
        if any(len(fila) != ancho for fila in matriz):
            raise ValueError("Todas las filas deben tener el mismo largo")
        self.matriz = matriz
        self.filas = len(matriz)
        self.columnas = ancho

    @classmethod
    def desde_archivo(cls, ruta):
        """Lee un .txt con números separados por espacios, una fila por línea."""
        matriz = []
        with open(ruta, encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    matriz.append([int(x) for x in linea.split()])
        return cls(matriz)

    def __getitem__(self, pos):
        f, c = pos
        return self.matriz[f][c]

    def en_rango(self, f, c):
        return 0 <= f < self.filas and 0 <= c < self.columnas

    def posiciones(self, valor):
        """Lista de (fila, columna) donde aparece un valor."""
        return [
            (f, c)
            for f in range(self.filas)
            for c in range(self.columnas)
            if self.matriz[f][c] == valor
        ]

    @property
    def agrobot(self):
        pos = self.posiciones(AGROBOT)
        return pos[0] if pos else None

    @property
    def deposito(self):
        pos = self.posiciones(DEPOSITO)
        return pos[0] if pos else None

    @property
    def avioneta(self):
        pos = self.posiciones(AVIONETA)
        return pos[0] if pos else None

    @property
    def cultivos_secos(self):
        return self.posiciones(CULTIVO_SECO)

    def vecinos(self, f, c, bloqueados=(OBSTACULO,)):
        """Casillas adyacentes (arriba, derecha, abajo, izquierda) transitables."""
        for df, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            nf, nc = f + df, c + dc
            if self.en_rango(nf, nc) and self.matriz[nf][nc] not in bloqueados:
                yield nf, nc

    def nombre_celda(self, f, c):
        """Texto legible del contenido de una casilla (útil para la UI)."""
        return SIGNIFICADO[self.matriz[f][c]]

    def es_transitable(self, f, c):
        return self.en_rango(f, c) and self.matriz[f][c] != OBSTACULO

    def copiar(self):
        """Copia independiente, para que cada algoritmo trabaje sin alterar el original."""
        return Mundo([fila[:] for fila in self.matriz])

    def a_lista(self):
        """Matriz como lista de listas, lista para pasarla a la UI."""
        return [fila[:] for fila in self.matriz]

    def a_dict(self):
        return {
            "filas": self.filas,
            "columnas": self.columnas,
            "matriz": self.a_lista(),
            "agrobot": self.agrobot,
            "deposito": self.deposito,
            "avioneta": self.avioneta,
            "cultivos_secos": self.cultivos_secos,
        }

    def a_json(self):
        return json.dumps(self.a_dict(), ensure_ascii=False)

    def resumen(self):
        conteo = defaultdict(int)
        for fila in self.matriz:
            for v in fila:
                conteo[v] += 1
        return dict(sorted(conteo.items()))

    def __str__(self):
        return "\n".join(" ".join(str(v) for v in fila) for fila in self.matriz)


