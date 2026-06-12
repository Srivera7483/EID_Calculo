# plotter.py - Graficador interactivo con Tkinter
# Permite graficar cónicas y funciones por tramos en un plano cartesiano
# Soporta: arrastre con clic izquierdo y zoom con la rueda del ratón

import tkinter as tk


class Graficador:
    """Dibuja cónicas y funciones en un plano cartesiano interactivo."""

    def __init__(self, lienzo):
        self.lienzo = lienzo
        self.escala = 40              # Pixeles por unidad matemática
        self.desplazamientoX = 0      # Desplazamiento horizontal del origen
        self.desplazamientoY = 0      # Desplazamiento vertical del origen
        self.tipoGrafico = None       # "conica" o "funcion"
        self.datos = None             # Datos matemáticos a graficar
        self.arrastre_x = 0
        self.arrastre_y = 0

        # Vincular eventos del ratón
        lienzo.bind("<Configure>", self.dibujarTodo)
        lienzo.bind("<ButtonPress-1>", self.inicioArrastre)
        lienzo.bind("<B1-Motion>", self.moverPlano)
        lienzo.bind("<Button-4>", lambda e: self.hacerZoom(5))       # Linux rueda arriba
        lienzo.bind("<Button-5>", lambda e: self.hacerZoom(-5))      # Linux rueda abajo
        lienzo.bind("<MouseWheel>", lambda e: self.hacerZoom(5 if e.delta > 0 else -5))

    # ==========================================
    # INTERACCIÓN DEL USUARIO
    # ==========================================

    def inicioArrastre(self, evento):
        """Guarda la posición inicial del clic."""
        self.arrastre_x = evento.x
        self.arrastre_y = evento.y

    def moverPlano(self, evento):
        """Mueve el plano según el arrastre del ratón."""
        self.desplazamientoX += evento.x - self.arrastre_x
        self.desplazamientoY += evento.y - self.arrastre_y
        self.arrastre_x = evento.x
        self.arrastre_y = evento.y
        self.dibujarTodo()

    def hacerZoom(self, delta):
        """Acerca o aleja el plano con la rueda del ratón."""
        self.escala = max(10, min(200, self.escala + delta))
        self.dibujarTodo()

    # ==========================================
    # CONVERSIÓN DE COORDENADAS
    # ==========================================

    def centroX(self):
        """Retorna la posición X del origen (0,0) en pixeles."""
        return self.lienzo.winfo_width() // 2 + self.desplazamientoX

    def centroY(self):
        """Retorna la posición Y del origen (0,0) en pixeles."""
        return self.lienzo.winfo_height() // 2 + self.desplazamientoY

    def aPixelX(self, xMatematico):
        """Convierte coordenada X matemática a pixeles."""
        return self.centroX() + xMatematico * self.escala

    def aPixelY(self, yMatematico):
        """Convierte coordenada Y matemática a pixeles (eje Y invertido en pantalla)."""
        return self.centroY() - yMatematico * self.escala

    # ==========================================
    # PUNTO DE ENTRADA
    # ==========================================

    def cargarDatos(self, tipoGrafico, datos):
        """Guarda los datos matemáticos y dibuja la gráfica."""
        self.tipoGrafico = tipoGrafico
        self.datos = datos
        self.lienzo.update_idletasks()
        self.dibujarTodo()

    # ==========================================
    # DIBUJO PRINCIPAL
    # ==========================================

    def dibujarTodo(self, evento=None):
        """Limpia el lienzo y redibuja todo: fondo, cuadrícula, ejes y gráfica."""
        self.lienzo.delete("all")
        
        # Si venimos de un evento Configure, usamos sus medidas que son las más recientes
        if evento and hasattr(evento, 'width') and evento.width > 10:
            ancho = evento.width
            alto = evento.height
        else:
            self.lienzo.update_idletasks()
            ancho = self.lienzo.winfo_width()
            alto = self.lienzo.winfo_height()
            
        # Si el lienzo aún no se inicializa, le damos un tamaño por defecto
        if ancho < 10: ancho = 800
        if alto < 10: alto = 600

        # Fondo gris claro (sin bordes blancos)
        self.lienzo.create_rectangle(-2, -2, ancho + 4, alto + 4, fill="#f8f9fa", outline="")

        self.dibujarCuadricula(ancho, alto)
        self.dibujarEjes(ancho, alto)

        # Dibujar la gráfica matemática
        if self.tipoGrafico == "conica" and self.datos:
            self.dibujarConica()
        elif self.tipoGrafico == "funcion" and self.datos:
            self.dibujarFuncion()

    def dibujarCuadricula(self, ancho, alto):
        """Dibuja líneas de fondo tipo papel milimetrado."""
        cx = self.centroX()
        cy = self.centroY()

        xInicio = int((0 - cx) / self.escala) - 1
        xFin = int((ancho - cx) / self.escala) + 2
        yInicio = int((cy - alto) / self.escala) - 1
        yFin = int(cy / self.escala) + 2

        for x in range(xInicio, xFin):
            pixelX = self.aPixelX(x)
            self.lienzo.create_line(pixelX, 0, pixelX, alto, fill="#e0e0e0", dash=(2, 4))

        for y in range(yInicio, yFin):
            pixelY = self.aPixelY(y)
            self.lienzo.create_line(0, pixelY, ancho, pixelY, fill="#e0e0e0", dash=(2, 4))

    def dibujarEjes(self, ancho, alto):
        """Dibuja los ejes X e Y con sus números."""
        cx = self.centroX()
        cy = self.centroY()

        # Ejes principales
        self.lienzo.create_line(0, cy, ancho, cy, fill="#495057", width=2)
        self.lienzo.create_line(cx, 0, cx, alto, fill="#495057", width=2)

        # Números en el eje X
        xInicio = int((0 - cx) / self.escala)
        xFin = int((ancho - cx) / self.escala) + 1
        for x in range(xInicio, xFin):
            if x != 0:
                pixelX = self.aPixelX(x)
                self.lienzo.create_line(pixelX, cy - 4, pixelX, cy + 4, fill="#495057")
                self.lienzo.create_text(pixelX, cy + 14, text=str(x), fill="#6c757d", font=("Arial", 8))

        # Números en el eje Y
        yInicio = int((cy - alto) / self.escala)
        yFin = int(cy / self.escala) + 1
        for y in range(yInicio, yFin):
            if y != 0:
                pixelY = self.aPixelY(y)
                self.lienzo.create_line(cx - 4, pixelY, cx + 4, pixelY, fill="#495057")
                self.lienzo.create_text(cx - 14, pixelY, text=str(y), fill="#6c757d", font=("Arial", 8))

    # ==========================================
    # DIBUJO DE CÓNICAS
    # ==========================================

    def dibujarConica(self):
        """Dibuja la cónica según su tipo: circunferencia, elipse, hipérbola o parábola."""
        tipoConica = self.datos.get("tipo", "")
        centro = self.datos.get("centro")
        parametros = self.datos.get("parametros", {})
        if not centro:
            return

        h, k = centro
        colorConica = "#007bff"

        if tipoConica == "Circunferencia":
            radio = parametros.get("r", 0)
            self.lienzo.create_oval(
                self.aPixelX(h - radio), self.aPixelY(k + radio),
                self.aPixelX(h + radio), self.aPixelY(k - radio),
                outline=colorConica, width=2)
            self.marcarPunto(h, k, "Centro")

        elif tipoConica == "Elipse":
            semiEjeA = parametros.get("a2", 0) ** 0.5
            semiEjeB = parametros.get("b2", 0) ** 0.5
            self.lienzo.create_oval(
                self.aPixelX(h - semiEjeA), self.aPixelY(k + semiEjeB),
                self.aPixelX(h + semiEjeA), self.aPixelY(k - semiEjeB),
                outline=colorConica, width=2)
            self.marcarPunto(h, k, "Centro")

        elif tipoConica == "Hipérbola":
            semiEjeA = parametros.get("a2", 0) ** 0.5
            semiEjeB = parametros.get("b2", 0) ** 0.5
            ramaDerecha = []
            ramaIzquierda = []
            t = semiEjeA
            while t <= 25:
                valor = ((t ** 2) / (semiEjeA ** 2)) - 1
                if valor >= 0:
                    yValor = (valor * semiEjeB ** 2) ** 0.5
                    ramaDerecha.insert(0, (h + t, k + yValor))
                    ramaDerecha.append((h + t, k - yValor))
                    ramaIzquierda.insert(0, (h - t, k + yValor))
                    ramaIzquierda.append((h - t, k - yValor))
                t += 0.1
            self.trazarLinea(ramaDerecha, colorConica)
            self.trazarLinea(ramaIzquierda, colorConica)
            self.marcarPunto(h, k, "Centro")

        elif tipoConica == "Parábola":
            parametroP = parametros.get("p", 0)
            orientacion = parametros.get("orientacion", "vertical")
            puntos = []

            if orientacion == "horizontal":
                t = -25
                while t <= 25:
                    xValor = (t ** 2) / (4 * parametroP) if parametroP != 0 else 0
                    puntos.append((h + xValor, k + t))
                    t += 0.2
            else:
                t = -25
                while t <= 25:
                    yValor = (t ** 2) / (4 * parametroP) if parametroP != 0 else 0
                    puntos.append((h + t, k + yValor))
                    t += 0.2

            self.trazarLinea(puntos, colorConica)
            self.marcarPunto(h, k, "Vértice")

    # ==========================================
    # DIBUJO DE FUNCIONES POR TRAMOS
    # ==========================================

    def dibujarFuncion(self):
        """Dibuja la función por tramos, cortando en las discontinuidades."""
        funcionEvaluar = self.datos["limites"]["f_eval"]
        puntoAnalisis = self.datos["funcion"]["puntoAnalisis"]
        tipoDiscontinuidad = self.datos["funcion"]["tipo"]

        anchoLienzo = self.lienzo.winfo_width()
        cx = self.centroX()
        xInicio = int((0 - cx) / self.escala) - 5
        xFin = int((anchoLienzo - cx) / self.escala) + 5

        colorFuncion = "#dc3545"
        tramoActual = []
        x = xInicio
        paso = 0.05

        while x <= xFin:
            valorY = funcionEvaluar(x)

            # Si el valor es indefinido o muy grande, cortamos el trazo
            if valorY == "Indefinido" or valorY is None or abs(valorY) > 100:
                if len(tramoActual) > 1:
                    self.trazarLinea(tramoActual, colorFuncion)
                tramoActual = []
            else:
                tramoActual.append((x, valorY))
            x += paso

        # Dibujar el último tramo pendiente
        if len(tramoActual) > 1:
            self.trazarLinea(tramoActual, colorFuncion)

        # Marcadores visuales según tipo de discontinuidad
        if tipoDiscontinuidad == "infinita":
            # Asíntota vertical (línea punteada)
            pixelAsintota = self.aPixelX(puntoAnalisis)
            altoLienzo = self.lienzo.winfo_height()
            self.lienzo.create_line(pixelAsintota, 0, pixelAsintota, altoLienzo,
                                    fill="#adb5bd", dash=(6, 4))
            self.lienzo.create_text(pixelAsintota + 8, 16, text=f"x = {puntoAnalisis}",
                                    fill="#adb5bd", anchor=tk.W, font=("Arial", 9, "italic"))

        elif tipoDiscontinuidad == "removible":
            # Círculo vacío: indica que el punto NO está definido
            valorLimite = puntoAnalisis + self.datos["funcion"]["digitos"][0]  # a + d1
            pxHueco = self.aPixelX(puntoAnalisis)
            pyHueco = self.aPixelY(valorLimite)
            radio = 5
            self.lienzo.create_oval(pxHueco - radio, pyHueco - radio,
                                    pxHueco + radio, pyHueco + radio,
                                    outline=colorFuncion, width=2, fill="#f8f9fa")

        elif tipoDiscontinuidad == "salto":
            # Puntos llenos en cada lado del salto
            d2 = self.datos["funcion"]["digitos"][1]
            d4 = self.datos["funcion"]["digitos"][3]
            valorIzq = puntoAnalisis + d2
            valorDer = puntoAnalisis + d4
            self.marcarPunto(puntoAnalisis, valorIzq, "lím izq")
            self.marcarPunto(puntoAnalisis, valorDer, "lím der")

    # ==========================================
    # UTILIDADES DE DIBUJO
    # ==========================================

    def trazarLinea(self, puntosMath, color):
        """Dibuja una línea continua desde una lista de coordenadas (x, y) matemáticas."""
        coordenadasPixel = []
        for xMath, yMath in puntosMath:
            coordenadasPixel.extend([self.aPixelX(xMath), self.aPixelY(yMath)])
        if len(coordenadasPixel) >= 4:
            self.lienzo.create_line(coordenadasPixel, fill=color, width=2)

    def marcarPunto(self, x, y, etiqueta):
        """Dibuja un punto negro con una etiqueta de texto."""
        pixelX = self.aPixelX(x)
        pixelY = self.aPixelY(y)
        self.lienzo.create_oval(pixelX - 4, pixelY - 4, pixelX + 4, pixelY + 4, fill="#212529")
        self.lienzo.create_text(pixelX + 10, pixelY - 12,
                                text=f"{etiqueta} ({round(x, 1)}, {round(y, 1)})",
                                fill="#212529", anchor=tk.W, font=("Arial", 9, "bold"))