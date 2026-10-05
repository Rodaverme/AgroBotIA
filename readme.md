# Mundo del AgroBot (`mundo.py`)

Representación del mundo como una matriz, lista para usarse en el algoritmo de búsqueda.

## Formato del archivo de mundo

Un `.txt` con números separados por espacios, una fila por línea. Todas las filas deben tener el mismo largo.

| Valor | Constante | Significado |
|---|---|---|
| 0 | `LIBRE` | Casilla libre |
| 1 | `OBSTACULO` | Obstáculo (muro) |
| 2 | `AGROBOT` | AgroBot |
| 3 | `CULTIVO_SECO` | Cultivo seco |
| 4 | `DEPOSITO` | Depósito de fertilizante |
| 5 | `AVIONETA` | Avioneta |

Las constantes se importan con `from mundo import LIBRE, OBSTACULO, AGROBOT, CULTIVO_SECO, DEPOSITO, AVIONETA`, para no tener que acordarse de los números.

## Convención de coordenadas

Todas las posiciones son tuplas `(fila, columna)`. La fila 0 es la de arriba y la columna 0 la de la izquierda, igual que en el `.txt`.

## Clase `Mundo`

### Crear el mundo

| Función | Qué hace |
|---|---|
| `Mundo.desde_archivo(ruta)` | Lee un `.txt` y devuelve un `Mundo`. Es la forma normal de crearlo. |
| `Mundo(matriz)` | Crea el mundo desde una lista de listas. Lanza `ValueError` si está vacía o si las filas tienen distinto largo. |

### Atributos

| Atributo | Qué es |
|---|---|
| `mundo.filas` | Cantidad de filas |
| `mundo.columnas` | Cantidad de columnas |
| `mundo.matriz` | La matriz (lista de listas). Mejor no modificarla directamente. |

### Elementos clave del mundo

| Propiedad | Devuelve |
|---|---|
| `mundo.agrobot` | `(fila, columna)` del AgroBot, o `None` si no existe |
| `mundo.deposito` | `(fila, columna)` del depósito de fertilizante, o `None` |
| `mundo.avioneta` | `(fila, columna)` de la avioneta, o `None` |
| `mundo.cultivos_secos` | Lista de `(fila, columna)` de todos los cultivos secos |

### Consultar casillas

| Función | Qué hace |
|---|---|
| `mundo[f, c]` | Valor de la casilla (0 a 5). Ejemplo: `mundo[4, 0]` da `2`. |
| `mundo.en_rango(f, c)` | `True` si la posición está dentro de la matriz. |
| `mundo.es_transitable(f, c)` | `True` si está dentro de la matriz y no es obstáculo. |
| `mundo.nombre_celda(f, c)` | Texto del contenido, por ejemplo `"AgroBot"`. |
| `mundo.posiciones(valor)` | Lista de `(fila, columna)` donde aparece un valor. Ejemplo: `mundo.posiciones(CULTIVO_SECO)`. |

### Para el algoritmo de búsqueda

| Función | Qué hace |
|---|---|
| `mundo.vecinos(f, c, bloqueados=(OBSTACULO,))` | Genera las casillas adyacentes (arriba, derecha, abajo, izquierda) que no estén bloqueadas. Por defecto solo los obstáculos bloquean. Si la avioneta u otro elemento también debe bloquear, se pasa en `bloqueados`, por ejemplo `bloqueados=(OBSTACULO, AVIONETA)`. |
| `mundo.copiar()` | Devuelve una copia independiente del mundo, para que un algoritmo trabaje sin alterar el original. |

`vecinos` devuelve un generador. Se recorre con `for` o se convierte con `list(...)`.

### Exportar

| Función | Qué hace |
|---|---|
| `mundo.a_lista()` | La matriz como lista de listas (copia). |
| `mundo.a_dict()` | Diccionario con filas, columnas, matriz y posiciones de AgroBot, depósito, avioneta y cultivos. |
| `mundo.a_json()` | Lo mismo que `a_dict()` pero como texto JSON. Las tuplas salen como listas. |
| `mundo.resumen()` | Diccionario con cuántas veces aparece cada valor. Ejemplo: `{0: 45, 1: 49, ...}`. |
| `print(mundo)` | Imprime la matriz en consola. |

## Ejemplo de uso

```python
from mundo import Mundo

mundo = Mundo.desde_archivo("Prueba1.txt")

inicio = mundo.agrobot            # (4, 0)
metas = mundo.cultivos_secos      # [(4, 3), (5, 3), (6, 8)]

for f, c in mundo.vecinos(*inicio):
    print(f, c, mundo.nombre_celda(f, c))
```

## Notas

- `mundo.py` no necesita ninguna librería externa.
- El bloque `if __name__ == "__main__":` al final es solo una prueba rápida. Se puede borrar sin afectar nada.
- Si el `.txt` tiene filas de distinto largo, `Mundo` lanza `ValueError`.