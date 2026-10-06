import os
import tkinter as tk
from tkinter import ttk
import mundo

class BusquedaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Algoritmos de Búsqueda")
        self.root.geometry("800x650")
        self.root.resizable(False, False)

        # Diccionario de algoritmos según la categoría
        self.opciones_algoritmos = {
            "No informada": ["Amplitud", "Costo uniforme", "Profundidad evitando ciclos"],
            "Informada": ["Avara", "A"]
        }

        # --- PANEL SUPERIOR DE CONTROLES ---
        frame_controles = ttk.LabelFrame(self.root, text=" Configuración de Búsqueda ", padding=10)
        frame_controles.pack(fill="x", padx=15, pady=10)

        # Combo 1: Tipo de búsqueda
        ttk.Label(frame_controles, text="Tipo de búsqueda:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_tipo = ttk.Combobox(
            frame_controles, 
            values=list(self.opciones_algoritmos.keys()), 
            state="readonly",
            width=20
        )
        self.combo_tipo.grid(row=0, column=1, padx=5, pady=5)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.actualizar_algoritmos)

        # Combo 2: Algoritmo específico
        ttk.Label(frame_controles, text="Algoritmo:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.combo_algoritmo = ttk.Combobox(frame_controles, state="readonly", width=25)
        self.combo_algoritmo.grid(row=0, column=3, padx=5, pady=5)

        # Botón de ejecución
        btn_ejecutar = ttk.Button(frame_controles, text="Ejecutar Búsqueda", command=self.ejecutar_busqueda)
        btn_ejecutar.grid(row=0, column=4, padx=15, pady=5)

        # Seleccionar la primera opción por defecto
        self.combo_tipo.current(0)
        self.actualizar_algoritmos()

        # --- PANEL DEL TABLERO (MATRIZ) ---
        frame_matriz = ttk.Frame(self.root, padding=10)
        frame_matriz.pack(expand=True, fill="both")

        # 1. Obtener la ruta exacta del archivo .txt en la misma carpeta que interfaz.py
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_txt = os.path.join(directorio_actual, "Prueba1.txt")

        # Representación de la imagen (10x10):
        # 0 = Libre, 1 = Muro (Gris), 
        # 'R' = Robot, 'G' = Gasolina, 'A' = Avión, 'P' = Planta secándose
        # 2. Cargar el objeto Mundo desde la ruta absoluta y obtener la lista/matriz
        self.objeto_mundo = mundo.Mundo.desde_archivo(ruta_txt)
        self.grid_data = self.objeto_mundo.a_lista()
        # Configuración del Canvas para dibujar la matriz
        self.cell_size = 45
        self.rows = len(self.grid_data)
        self.cols = len(self.grid_data[0])
        
        self.canvas = tk.Canvas(
            frame_matriz, 
            width=self.cols * self.cell_size, 
            height=self.rows * self.cell_size, 
            bg="white",
            highlightthickness=1,
            highlightbackground="black"
        )
        self.canvas.pack(anchor="center", pady=10)

        self.dibujar_tablero()

    def actualizar_algoritmos(self, event=None):
        """Actualiza el segundo combobox según la selección del primero."""
        tipo_seleccionado = self.combo_tipo.get()
        algoritmos = self.opciones_algoritmos.get(tipo_seleccionado, [])
        self.combo_algoritmo['values'] = algoritmos
        if algoritmos:
            self.combo_algoritmo.current(0)

    def dibujar_tablero(self):
        """Dibuja la cuadrícula, obstáculos y elementos del mapa."""
        simbolos = {
            2: ("🤖", "#2196F3"),
            4: ("⛽", "#4CAF50"),
            5: ("✈️", "#9C27B0"),
            3: ("🍂", "#FF9800")
        }

        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                val = self.grid_data[r][c]

                # Dibujar Muros (1) o Casillas Libres (0 y otros)
                if val == 1:  # OBSTACULO
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#707070", outline="black")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

                # Dibujar íconos si la casilla contiene un elemento especial
                if val in simbolos:
                    texto, color = simbolos[val]
                    self.canvas.create_text(
                        (x1 + x2) / 2, 
                        (y1 + y2) / 2, 
                        text=texto, 
                        font=("Segoe UI Emoji", 18),
                        fill=color
                    )

    def ejecutar_busqueda(self):
        """Acción cuando el usuario presiona el botón ejecutar."""
        tipo = self.combo_tipo.get()
        algoritmo = self.combo_algoritmo.get()
        print(f"Ejecutando algoritmo '{algoritmo}' de tipo '{tipo}'...")

if __name__ == "__main__":
    root = tk.Tk()
    app = BusquedaApp(root)
    root.mainloop()