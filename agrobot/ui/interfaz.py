
import tkinter as tk
from tkinter import ttk
import agrobot.domain.mundo as mundo


class BusquedaApp:
    """
    Interfaz de búsqueda.

    Recibe en `algoritmos` un diccionario con la forma:
        {
            "No informada": {"Amplitud": funcion, "Costo uniforme": funcion, ...},
            "Informada":    {"Avara": funcion, "A*": funcion},
        }

    Cada función recibe el objeto Mundo y devuelve un objeto/dict/lista con:
      - camino: lista de posiciones [(fila, col), ...]  (obligatorio)
      - costo, nodos_expandidos, profundidad, tiempo_ejecucion (opcionales)
    """

    SUBPASOS = 6  # fotogramas de interpolación entre una casilla y la siguiente
    NOMBRES_CASILLA = {0: "libre", 2: "inicio", 3: "cultivo", 4: "recarga", 5: "avioneta"}

    def __init__(self, root, algoritmos=None, ruta_mapa=None):
        self.root = root
        self.root.title("Proyecto Algoritmos de Búsqueda")
        self.root.geometry("980x680")
        self.root.resizable(False, False)

        self.algoritmos = algoritmos or {}
        self.after_id = None  # para cancelar la animación anterior
        self.camino = []
        self.visitas = {}
        self.recargas = 0
        self.cultivos_vistos = set()
        self.robot_item = None

        # --- PANEL SUPERIOR DE CONTROLES ---
        frame_controles = ttk.LabelFrame(self.root, text=" Configuración de Búsqueda ", padding=10)
        frame_controles.pack(fill="x", padx=15, pady=10)

        ttk.Label(frame_controles, text="Tipo de búsqueda:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_tipo = ttk.Combobox(
            frame_controles,
            values=list(self.algoritmos.keys()),
            state="readonly",
            width=20
        )
        self.combo_tipo.grid(row=0, column=1, padx=5, pady=5)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.actualizar_algoritmos)

        ttk.Label(frame_controles, text="Algoritmo:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.combo_algoritmo = ttk.Combobox(frame_controles, state="readonly", width=25)
        self.combo_algoritmo.grid(row=0, column=3, padx=5, pady=5)

        btn_ejecutar = ttk.Button(frame_controles, text="Ejecutar Búsqueda", command=self.ejecutar_busqueda)
        btn_ejecutar.grid(row=0, column=4, padx=15, pady=5)

        if self.algoritmos:
            self.combo_tipo.current(0)
            self.actualizar_algoritmos()

        # --- CARGA DEL MUNDO ---
       

        self.objeto_mundo = mundo.Mundo.desde_archivo(str(ruta_mapa))
        self.grid_data = self.objeto_mundo.a_lista()

        self.cell_size = 45
        self.rows = len(self.grid_data)
        self.cols = len(self.grid_data[0])

        # Casilla inicial del robot (valor 2) y total de cultivos (valor 3)
        self.inicio = (0, 0)
        self.total_cultivos = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid_data[r][c] == 2:
                    self.inicio = (r, c)
                elif self.grid_data[r][c] == 3:
                    self.total_cultivos += 1

        # --- ZONA CENTRAL: tablero (izquierda) + estado (derecha) ---
        frame_central = ttk.Frame(self.root)
        frame_central.pack(expand=True, fill="both", padx=15)

        frame_matriz = ttk.Frame(frame_central)
        frame_matriz.pack(side="left", anchor="n")

        self.canvas = tk.Canvas(
            frame_matriz,
            width=self.cols * self.cell_size,
            height=self.rows * self.cell_size,
            bg="white",
            highlightthickness=1,
            highlightbackground="black"
        )
        self.canvas.pack(pady=5)

        self.lbl_resultado = ttk.Label(frame_matriz, text="", justify="center", wraplength=450)
        self.lbl_resultado.pack(pady=5)

        frame_info = ttk.LabelFrame(frame_central, text=" Estado del AgroBot ", padding=10)
        frame_info.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=5)

        self.lbl_estado = ttk.Label(frame_info, text="Aún no hay una búsqueda ejecutada.",
                                    justify="left", font=("Consolas", 10))
        self.lbl_estado.pack(anchor="w")

        frame_vel = ttk.Frame(frame_info)
        frame_vel.pack(fill="x", pady=10)
        ttk.Label(frame_vel, text="Velocidad:").pack(side="left")
        self.var_vel = tk.DoubleVar(value=5)
        ttk.Scale(frame_vel, from_=1, to=10, variable=self.var_vel, orient="horizontal").pack(
            side="left", fill="x", expand=True, padx=8)

        ttk.Label(frame_info, text="Eventos del recorrido:").pack(anchor="w")
        frame_log = ttk.Frame(frame_info)
        frame_log.pack(fill="both", expand=True)
        scroll = ttk.Scrollbar(frame_log, orient="vertical")
        self.txt_log = tk.Text(frame_log, height=16, width=38, wrap="word", state="disabled",
                               font=("Segoe UI Emoji", 10), yscrollcommand=scroll.set)
        scroll.config(command=self.txt_log.yview)
        scroll.pack(side="right", fill="y")
        self.txt_log.pack(side="left", fill="both", expand=True)

        self.dibujar_tablero()

    # ------------------------------------------------------------------
    def actualizar_algoritmos(self, event=None):
        """Actualiza el segundo combobox según la categoría elegida."""
        tipo = self.combo_tipo.get()
        nombres = list(self.algoritmos.get(tipo, {}).keys())
        self.combo_algoritmo['values'] = nombres
        if nombres:
            self.combo_algoritmo.current(0)
        else:
            self.combo_algoritmo.set("")

    def _centro(self, celda):
        r, c = celda
        return (c + 0.5) * self.cell_size, (r + 0.5) * self.cell_size

    def dibujar_tablero(self, visitas=None, robot_celda=None):
        """
        Dibuja la cuadrícula. Las casillas visitadas se pintan más oscuras
        mientras más veces pasa el robot por ellas (y muestran 'xN').
        El robot se dibuja en `robot_celda` (o en la casilla inicial).
        """
        self.canvas.delete("all")
        visitas = visitas or {}

        simbolos = {
            4: ("⛽", "#4CAF50"),
            5: ("✈️", "#9C27B0"),
            3: ("🍂", "#FF9800"),
        }
        colores_visita = {1: "#FFF59D", 2: "#FFCC80"}

        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                val = self.grid_data[r][c]
                n = visitas.get((r, c), 0)

                if val == 1:
                    relleno = "#707070"
                elif n == 0:
                    relleno = "white"
                else:
                    relleno = colores_visita.get(n, "#FF8A65")
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=relleno, outline="black")

                if val in simbolos:
                    texto, color = simbolos[val]
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=texto,
                                            font=("Segoe UI Emoji", 18), fill=color)

                if n > 1 and val != 1:
                    self.canvas.create_text(x2 - 3, y1 + 2, text=f"x{n}", anchor="ne",
                                            font=("Segoe UI", 8, "bold"), fill="#555555")

        cx, cy = self._centro(robot_celda or self.inicio)
        self.robot_item = self.canvas.create_text(cx, cy, text="🤖",
                                                  font=("Segoe UI Emoji", 20), fill="#2196F3")

    # ------------------------------------------------------------------
    def log(self, texto):
        self.txt_log.config(state="normal")
        self.txt_log.insert("end", texto + "\n")
        self.txt_log.see("end")
        self.txt_log.config(state="disabled")

    def limpiar_log(self):
        self.txt_log.config(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.config(state="disabled")

    def ejecutar_busqueda(self):
        """Busca la función elegida en los combos, la ejecuta y anima el recorrido."""
        tipo = self.combo_tipo.get()
        nombre = self.combo_algoritmo.get()

        funcion = self.algoritmos.get(tipo, {}).get(nombre)
        if funcion is None:
            self.lbl_resultado.config(text="Selecciona un algoritmo válido.")
            return

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        print(f"Ejecutando algoritmo '{nombre}' de tipo '{tipo}'...")
        try:
            resultado = funcion(self.objeto_mundo)
        except Exception as e:
            self.lbl_resultado.config(text=f"Error en '{nombre}': {e}")
            raise

        # Normalizar el resultado (objeto, dict o lista)
        if isinstance(resultado, dict):
            datos = dict(resultado)
        elif hasattr(resultado, "__dict__"):
            datos = dict(vars(resultado))
        else:
            datos = {"camino": resultado}

        camino = datos.pop("camino", None) or []

        if not camino:
            self.dibujar_tablero()
            self.limpiar_log()
            self.lbl_estado.config(text="Sin solución.")
            self.lbl_resultado.config(text=f"{nombre}: no se encontró solución.")
            return

        etiquetas = {
            "costo": "costo",
            "nodos_expandidos": "nodos expandidos",
            "profundidad": "profundidad",
            "tiempo_ejecucion": "tiempo",
        }
        partes = []
        for clave, etiqueta in etiquetas.items():
            if clave in datos:
                valor = datos[clave]
                if clave == "tiempo_ejecucion":
                    valor = f"{valor:.4f} s"
                partes.append(f"{etiqueta}: {valor}")

        texto = f"{nombre}  |  pasos: {len(camino) - 1}"
        if partes:
            texto += "\n" + "  |  ".join(partes)
        self.lbl_resultado.config(text=texto)

        self.iniciar_animacion(list(camino))

    # ------------------------------------------------------------------
    def iniciar_animacion(self, camino):
        self.camino = camino
        self.visitas = {}
        self.recargas = 0
        self.cultivos_vistos = set()
        self.limpiar_log()

        self.registrar_paso(0)
        self.dibujar_tablero(self.visitas, camino[0])

        if len(camino) > 1:
            self.after_id = self.root.after(300, self.mover, 1, 1)
        else:
            self.after_id = None

    def registrar_paso(self, i):
        """Actualiza contadores, panel de estado y registro de eventos al llegar al paso i."""
        pos = self.camino[i]
        r, c = pos
        val = self.grid_data[r][c]

        self.visitas[pos] = self.visitas.get(pos, 0) + 1
        n = self.visitas[pos]
        repetida = f" (pasada {n})" if n > 1 else ""

        if i == 0:
            self.log(f"Inicio en {pos}")
        if val == 3:
            self.cultivos_vistos.add(pos)
            self.log(f"Paso {i}: 🍂 cultivo en {pos}{repetida}")
        elif val == 4:
            self.recargas += 1
            self.log(f"Paso {i}: ⛽ punto de recarga en {pos}{repetida}")
        elif val == 5:
            self.log(f"Paso {i}: ✈️ avioneta en {pos}{repetida}")

        self.lbl_estado.config(text=(
            f"Paso:               {i} / {len(self.camino) - 1}\n"
            f"Posición:           {pos}\n"
            f"Casilla:            {self.NOMBRES_CASILLA.get(val, 'libre')}\n"
            f"Cultivos visitados: {len(self.cultivos_vistos)} / {self.total_cultivos}\n"
            f"Pasadas por recarga: {self.recargas}"
        ))

    def mover(self, i, sub):
        """Mueve el robot suavemente de camino[i-1] a camino[i] en SUBPASOS fotogramas."""
        x0, y0 = self._centro(self.camino[i - 1])
        x1, y1 = self._centro(self.camino[i])
        t = sub / self.SUBPASOS
        self.canvas.coords(self.robot_item, x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)

        duracion = int(660 / max(1.0, self.var_vel.get()))  # ms por casilla
        frame_ms = max(8, duracion // self.SUBPASOS)

        if sub < self.SUBPASOS:
            self.after_id = self.root.after(frame_ms, self.mover, i, sub + 1)
            return

        # Llegó a la casilla i
        self.registrar_paso(i)
        self.dibujar_tablero(self.visitas, self.camino[i])

        if i + 1 < len(self.camino):
            self.after_id = self.root.after(frame_ms, self.mover, i + 1, 1)
        else:
            self.after_id = None
            self.log("Fin del recorrido")


