# plotter.py - Graficador interactivo con Tkinter Canvas
# Soporta: pan (arrastre), zoom (rueda), cónicas y funciones por tramos
# No usa numpy, matplotlib ni librerías matemáticas externas

import tkinter as tk


class Plotter:
    """Graficador interactivo. Dibuja cónicas y funciones en un Canvas."""

    def __init__(self, canvas):
        self.canvas = canvas
        self.scale = 40          # Píxeles por unidad matemática
        self.offset_x = 0        # Desplazamiento horizontal del origen
        self.offset_y = 0        # Desplazamiento vertical del origen
        self.tipo = None         # "conica" o "funcion"
        self.data = None         # Datos matemáticos a graficar
        self._drag_x = 0
        self._drag_y = 0

        # Eventos de interacción
        canvas.bind("<Configure>", lambda e: self._dibujar())
        canvas.bind("<ButtonPress-1>", self._inicio_arrastre)
        canvas.bind("<B1-Motion>", self._arrastrar)
        canvas.bind("<Button-4>", lambda e: self._zoom(5))      # Linux scroll up
        canvas.bind("<Button-5>", lambda e: self._zoom(-5))     # Linux scroll down
        canvas.bind("<MouseWheel>", lambda e: self._zoom(5 if e.delta > 0 else -5))

    # --- Interacción ---

    def _inicio_arrastre(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _arrastrar(self, event):
        self.offset_x += event.x - self._drag_x
        self.offset_y += event.y - self._drag_y
        self._drag_x = event.x
        self._drag_y = event.y
        self._dibujar()

    def _zoom(self, delta):
        self.scale = max(10, min(200, self.scale + delta))
        self._dibujar()

    # --- Conversión de coordenadas ---

    def _cx(self):
        """Centro X del origen (0,0) en píxeles."""
        return self.canvas.winfo_width() // 2 + self.offset_x

    def _cy(self):
        """Centro Y del origen (0,0) en píxeles."""
        return self.canvas.winfo_height() // 2 + self.offset_y

    def _px(self, x):
        """X matemático → X píxeles."""
        return self._cx() + x * self.scale

    def _py(self, y):
        """Y matemático → Y píxeles (invertido)."""
        return self._cy() - y * self.scale

    # --- Punto de entrada ---

    def set_data(self, tipo, data):
        """Guarda los datos y dibuja."""
        self.tipo = tipo
        self.data = data
        self._dibujar()

    # --- Dibujo principal ---

    def _dibujar(self):
        """Redibuja todo: fondo, cuadrícula, ejes y gráfica."""
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        # Fondo
        self.canvas.create_rectangle(-2, -2, w + 4, h + 4, fill="#f8f9fa", outline="")

        # Cuadrícula
        cx, cy = self._cx(), self._cy()
        for x in range(int((0 - cx) / self.scale) - 1, int((w - cx) / self.scale) + 2):
            px = self._px(x)
            self.canvas.create_line(px, 0, px, h, fill="#e0e0e0", dash=(2, 4))
        for y in range(int((cy - h) / self.scale) - 1, int((cy) / self.scale) + 2):
            py = self._py(y)
            self.canvas.create_line(0, py, w, py, fill="#e0e0e0", dash=(2, 4))

        # Ejes
        self.canvas.create_line(0, cy, w, cy, fill="#495057", width=2)
        self.canvas.create_line(cx, 0, cx, h, fill="#495057", width=2)

        # Números en los ejes
        for x in range(int((0 - cx) / self.scale), int((w - cx) / self.scale) + 1):
            if x != 0:
                px = self._px(x)
                self.canvas.create_line(px, cy - 4, px, cy + 4, fill="#495057")
                self.canvas.create_text(px, cy + 14, text=str(x), fill="#6c757d", font=("Arial", 8))
        for y in range(int((cy - h) / self.scale), int(cy / self.scale) + 1):
            if y != 0:
                py = self._py(y)
                self.canvas.create_line(cx - 4, py, cx + 4, py, fill="#495057")
                self.canvas.create_text(cx - 14, py, text=str(y), fill="#6c757d", font=("Arial", 8))

        # Gráfica matemática
        if self.tipo == "conica" and self.data:
            self._dibujar_conica()
        elif self.tipo == "funcion" and self.data:
            self._dibujar_funcion()

    # --- Cónicas ---

    def _dibujar_conica(self):
        """Dibuja la cónica según su tipo."""
        tipo = self.data.get("tipo", "")
        centro = self.data.get("centro")
        params = self.data.get("parametros", {})
        if not centro:
            return
        h, k = centro
        color = "#007bff"

        if tipo == "Circunferencia":
            r = params.get("r", 0)
            self.canvas.create_oval(
                self._px(h - r), self._py(k + r),
                self._px(h + r), self._py(k - r),
                outline=color, width=2)
            self._punto(h, k, "Centro")

        elif tipo == "Elipse":
            a = params.get("a2", 0) ** 0.5
            b = params.get("b2", 0) ** 0.5
            self.canvas.create_oval(
                self._px(h - a), self._py(k + b),
                self._px(h + a), self._py(k - b),
                outline=color, width=2)
            self._punto(h, k, "Centro")

        elif tipo == "Hipérbola":
            a = params.get("a2", 0) ** 0.5
            b = params.get("b2", 0) ** 0.5
            rama_d, rama_i = [], []
            t = a
            while t <= 25:
                val = ((t ** 2) / (a ** 2)) - 1
                if val >= 0:
                    yv = (val * b ** 2) ** 0.5
                    rama_d.insert(0, (h + t, k + yv))
                    rama_d.append((h + t, k - yv))
                    rama_i.insert(0, (h - t, k + yv))
                    rama_i.append((h - t, k - yv))
                t += 0.1
            self._linea(rama_d, color)
            self._linea(rama_i, color)
            self._punto(h, k, "Centro")

        elif tipo == "Parábola":
            p = params.get("p", 0)
            pts = []
            if params.get("orientacion") == "horizontal":
                t = -25
                while t <= 25:
                    pts.append((h + (t ** 2) / (4 * p) if p else 0, k + t))
                    t += 0.2
            else:
                t = -25
                while t <= 25:
                    pts.append((h + t, k + (t ** 2) / (4 * p) if p else 0))
                    t += 0.2
            self._linea(pts, color)
            self._punto(h, k, "Vértice")

    # --- Funciones por tramos ---

    def _dibujar_funcion(self):
        """Dibuja la función con cortes en discontinuidades."""
        f = self.data["limites"]["f_eval"]
        punto = self.data["funcion"]["puntoAnalisis"]
        tipo_disc = self.data["funcion"]["tipo"]

        cx = self._cx()
        w = self.canvas.winfo_width()
        x = int((0 - cx) / self.scale) - 5
        x_fin = int((w - cx) / self.scale) + 5

        tramo = []
        while x <= x_fin:
            y = f(x)
            if y == "Indefinido" or y is None or abs(y) > 100:
                if len(tramo) > 1:
                    self._linea(tramo, "#dc3545")
                tramo = []
            else:
                tramo.append((x, y))
            x += 0.05

        if len(tramo) > 1:
            self._linea(tramo, "#dc3545")

        # Asíntota vertical
        if tipo_disc == "infinita":
            px = self._px(punto)
            h = self.canvas.winfo_height()
            self.canvas.create_line(px, 0, px, h, fill="#adb5bd", dash=(6, 4))
            self.canvas.create_text(px + 8, 16, text=f"x = {punto}",
                                    fill="#adb5bd", anchor=tk.W, font=("Arial", 9, "italic"))

    # --- Utilidades ---

    def _linea(self, puntos, color):
        """Dibuja una línea continua desde una lista de (x, y) matemáticos."""
        coords = []
        for x, y in puntos:
            coords.extend([self._px(x), self._py(y)])
        if len(coords) >= 4:
            self.canvas.create_line(coords, fill=color, width=2)

    def _punto(self, x, y, etiqueta):
        """Dibuja un punto destacado con etiqueta."""
        px, py = self._px(x), self._py(y)
        self.canvas.create_oval(px - 4, py - 4, px + 4, py + 4, fill="#212529")
        self.canvas.create_text(px + 10, py - 12,
                                text=f"{etiqueta} ({round(x, 1)}, {round(y, 1)})",
                                fill="#212529", anchor=tk.W, font=("Arial", 9, "bold"))