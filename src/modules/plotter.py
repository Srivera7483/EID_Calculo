# plotter.py - Motor de renderizado visual de matemáticas
# ============================================================================
# Este módulo se encarga de transformar cálculos matemáticos en gráficas visuales
# utilizando exclusivamente las herramientas nativas de Tkinter (Canvas),
# respetando la restricción de no usar librerías como Matplotlib o NumPy.

import tkinter as tk

class Plotter:
    """
    Motor de graficación interactivo. Soporta desplazamiento (Pan) y Zoom.
    Mantiene un estado interno de la data para poder redibujarse dinámicamente.
    """
    def __init__(self, canvas, width=800, height=600):
        self.canvas = canvas
        self.width = width
        self.height = height

        # Escala matemática inicial (píxeles por unidad)
        self.scale = 40

        # Centro del plano en píxeles (origen 0,0)
        self.center_x = width // 2
        self.center_y = height // 2
        
        # Datos a graficar (se llenan después)
        self.tipo_grafico = None
        self.data = None
        
        # Variables de estado para el arrastre
        self.drag_data = {"x": 0, "y": 0}
        
        # Vincular eventos del ratón para interactividad
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        
        # Eventos de Zoom (Rueda del ratón: Windows/Mac y Linux)
        self.canvas.bind("<MouseWheel>", self.on_zoom)
        self.canvas.bind("<Button-4>", self.on_zoom_in)   # Linux scroll up
        self.canvas.bind("<Button-5>", self.on_zoom_out)  # Linux scroll down

    # =========================================
    # EVENTOS DE INTERACTIVIDAD (PAN & ZOOM)
    # =========================================
    def on_press(self, event):
        """Inicia el movimiento de arrastre."""
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_drag(self, event):
        """Desplaza el plano y redibuja para mantener la cuadrícula infinita."""
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        
        self.center_x += dx
        self.center_y += dy
        
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.renderizar_todo()

    def on_zoom(self, event):
        """Maneja el zoom para Windows/Mac."""
        if event.delta > 0:
            self.scale = min(self.scale + 5, 200) # Límite máx
        elif event.delta < 0:
            self.scale = max(self.scale - 5, 10)  # Límite mín
        self.renderizar_todo()

    def on_zoom_in(self, event):
        """Zoom in para Linux."""
        self.scale = min(self.scale + 5, 200)
        self.renderizar_todo()

    def on_zoom_out(self, event):
        """Zoom out para Linux."""
        self.scale = max(self.scale - 5, 10)
        self.renderizar_todo()

    # =========================================
    # CONVERSIÓN DE COORDENADAS
    # =========================================
    def convertir_x(self, x):
        """Convierte X matemático a X en píxeles."""
        return self.center_x + (x * self.scale)

    def convertir_y(self, y):
        """Convierte Y matemático a Y en píxeles (Y invertido en pantallas)."""
        return self.center_y - (y * self.scale)

    # =========================================
    # RENDERIZADO PRINCIPAL
    # =========================================
    def set_data(self, tipo_grafico, data):
        """Guarda la información matemática y dispara el dibujo inicial."""
        self.tipo_grafico = tipo_grafico
        self.data = data
        self.renderizar_todo()

    def renderizar_todo(self):
        """Limpia el canvas y redibuja el fondo, los ejes y la matemática actual."""
        self.canvas.delete("all")
        
        # Fondo moderno gris muy claro
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#f8f9fa", outline="")
        
        self.dibujar_cuadricula()
        self.dibujar_ejes()
        
        # Enrutar el dibujo matemático
        if self.tipo_grafico == "conica" and self.data:
            self.renderizar_conica()
        elif self.tipo_grafico == "funcion" and self.data:
            self.renderizar_funcion()
            
        self.canvas.update_idletasks()

    # =========================================
    # DISEÑO DE FONDO (CUADRÍCULA Y EJES)
    # =========================================
    def dibujar_cuadricula(self):
        """Dibuja una cuadrícula infinita basada en la escala y centro actuales."""
        # Encontrar el inicio matemático de la pantalla
        min_x_math = int((0 - self.center_x) / self.scale) - 1
        max_x_math = int((self.width - self.center_x) / self.scale) + 1
        
        min_y_math = int((self.center_y - self.height) / self.scale) - 1
        max_y_math = int((self.center_y - 0) / self.scale) + 1

        # Líneas verticales
        for x in range(min_x_math, max_x_math):
            px = self.convertir_x(x)
            self.canvas.create_line(px, 0, px, self.height, fill="#e9ecef", dash=(2, 4))
            
        # Líneas horizontales
        for y in range(min_y_math, max_y_math):
            py = self.convertir_y(y)
            self.canvas.create_line(0, py, self.width, py, fill="#e9ecef", dash=(2, 4))

    def dibujar_ejes(self):
        """Dibuja los ejes X e Y engrosados con numeración."""
        # Eje X
        self.canvas.create_line(0, self.center_y, self.width, self.center_y, fill="#495057", width=2)
        # Eje Y
        self.canvas.create_line(self.center_x, 0, self.center_x, self.height, fill="#495057", width=2)

        # Rango visible
        min_x = int((0 - self.center_x) / self.scale)
        max_x = int((self.width - self.center_x) / self.scale)
        min_y = int((self.center_y - self.height) / self.scale)
        max_y = int((self.center_y - 0) / self.scale)

        # Etiquetas X
        for x in range(min_x, max_x + 1):
            if x != 0:
                px = self.convertir_x(x)
                self.canvas.create_line(px, self.center_y - 4, px, self.center_y + 4, fill="#495057")
                self.canvas.create_text(px, self.center_y + 15, text=str(x), fill="#6c757d", font=("Segoe UI", 8))

        # Etiquetas Y
        for y in range(min_y, max_y + 1):
            if y != 0:
                py = self.convertir_y(y)
                self.canvas.create_line(self.center_x - 4, py, self.center_x + 4, py, fill="#495057")
                self.canvas.create_text(self.center_x - 15, py, text=str(y), fill="#6c757d", font=("Segoe UI", 8))

    # =========================================
    # RENDERIZADO DE CÓNICAS (SIMPLIFICADO)
    # =========================================
    def renderizar_conica(self):
        """Dibuja la cónica actual usando primitivas matemáticas eficientes de Tkinter."""
        tipo = self.data.get('tipo', '')
        centro = self.data.get('centro')
        params = self.data.get('parametros', {})
        
        if not centro: return
        h, k = centro
        
        # Color primario
        color = "#007bff" # Azul bonito
        
        if tipo == 'Circunferencia':
            r = params.get('r', 0)
            # Dibujo perfecto usando la caja delimitadora (Bounding Box)
            x1, y1 = self.convertir_x(h - r), self.convertir_y(k + r)
            x2, y2 = self.convertir_x(h + r), self.convertir_y(k - r)
            self.canvas.create_oval(x1, y1, x2, y2, outline=color, width=2)
            self.marcar_punto(h, k, "Centro")

        elif tipo == 'Elipse':
            a = params.get('a2', 0)**0.5
            b = params.get('b2', 0)**0.5
            x1, y1 = self.convertir_x(h - a), self.convertir_y(k + b)
            x2, y2 = self.convertir_x(h + a), self.convertir_y(k - b)
            self.canvas.create_oval(x1, y1, x2, y2, outline=color, width=2)
            self.marcar_punto(h, k, "Centro")

        elif tipo == 'Hipérbola':
            a = params.get('a2', 0)**0.5
            b = params.get('b2', 0)**0.5
            # Puntos sueltos pero unidos con línea para formar ramas suaves
            puntos_der, puntos_izq = [], []
            x_math = a
            while x_math <= 20: # Límite matemático arbitrario
                valor = ((x_math**2) / (a**2)) - 1
                if valor >= 0:
                    y_math = (valor * (b**2))**0.5
                    puntos_der.insert(0, (h + x_math, k + y_math)) # Rama derecha arriba
                    puntos_der.append((h + x_math, k - y_math))    # Rama derecha abajo
                    puntos_izq.insert(0, (h - x_math, k + y_math)) # Rama izquierda arriba
                    puntos_izq.append((h - x_math, k - y_math))    # Rama izquierda abajo
                x_math += 0.1
            
            # Dibujar líneas continuas
            self.dibujar_linea_continua(puntos_der, color)
            self.dibujar_linea_continua(puntos_izq, color)
            self.marcar_punto(h, k, "Centro")

        elif tipo == 'Parábola':
            p = params.get('p', 0)
            orientacion = params.get('orientacion')
            puntos = []
            
            if orientacion == 'horizontal':
                y_math = -20
                while y_math <= 20:
                    x_math = (y_math**2) / (4*p) if p != 0 else 0
                    puntos.append((h + x_math, k + y_math))
                    y_math += 0.2
            else: # vertical
                x_math = -20
                while x_math <= 20:
                    y_math = (x_math**2) / (4*p) if p != 0 else 0
                    puntos.append((h + x_math, k + y_math))
                    x_math += 0.2
                    
            self.dibujar_linea_continua(puntos, color)
            self.marcar_punto(h, k, "Vértice")

    # =========================================
    # RENDERIZADO DE FUNCIONES
    # =========================================
    def renderizar_funcion(self):
        """Renderiza una función matemática continua o con cortes."""
        f_eval = self.data['limites']['f_eval']
        punto_critico = self.data['funcion']['puntoAnalisis']
        tipo_disc = self.data['funcion']['tipo']
        
        # Color rojo para la función
        color = "#dc3545" 
        
        x_math = int((0 - self.center_x) / self.scale) - 5 # Rango dinámico
        x_max = int((self.width - self.center_x) / self.scale) + 5
        
        tramo_actual = []
        step = 0.05
        
        while x_math <= x_max:
            y_math = f_eval(x_math)
            
            # Cortar la línea si hay error, discontinuidad o crecimiento excesivo
            if y_math == "Indefinido" or abs(y_math) > 100:
                if len(tramo_actual) > 1:
                    self.dibujar_linea_continua(tramo_actual, color)
                tramo_actual = []
            else:
                tramo_actual.append((x_math, y_math))
                
            x_math += step
            
        # Dibujar último tramo
        if len(tramo_actual) > 1:
            self.dibujar_linea_continua(tramo_actual, color)
            
        # Dibujar asíntota si existe
        if tipo_disc == 'infinita':
            px = self.convertir_x(punto_critico)
            self.canvas.create_line(px, 0, px, self.height, fill="#adb5bd", dash=(5, 5), width=2)
            self.canvas.create_text(px + 10, 20, text="Asíntota", fill="#adb5bd", anchor=tk.W)

    # =========================================
    # HELPERS
    # =========================================
    def dibujar_linea_continua(self, puntos_math, color):
        """Dibuja una línea continua a partir de una lista de coordenadas (x, y)."""
        coords_pixels = []
        for x, y in puntos_math:
            coords_pixels.extend([self.convertir_x(x), self.convertir_y(y)])
        if len(coords_pixels) >= 4:
            self.canvas.create_line(coords_pixels, fill=color, width=2, smooth=False)

    def marcar_punto(self, x, y, etiqueta):
        """Dibuja un punto destacado y su etiqueta en el plano."""
        px = self.convertir_x(x)
        py = self.convertir_y(y)
        self.canvas.create_oval(px - 4, py - 4, px + 4, py + 4, fill="#212529")
        self.canvas.create_text(px + 10, py - 10, text=f"{etiqueta}\n({round(x,1)}, {round(y,1)})", 
                                font=("Segoe UI", 9, "bold"), fill="#212529", anchor=tk.W)