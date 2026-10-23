import tkinter as tk
from pathlib import Path

from agrobot.busqueda import costo
from agrobot.ui.interfaz import BusquedaApp

DATA_DIR = Path(__file__).parent / "data"


def pendiente(m):
    return []


def main():
    algoritmos = {
        "No informada": {
            "Amplitud": pendiente,
            "Costo uniforme": costo.busqueda_costo_uniforme,
            "Profundidad evitando ciclos": pendiente,
        },
        "Informada": {
            "Avara": pendiente,
            "A*": pendiente,
        },
    }

    root = tk.Tk()
    BusquedaApp(root, algoritmos, ruta_mapa=DATA_DIR / "Prueba1.txt")
    root.mainloop()


if __name__ == "__main__":
    main()