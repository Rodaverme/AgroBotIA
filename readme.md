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

# Proyecto Algoritmos de Búsqueda

Aplicación de escritorio en Python (Tkinter) que carga un mapa tipo cuadrícula desde un archivo de texto y lo muestra visualmente. Permite elegir entre distintos algoritmos de búsqueda **no informada** e **informada** para resolver el problema planteado en el mundo (un robot que debe moverse por el mapa esquivando obstáculos).

## Características

- Interfaz gráfica con Tkinter / ttk.
- Carga del mundo desde un archivo `.txt` mediante el módulo `mundo`.
- Dibujo del tablero en un `Canvas`, con muros, robot y elementos especiales representados con emojis.
- Selección dinámica del algoritmo: el segundo menú se actualiza según el tipo de búsqueda elegido.

## Algoritmos disponibles

| Tipo de búsqueda | Algoritmos |
|------------------|------------|
| No informada     | Amplitud, Costo uniforme, Profundidad evitando ciclos |
| Informada        | Avara, A* |

> **Estado actual:** la interfaz ya permite seleccionar el algoritmo y presionar **Ejecutar Búsqueda**, pero por ahora el botón solo imprime en consola el algoritmo y tipo elegidos. La implementación de cada algoritmo está pendiente de conectarse en el método `ejecutar_busqueda`.

## Requisitos

- Python 3.8 o superior
- Tkinter (incluido por defecto en la instalación estándar de Python en Windows y macOS)
  - En Linux (Debian/Ubuntu): `sudo apt install python3-tk`
- La fuente **Segoe UI Emoji** para ver correctamente los íconos (viene con Windows; en otros sistemas se usará una fuente alternativa).

No se requieren librerías externas.

## Estructura del proyecto

```
.
├── interfaz.py     # Interfaz gráfica (este archivo)
├── mundo.py        # Módulo con la clase Mundo (carga y representación del mapa)
├── Prueba1.txt     # Archivo con la descripción del mapa
└── README.md
```

> `Prueba1.txt` debe estar en la misma carpeta que `interfaz.py`, ya que la ruta se construye a partir de la ubicación del script.

## Uso

1. Clona o descarga el proyecto.
2. Asegúrate de que `interfaz.py`, `mundo.py` y `Prueba1.txt` estén en la misma carpeta.
3. Ejecuta:

```bash
python interfaz.py
```

4. En la ventana:
   1. Elige el **Tipo de búsqueda** (No informada / Informada).
   2. Elige el **Algoritmo** específico.
   3. Presiona **Ejecutar Búsqueda**.

## Representación del mapa

El método `Mundo.a_lista()` devuelve una matriz donde cada celda es un código numérico, que la interfaz dibuja así:

| Código | Elemento   | Representación              |
|--------|------------|-----------------------------|
| `0`    | Casilla libre | Celda blanca             |
| `1`    | Obstáculo (muro) | Celda gris            |
| `2`    | Robot      | 🤖                          |
| `3`    | Planta secándose | 🍂                    |
| `4`    | Gasolina   | ⛽                          |
| `5`    | Avión      | ✈️                          |

El tamaño de cada celda es de 45 px y las dimensiones del canvas se calculan automáticamente según el número de filas y columnas del mapa.

## Descripción del código

- **`BusquedaApp`**: clase principal de la aplicación.
  - `__init__`: construye el panel de controles, carga el mundo desde `Prueba1.txt` y crea el canvas.
  - `actualizar_algoritmos`: actualiza el combo de algoritmos según el tipo de búsqueda seleccionado.
  - `dibujar_tablero`: recorre la matriz y dibuja celdas, muros e íconos.
  - `ejecutar_busqueda`: punto de entrada para ejecutar el algoritmo elegido (pendiente de implementar).

## Próximos pasos

- Implementar los algoritmos de búsqueda y conectarlos al botón **Ejecutar Búsqueda**.
- Animar el recorrido del robot sobre el tablero.
- Mostrar métricas de la búsqueda (nodos expandidos, costo de la solución, profundidad, tiempo de cómputo).