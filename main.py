import tkinter as tk
from pathlib import Path

from agrobot.busqueda.Costo import costo
from agrobot.busqueda.Amplitud.Amplitud import Busqueda_no_informada_por_amplitud
from agrobot.busqueda.Avara.Avara import busqueda_Avara
from agrobot.ui.interfaz import BusquedaApp
# En main.py cambiar esta línea:


DATA_DIR = Path(__file__).parent / "data"


def pendiente(m):
    return []


def main():
    algoritmos = {
        "No informada": {
            "Amplitud": Busqueda_no_informada_por_amplitud,
            "Costo uniforme": costo.busqueda_costo_uniforme,
            "Profundidad evitando ciclos": pendiente,
        },
        "Informada": {
            "Avara": busqueda_Avara,
            "A*": pendiente,
        },
    }

    root = tk.Tk()
    BusquedaApp(root, algoritmos, ruta_mapa=DATA_DIR / "Prueba3.txt")
    root.mainloop()


if __name__ == "__main__":
    main()