# plotter.py - Motor de graficación interactivo
# ============================================================================
# Renderiza cónicas y funciones por tramos en un Canvas de Tkinter.
# Soporta desplazamiento (pan) con clic izquierdo y zoom con la rueda.
# No usa librerías externas (numpy, matplotlib, etc.) según las restricciones.
# ============================================================================

import tkinter as tk


class Plotter:
    """
    Graficador interactivo sobre un Canvas de Tkinter.
    
    Funcionalidades:
        - Dibuja ejes cartesianos con numeración dinámica
        - Cuadrícula tipo papel milimetrado
        - Pan (arrastre con clic izquierdo)
        - Zoom (rueda del ratón)
        - Renderiza cónicas: circunferencia, elipse, hipérbola, parábola
        - Renderiza funciones por tramos con detección de discontinuidades
    """

    # ── Colores del tema ────────────────────────────────────────────────
    COLOR_FONDO      = "#f8f9fa"   # Gris muy claro
    COLOR_CUADRICULA = "#e0e0e0"   # Gris suave para la cuadrícula
    COLOR_EJE        = "#495057"   # Gris oscuro para los ejes
    COLOR_NUMERO     = "#6c757d"   # Gris medio para las etiquetas
    COLOR_CONICA     = "#007bff"   # Azul para cónicas
    COLOR_FUNCION    = "#dc3545"   # Rojo para funciones
    COLOR_ASINTOTA   = "#adb5bd"   # Gris claro para asíntotas
    COLOR_PUNTO      = "#212529"   # Negro para puntos destacados

    def __init__(self, canvas):
        self.canvas = canvas

        # Escala: cuántos píxeles representa una unidad matemática
        self.scale = 40

        # Desplazamiento del origen (0,0) respecto a la esquina superior-izquierda
        # Se calcula dinámicamente al renderizar
        self.offset_x = 0
        self.offset_y = 0

        # Datos matemáticos a graficar
        self.tipo_grafico = None
        self.data = None

        # Estado del arrastre
        self._drag_x = 0
        self._drag_y = 0

        # ── Vincular eventos ────────────────────────────────────────────
        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        # Zoom: Linux usa Button-4/5, Windows/Mac usa MouseWheel
        self.canvas.bind("<Button-4>", lambda e: self._zoom(5))
        self.canvas.bind("<Button-5>", lambda e: self._zoom(-5))
        self.canvas.bind("<MouseWheel>", lambda e: self._zoom(5 if e.delta > 0 else -5))

    # ════════════════════════════════════════════════════════════════════
    # EVENTOS DE INTERACTIVIDAD
    # ════════════════════════════════════════════════════════════════════

    def _on_resize(self, event):
        """Redibuja al cambiar el tamaño de la ventana."""
        self._renderizar()

    def _on_press(self, event):
        """Guarda posición inicial del arrastre."""
        self._drag_x = event.x
        self._drag_y = event.y

    def _on_drag(self, event):
        """Desplaza el plano según el movimiento del ratón."""
        self.offset_x += event.x - self._drag_x
        self.offset_y += event.y - self._drag_y
        self._drag_x = event.x
        self._drag_y = event.y
        self._renderizar()

    def _zoom(self, delta):
        """Cambia la escala (zoom in/out) con límites."""
        self.scale = max(10, min(200, self.scale + delta))
        self._renderizar()

    # ════════════════════════════════════════════════════════════════════
    # CONVERSIÓN DE COORDENADAS
    # ════════════════════════════════════════════════════════════════════

    def _cx(self):
        """Centro X actual del canvas (origen matemático en píxeles)."""
        return self.canvas.winfo_width() // 2 + self.offset_x

    def _cy(self):
        """Centro Y actual del canvas (origen matemático en píxeles)."""
        return self.canvas.winfo_height() // 2 + self.offset_y

    def _to_px(self, x):
        """Convierte coordenada X matemática a píxeles."""
        return self._cx() + x * self.scale

    def _to_py(self, y):
        """Convierte coordenada Y matemática a píxeles (eje Y invertido)."""
        return self._cy() - y * self.scale

    # ════════════════════════════════════════════════════════════════════
    # PUNTO DE ENTRADA
    # ════════════════════════════════════════════════════════════════════

    def set_data(self, tipo_grafico, data):
        """Guarda los datos y lanza el primer renderizado."""
        self.tipo_grafico = tipo_grafico
        self.data = data
        self._renderizar()

    # ════════════════════════════════════════════════════════════════════
    # RENDERIZADO PRINCIPAL
    # ════════════════════════════════════════════════════════════════════

    def _renderizar(self):
        """Limpia y redibuja todo el canvas."""
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        # Fondo completo (elimina cualquier borde blanco residual)
        self.canvas.create_rectangle(-2, -2, w + 4, h + 4,
                                     fill=self.COLOR_FONDO, outline="")

        self._dibujar_cuadricula(w, h)
        self._dibujar_ejes(w, h)

        # Dibujar los datos matemáticos
        if self.tipo_grafico == "conica" and self.data:
            self._renderizar_conica()
        elif self.tipo_grafico == "funcion" and self.data:
            self._renderizar_funcion(w)

    # ════════════════════════════════════════════════════════════════════
    # CUADRÍCULA Y EJES
    # ════════════════════════════════════════════════════════════════════

    def _dibujar_cuadricula(self, w, h):
        """Dibuja líneas punteadas de fondo (papel milimetrado)."""
        cx, cy = self._cx(), self._cy()

        # Rango visible en unidades matemáticas
        x_min = int((0 - cx) / self.scale) - 1
        x_max = int((w - cx) / self.scale) + 1
        y_min = int((cy - h) / self.scale) - 1
        y_max = int((cy - 0) / self.scale) + 1

        for x in range(x_min, x_max + 1):
            px = self._to_px(x)
            self.canvas.create_line(px, 0, px, h,
                                    fill=self.COLOR_CUADRICULA, dash=(2, 4))

        for y in range(y_min, y_max + 1):
            py = self._to_py(y)
            self.canvas.create_line(0, py, w, py,
                                    fill=self.COLOR_CUADRICULA, dash=(2, 4))

    def _dibujar_ejes(self, w, h):
        """Dibuja ejes X e Y con marcas numéricas."""
        cx, cy = self._cx(), self._cy()

        # Ejes principales
        self.canvas.create_line(0, cy, w, cy, fill=self.COLOR_EJE, width=2)
        self.canvas.create_line(cx, 0, cx, h, fill=self.COLOR_EJE, width=2)

        # Marcas y números
        x_min = int((0 - cx) / self.scale)
        x_max = int((w - cx) / self.scale)
        y_min = int((cy - h) / self.scale)
        y_max = int((cy - 0) / self.scale)

        for x in range(x_min, x_max + 1):
            if x == 0:
                continue
            px = self._to_px(x)
            self.canvas.create_line(px, cy - 4, px, cy + 4,
                                    fill=self.COLOR_EJE)
            self.canvas.create_text(px, cy + 14, text=str(x),
                                    fill=self.COLOR_NUMERO, font=("Arial", 8))

        for y in range(y_min, y_max + 1):
            if y == 0:
                continue
            py = self._to_py(y)
            self.canvas.create_line(cx - 4, py, cx + 4, py,
                                    fill=self.COLOR_EJE)
            self.canvas.create_text(cx - 14, py, text=str(y),
                                    fill=self.COLOR_NUMERO, font=("Arial", 8))

    # ════════════════════════════════════════════════════════════════════
    # RENDERIZADO DE CÓNICAS
    # ════════════════════════════════════════════════════════════════════

    def _renderizar_conica(self):
        """Dibuja la cónica según su tipo, usando las primitivas de Tkinter."""
        tipo = self.data.get("tipo", "")
        centro = self.data.get("centro")
        params = self.data.get("parametros", {})

        if not centro:
            return
        h, k = centro

        if tipo == "Circunferencia":
            r = params.get("r", 0)
            # create_oval recibe la caja delimitadora (bounding box)
            self.canvas.create_oval(
                self._to_px(h - r), self._to_py(k + r),
                self._to_px(h + r), self._to_py(k - r),
                outline=self.COLOR_CONICA, width=2)
            self._marcar_punto(h, k, "Centro")

        elif tipo == "Elipse":
            a = params.get("a2", 0) ** 0.5
            b = params.get("b2", 0) ** 0.5
            self.canvas.create_oval(
                self._to_px(h - a), self._to_py(k + b),
                self._to_px(h + a), self._to_py(k - b),
                outline=self.COLOR_CONICA, width=2)
            self._marcar_punto(h, k, "Centro")

        elif tipo == "Hipérbola":
            a = params.get("a2", 0) ** 0.5
            b = params.get("b2", 0) ** 0.5
            rama_der = []
            rama_izq = []
            t = a
            while t <= 25:
                val = ((t ** 2) / (a ** 2)) - 1
                if val >= 0:
                    y_val = (val * (b ** 2)) ** 0.5
                    # Cada rama se construye como arco continuo (arriba → abajo)
                    rama_der.insert(0, (h + t, k + y_val))
                    rama_der.append((h + t, k - y_val))
                    rama_izq.insert(0, (h - t, k + y_val))
                    rama_izq.append((h - t, k - y_val))
                t += 0.1
            self._trazar_linea(rama_der, self.COLOR_CONICA)
            self._trazar_linea(rama_izq, self.COLOR_CONICA)
            self._marcar_punto(h, k, "Centro")

        elif tipo == "Parábola":
            p = params.get("p", 0)
            orientacion = params.get("orientacion", "vertical")
            puntos = []

            if orientacion == "horizontal":
                t = -25
                while t <= 25:
                    x_val = (t ** 2) / (4 * p) if p != 0 else 0
                    puntos.append((h + x_val, k + t))
                    t += 0.2
            else:
                t = -25
                while t <= 25:
                    y_val = (t ** 2) / (4 * p) if p != 0 else 0
                    puntos.append((h + t, k + y_val))
                    t += 0.2

            self._trazar_linea(puntos, self.COLOR_CONICA)
            self._marcar_punto(h, k, "Vértice")

    # ════════════════════════════════════════════════════════════════════
    # RENDERIZADO DE FUNCIONES POR TRAMOS
    # ════════════════════════════════════════════════════════════════════

    def _renderizar_funcion(self, ancho_canvas):
        """Dibuja la función evaluando punto a punto con cortes en discontinuidades."""
        f_eval = self.data["limites"]["f_eval"]
        punto = self.data["funcion"]["puntoAnalisis"]
        tipo_disc = self.data["funcion"]["tipo"]

        # Rango visible dinámico
        cx = self._cx()
        x_ini = int((0 - cx) / self.scale) - 5
        x_fin = int((ancho_canvas - cx) / self.scale) + 5

        tramo = []
        x = x_ini
        paso = 0.05
        while x <= x_fin:
            y = f_eval(x)

            # Si la función es indefinida o explota, cortamos el trazo
            if y == "Indefinido" or y is None or abs(y) > 100:
                if len(tramo) > 1:
                    self._trazar_linea(tramo, self.COLOR_FUNCION)
                tramo = []
            else:
                tramo.append((x, y))

            x += paso

        # Dibujar el último tramo pendiente
        if len(tramo) > 1:
            self._trazar_linea(tramo, self.COLOR_FUNCION)

        # Asíntota vertical (solo para discontinuidad infinita)
        if tipo_disc == "infinita":
            px = self._to_px(punto)
            h = self.canvas.winfo_height()
            self.canvas.create_line(px, 0, px, h,
                                    fill=self.COLOR_ASINTOTA, dash=(6, 4), width=1)
            self.canvas.create_text(px + 8, 16, text=f"x = {punto}",
                                    fill=self.COLOR_ASINTOTA, anchor=tk.W,
                                    font=("Arial", 9, "italic"))

    # ════════════════════════════════════════════════════════════════════
    # UTILIDADES DE DIBUJO
    # ════════════════════════════════════════════════════════════════════

    def _trazar_linea(self, puntos, color):
        """Convierte una lista de (x, y) matemáticos a píxeles y traza una línea."""
        coords = []
        for x, y in puntos:
            coords.append(self._to_px(x))
            coords.append(self._to_py(y))
        if len(coords) >= 4:
            self.canvas.create_line(coords, fill=color, width=2)

    def _marcar_punto(self, x, y, etiqueta):
        """Dibuja un punto negro con etiqueta de texto."""
        px, py = self._to_px(x), self._to_py(y)
        r = 4
        self.canvas.create_oval(px - r, py - r, px + r, py + r,
                                fill=self.COLOR_PUNTO)
        self.canvas.create_text(px + 10, py - 12,
                                text=f"{etiqueta} ({round(x, 1)}, {round(y, 1)})",
                                fill=self.COLOR_PUNTO, anchor=tk.W,
                                font=("Arial", 9, "bold"))