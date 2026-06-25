# plotter.py - Graficador interactivo con Tkinter
# Dibuja cónicas y funciones por tramos en un plano cartesiano.
# Soporta: arrastre con clic izquierdo y zoom con la rueda del ratón.

import tkinter as tk


# Constantes de configuración del graficador
ESCALA_INICIAL = 40       # Pixeles por unidad matemática
ESCALA_MINIMA = 10        # Zoom mínimo permitido
ESCALA_MAXIMA = 200       # Zoom máximo permitido
DELTA_ZOOM     = 5         # Pixeles por paso de rueda
RANGO_GRAFICO  = 25       # Rango de graficación en unidades matemáticas
PASO_HIPERBOLA = 0.1      # Incremento para trazar hipérbola
PASO_PARABOLA  = 0.2      # Incremento para trazar parábola
PASO_FUNCION   = 0.05     # Incremento para trazar función por tramos
UMBRAL_DISCONTINUIDAD = 100 # Valores absolutos por arriba se consideran discontinuidad
TAMANO_MARCA = 4          # Radio en pixeles de puntos marcados
TAMANO_AGUJERO = 5        # Radio en pixeles de círculos de discontinuidad
FUENTE_EJES = ("Arial", 8)
FUENTE_ETIQUETA = ("Arial", 9, "bold")
FUENTE_ASINTOTA = ("Arial", 9, "italic")
COLOR_FONDO = "#f8f9fa"
COLOR_CUADRICULA = "#e0e0e0"
COLOR_EJES = "#495057"
COLOR_NUMEROS = "#6c757d"
COLOR_CURVA_CONICA = "#007bff"
COLOR_CURVA_FUNCION = "#dc3545"
COLOR_ASINTOTA = "#adb5bd"
COLOR_PUNTO = "#212529"


class Graficador:
    """Dibuja cónicas y funciones por tramos en un plano cartesiano interactivo."""

    def __init__(self, lienzo):
        self.lienzo          = lienzo
        self.escala          = ESCALA_INICIAL
        self.desplazamientoX = 0
        self.desplazamientoY = 0
        self.tipoGrafico     = None  # "conica" o "funcion"
        self.datos           = {}
        self.arrastreInicialX = 0
        self.arrastreInicialY = 0

        # Vincular eventos del ratón al lienzo
        lienzo.bind("<Configure>",     self.dibujarTodo)
        lienzo.bind("<ButtonPress-1>", self.inicioArrastre)
        lienzo.bind("<B1-Motion>",      self.moverPlano)
        lienzo.bind("<Button-4>",       lambda e: self.hacerZoom(DELTA_ZOOM))      # Linux rueda arriba
        lienzo.bind("<Button-5>",       lambda e: self.hacerZoom(-DELTA_ZOOM))     # Linux rueda abajo
        lienzo.bind("<MouseWheel>",     lambda e: self.hacerZoom(DELTA_ZOOM if e.delta > 0 else -DELTA_ZOOM))

    # ==========================================
    # INTERACCIÓN DEL USUARIO
    # ==========================================

    def inicioArrastre(self, evento):
        """Guarda la posición inicial del clic para calcular el desplazamiento."""
        self.arrastreInicialX = evento.x
        self.arrastreInicialY = evento.y

    def moverPlano(self, evento):
        """Desplaza el origen del plano según el movimiento del ratón."""
        self.desplazamientoX += evento.x - self.arrastreInicialX
        self.desplazamientoY += evento.y - self.arrastreInicialY
        self.arrastreInicialX = evento.x
        self.arrastreInicialY = evento.y
        self.dibujarTodo()

    def hacerZoom(self, cambioPorPaso):
        """Acerca o aleja el plano con la rueda del ratón."""
        self.escala = max(ESCALA_MINIMA, min(ESCALA_MAXIMA, self.escala + cambioPorPaso))
        self.dibujarTodo()

    # ==========================================
    # CONVERSIÓN DE COORDENADAS
    # ==========================================

    def centroX(self):
        """Posición X del origen matemático (0,0) en pixeles."""
        return self.lienzo.winfo_width() // 2 + self.desplazamientoX

    def centroY(self):
        """Posición Y del origen matemático (0,0) en pixeles."""
        return self.lienzo.winfo_height() // 2 + self.desplazamientoY

    def aPixelX(self, xMatematico):
        """Convierte una coordenada X matemática a pixeles."""
        return self.centroX() + xMatematico * self.escala

    def aPixelY(self, yMatematico):
        """Convierte una coordenada Y matemática a pixeles (eje Y invertido en pantalla)."""
        return self.centroY() - yMatematico * self.escala

    # ==========================================
    # PUNTO DE ENTRADA
    # ==========================================

    def cargarDatos(self, tipoGrafico, datos):
        """Recibe los datos matemáticos y lanza el dibujo inicial."""
        self.tipoGrafico = tipoGrafico
        self.datos = datos if datos is not None else {}
        self.lienzo.update_idletasks()
        self.dibujarTodo()

    # ==========================================
    # DIBUJO PRINCIPAL
    # ==========================================

    def dibujarTodo(self, evento=None):
        """Borra el lienzo y redibuja: fondo, cuadrícula, ejes y gráfica."""
        self.lienzo.delete("all")

        # Obtener dimensiones actuales del lienzo
        if evento and hasattr(evento, 'width') and evento.width > 10:
            ancho = evento.width
            alto  = evento.height
        else:
            self.lienzo.update_idletasks()
            ancho = self.lienzo.winfo_width()
            alto  = self.lienzo.winfo_height()

        # Valores por defecto si el lienzo aún no se ha inicializado
        if ancho < 10: ancho = 800
        if alto  < 10: alto  = 600

        # Fondo
        self.lienzo.create_rectangle(-2, -2, ancho + 4, alto + 4, fill=COLOR_FONDO, outline="")

        self.dibujarCuadricula(ancho, alto)
        self.dibujarEjes(ancho, alto)

        if self.tipoGrafico == "conica" and self.datos:
            self.dibujarConica()
        elif self.tipoGrafico == "funcion" and self.datos:
            self.dibujarFuncion()

    def dibujarCuadricula(self, ancho, alto):
        """Dibuja líneas de fondo estilo papel milimetrado."""
        cx = self.centroX()
        cy = self.centroY()

        xInicio = int((0 - cx) / self.escala) - 1
        xFin    = int((ancho - cx) / self.escala) + 2
        yInicio = int((cy - alto) / self.escala) - 1
        yFin    = int(cy / self.escala) + 2

        for xUnidad in range(xInicio, xFin):
            pixelX = self.aPixelX(xUnidad)
            self.lienzo.create_line(pixelX, 0, pixelX, alto, fill=COLOR_CUADRICULA, dash=(2, 4))

        for yUnidad in range(yInicio, yFin):
            pixelY = self.aPixelY(yUnidad)
            self.lienzo.create_line(0, pixelY, ancho, pixelY, fill=COLOR_CUADRICULA, dash=(2, 4))

    def dibujarEjes(self, ancho, alto):
        """Dibuja los ejes X e Y con marcas numéricas."""
        cx = self.centroX()
        cy = self.centroY()

        # Ejes principales
        self.lienzo.create_line(0, cy, ancho, cy, fill=COLOR_EJES, width=2)
        self.lienzo.create_line(cx, 0, cx, alto, fill=COLOR_EJES, width=2)

        # Números en el eje X
        xInicio = int((0 - cx) / self.escala)
        xFin    = int((ancho - cx) / self.escala) + 1
        for xUnidad in range(xInicio, xFin):
            if xUnidad != 0:
                pixelX = self.aPixelX(xUnidad)
                self.lienzo.create_line(pixelX, cy - 4, pixelX, cy + 4, fill=COLOR_EJES)
                self.lienzo.create_text(pixelX, cy + 14, text=str(xUnidad), fill=COLOR_NUMEROS, font=FUENTE_EJES)

        # Números en el eje Y
        yInicio = int((cy - alto) / self.escala)
        yFin    = int(cy / self.escala) + 1
        for yUnidad in range(yInicio, yFin):
            if yUnidad != 0:
                pixelY = self.aPixelY(yUnidad)
                self.lienzo.create_line(cx - 4, pixelY, cx + 4, pixelY, fill=COLOR_EJES)
                self.lienzo.create_text(cx - 14, pixelY, text=str(yUnidad), fill=COLOR_NUMEROS, font=FUENTE_EJES)

    # ==========================================
    # DIBUJO DE CÓNICAS
    # ==========================================

    def dibujarConica(self):
        """Dibuja la cónica según su tipo: circunferencia, elipse, hipérbola o parábola."""
        datos = self.datos or {}
        tipoConica = datos.get("tipo", "")
        centro = datos.get("centro")
        parametros = datos.get("parametros", {})

        if not centro:
            return

        h, k = centro
        colorCurva = COLOR_CURVA_CONICA

        if tipoConica == "Circunferencia":
            radio = parametros.get("r", 0)
            self._dibujarOvalo(self.aPixelX(h - radio), self.aPixelY(k + radio),
                               self.aPixelX(h + radio), self.aPixelY(k - radio),
                               colorCurva)
            self.marcarPunto(h, k, "Centro")

        elif tipoConica == "Elipse":
            semiEjeA = parametros.get("a2", 0) ** 0.5
            semiEjeB = parametros.get("b2", 0) ** 0.5
            self._dibujarOvalo(self.aPixelX(h - semiEjeA), self.aPixelY(k + semiEjeB),
                                self.aPixelX(h + semiEjeA), self.aPixelY(k - semiEjeB),
                                colorCurva)
            self.marcarPunto(h, k, "Centro")

        elif tipoConica == "Hipérbola":
            semiEjeA = parametros.get("a2", 0) ** 0.5
            semiEjeB = parametros.get("b2", 0) ** 0.5
            ramaDerecha   = []
            ramaIzquierda = []

            xActual = semiEjeA
            while xActual <= RANGO_GRAFICO:
                valorBajoRaiz = ((xActual ** 2) / (semiEjeA ** 2)) - 1
                if valorBajoRaiz >= 0:
                    yValor = (valorBajoRaiz * semiEjeB ** 2) ** 0.5
                    ramaDerecha.insert(0, (h + xActual, k + yValor))
                    ramaDerecha.append((h + xActual, k - yValor))
                    ramaIzquierda.insert(0, (h - xActual, k + yValor))
                    ramaIzquierda.append((h - xActual, k - yValor))
                xActual += PASO_HIPERBOLA

            self.trazarLinea(ramaDerecha,   colorCurva)
            self.trazarLinea(ramaIzquierda, colorCurva)
            self.marcarPunto(h, k, "Centro")

        elif tipoConica == "Parábola":
            parametroP  = parametros.get("p", 0)
            orientacion = parametros.get("orientacion", "vertical")
            puntos      = []

            tActual = -RANGO_GRAFICO
            while tActual <= RANGO_GRAFICO:
                if orientacion == "horizontal":
                    xValor = (tActual ** 2) / (4 * parametroP) if parametroP != 0 else 0
                    puntos.append((h + xValor, k + tActual))
                else:
                    yValor = (tActual ** 2) / (4 * parametroP) if parametroP != 0 else 0
                    puntos.append((h + tActual, k + yValor))
                tActual += PASO_PARABOLA

            self.trazarLinea(puntos, colorCurva)
            self.marcarPunto(h, k, "Vértice")

    # ==========================================
    # DIBUJO DE FUNCIONES POR TRAMOS
    # ==========================================

    def dibujarFuncion(self):
        """Dibuja la función por tramos cortando el trazo en las discontinuidades."""
        datos = self.datos or {}
        limites = datos.get("limites", {})
        funcion_data = datos.get("funcion", {})

        funcionEvaluar     = limites.get("funcionEvaluar")
        puntoAnalisis      = funcion_data.get("puntoAnalisis")
        tipoDiscontinuidad = funcion_data.get("tipo", "")

        if funcionEvaluar is None or puntoAnalisis is None or not tipoDiscontinuidad:
            return

        anchoLienzo = self.lienzo.winfo_width()
        cx     = self.centroX()
        xInicio = int((0 - cx) / self.escala) - 5
        xFin    = int((anchoLienzo - cx) / self.escala) + 5

        colorCurva  = COLOR_CURVA_FUNCION
        tramoActual = []
        xActual     = xInicio
        paso        = PASO_FUNCION

        while xActual <= xFin:
            valorY = funcionEvaluar(xActual)

            # Cortar trazo si no está definido o es muy grande
            if valorY is None or valorY == "Indefinido" or abs(valorY) > UMBRAL_DISCONTINUIDAD:
                if len(tramoActual) > 1:
                    self.trazarLinea(tramoActual, colorCurva)
                tramoActual = []
            else:
                tramoActual.append((xActual, valorY))

            xActual += paso

        # Dibujar el último tramo si quedó pendiente
        if len(tramoActual) > 1:
            self.trazarLinea(tramoActual, colorCurva)

        if tipoDiscontinuidad == "infinita":
            # Asíntota vertical
            pixelAsintota = self.aPixelX(puntoAnalisis)
            altoLienzo    = self.lienzo.winfo_height()
            self.lienzo.create_line(pixelAsintota, 0, pixelAsintota, altoLienzo,
                                    fill=COLOR_ASINTOTA, dash=(6, 4))
            self.lienzo.create_text(pixelAsintota + 8, 16, text=f"x = {puntoAnalisis}",
                                    fill=COLOR_ASINTOTA, anchor=tk.W, font=FUENTE_ASINTOTA)

        elif tipoDiscontinuidad == "removible":
            # Círculo vacío: punto no definido en x = a
            digitos = funcion_data.get("digitos", [])
            if not digitos:
                return
            valorLimite = puntoAnalisis + digitos[0]
            pixelXAgujero = self.aPixelX(puntoAnalisis)
            pixelYAgujero = self.aPixelY(valorLimite)
            self.lienzo.create_oval(
                pixelXAgujero - TAMANO_AGUJERO, pixelYAgujero - TAMANO_AGUJERO,
                pixelXAgujero + TAMANO_AGUJERO, pixelYAgujero + TAMANO_AGUJERO,
                outline=colorCurva, width=2, fill=COLOR_FONDO
            )

        elif tipoDiscontinuidad == "salto":
            digitos = funcion_data.get("digitos", [])
            if len(digitos) < 4:
                return
            d2 = digitos[1]
            d4 = digitos[3]
            valorIzquierda = puntoAnalisis + d2
            valorDerecha   = puntoAnalisis + d4

            # Círculo vacío: límite izquierdo (no pertenece)
            pixelXIzq = self.aPixelX(puntoAnalisis)
            pixelYIzq = self.aPixelY(valorIzquierda)
            self.lienzo.create_oval(
                pixelXIzq - TAMANO_AGUJERO, pixelYIzq - TAMANO_AGUJERO,
                pixelXIzq + TAMANO_AGUJERO, pixelYIzq + TAMANO_AGUJERO,
                outline=colorCurva, width=2, fill=COLOR_FONDO
            )
            self.lienzo.create_text(pixelXIzq + 8, pixelYIzq - 14,
                                    text=f"lím izq ({puntoAnalisis}, {valorIzquierda})",
                                    fill=colorCurva, anchor=tk.W, font=FUENTE_ETIQUETA)

            # Círculo lleno: valor real f(a) (pertenece)
            pixelXDer = self.aPixelX(puntoAnalisis)
            pixelYDer = self.aPixelY(valorDerecha)
            self.lienzo.create_oval(
                pixelXDer - TAMANO_AGUJERO, pixelYDer - TAMANO_AGUJERO,
                pixelXDer + TAMANO_AGUJERO, pixelYDer + TAMANO_AGUJERO,
                outline=colorCurva, width=2, fill=colorCurva
            )
            self.lienzo.create_text(pixelXDer + 8, pixelYDer + 6,
                                    text=f"f({puntoAnalisis}) = {valorDerecha}",
                                    fill=colorCurva, anchor=tk.W, font=FUENTE_ETIQUETA)

    # ==========================================
    # UTILIDADES DE DIBUJO
    # ==========================================

    def _dibujarOvalo(self, x1, y1, x2, y2, color):
        """Crea un óvalo con el estilo de curva actual."""
        self.lienzo.create_oval(x1, y1, x2, y2, outline=color, width=2)

    def trazarLinea(self, puntosMath, color):
        """Dibuja una línea continua a partir de una lista de puntos (x, y) matemáticos."""
        coordenadasPixel = []
        for xMath, yMath in puntosMath:
            coordenadasPixel.extend([self.aPixelX(xMath), self.aPixelY(yMath)])
        if len(coordenadasPixel) >= 4:
            self.lienzo.create_line(coordenadasPixel, fill=color, width=2)

    def marcarPunto(self, x, y, etiqueta):
        """Dibuja un punto con su etiqueta sobre el plano."""
        pixelX = self.aPixelX(x)
        pixelY = self.aPixelY(y)
        self.lienzo.create_oval(pixelX - TAMANO_MARCA, pixelY - TAMANO_MARCA,
                                pixelX + TAMANO_MARCA, pixelY + TAMANO_MARCA,
                                fill=COLOR_PUNTO)
        self.lienzo.create_text(pixelX + 10, pixelY - 12,
                                text=f"{etiqueta} ({round(x, 1)}, {round(y, 1)})",
                                fill=COLOR_PUNTO, anchor=tk.W, font=FUENTE_ETIQUETA)
