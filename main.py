import tkinter as tk
from pathlib import Path

from agrobot.busqueda.Costo import costo
from agrobot.busqueda.Amplitud.Amplitud import Busqueda_no_informada_por_amplitud
from agrobot.busqueda.Profundidad.Profundidad import Busqueda_no_informada_por_profundidad
from agrobot.busqueda.Avara.Avara import busqueda_Avara
from agrobot.busqueda.A_estrella.A_estrella import busqueda_A_estrella
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
            "Profundidad evitando ciclos": Busqueda_no_informada_por_profundidad,
        },
        "Informada": {
            "Avara": busqueda_Avara,
            "A*": busqueda_A_estrella,
        },
    }

    root = tk.Tk()
    BusquedaApp(root, algoritmos, ruta_mapa=DATA_DIR / "Prueba3.txt")
    root.mainloop()


if __name__ == "__main__":
    main()