# plotter.py - Graficador interactivo con Tkinter
# Dibuja cónicas y funciones por tramos en un plano cartesiano.
# Soporta: arrastre con clic izquierdo y zoom con la rueda del ratón.

import tkinter as tk


class Graficador:
    """Dibuja cónicas y funciones por tramos en un plano cartesiano interactivo."""

    def __init__(self, lienzo):
        self.lienzo         = lienzo
        self.escala         = 40   # Pixeles por unidad matemática
        self.desplazamientoX = 0   # Desplazamiento horizontal del origen (arrastre)
        self.desplazamientoY = 0   # Desplazamiento vertical del origen (arrastre)
        self.tipoGrafico    = None  # "conica" o "funcion"
        self.datos          = None  # Datos matemáticos a graficar
        self.arrastreInicialX = 0
        self.arrastreInicialY = 0

        # Vincular eventos del ratón al lienzo
        lienzo.bind("<Configure>",    self.dibujarTodo)
        lienzo.bind("<ButtonPress-1>", self.inicioArrastre)
        lienzo.bind("<B1-Motion>",     self.moverPlano)
        lienzo.bind("<Button-4>",      lambda e: self.hacerZoom(5))    # Linux: rueda arriba
        lienzo.bind("<Button-5>",      lambda e: self.hacerZoom(-5))   # Linux: rueda abajo
        lienzo.bind("<MouseWheel>",    lambda e: self.hacerZoom(5 if e.delta > 0 else -5))


    def inicioArrastre(self, evento): # Clic presionado
        
        self.arrastreInicialX = evento.x
        self.arrastreInicialY = evento.y

    def moverPlano(self, evento): # Mouse en movimiento
       
        self.desplazamientoX += evento.x - self.arrastreInicialX
        self.desplazamientoY += evento.y - self.arrastreInicialY
        self.arrastreInicialX = evento.x
        self.arrastreInicialY = evento.y
        self.dibujarTodo()

    def hacerZoom(self, cambioPorPaso):
        """Acerca o aleja el plano con la rueda del ratón. Escala entre 10 y 200 px/unidad."""
        self.escala = max(10, min(200, self.escala + cambioPorPaso))
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
        self.datos = datos
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

        # Fondo gris claro
        self.lienzo.create_rectangle(-2, -2, ancho + 4, alto + 4, fill="#f8f9fa", outline="")

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
            self.lienzo.create_line(pixelX, 0, pixelX, alto, fill="#e0e0e0", dash=(2, 4))

        for yUnidad in range(yInicio, yFin):
            pixelY = self.aPixelY(yUnidad)
            self.lienzo.create_line(0, pixelY, ancho, pixelY, fill="#e0e0e0", dash=(2, 4))

    def dibujarEjes(self, ancho, alto):
        """Dibuja los ejes X e Y con marcas numéricas."""
        cx = self.centroX()
        cy = self.centroY()

        # Ejes principales
        self.lienzo.create_line(0, cy, ancho, cy, fill="#495057", width=2)
        self.lienzo.create_line(cx, 0, cx, alto, fill="#495057", width=2)

        # Números en el eje X
        xInicio = int((0 - cx) / self.escala)
        xFin    = int((ancho - cx) / self.escala) + 1
        for xUnidad in range(xInicio, xFin):
            if xUnidad != 0:
                pixelX = self.aPixelX(xUnidad)
                self.lienzo.create_line(pixelX, cy - 4, pixelX, cy + 4, fill="#495057")
                self.lienzo.create_text(pixelX, cy + 14, text=str(xUnidad), fill="#6c757d", font=("Arial", 8))

        # Números en el eje Y
        yInicio = int((cy - alto) / self.escala)
        yFin    = int(cy / self.escala) + 1
        for yUnidad in range(yInicio, yFin):
            if yUnidad != 0:
                pixelY = self.aPixelY(yUnidad)
                self.lienzo.create_line(cx - 4, pixelY, cx + 4, pixelY, fill="#495057")
                self.lienzo.create_text(cx - 14, pixelY, text=str(yUnidad), fill="#6c757d", font=("Arial", 8))

    # ==========================================
    # DIBUJO DE CÓNICAS
    # ==========================================

    def dibujarConica(self):
        """Dibuja la cónica según su tipo: circunferencia, elipse, hipérbola o parábola."""
        tipoConica  = self.datos.get("tipo", "")
        centro      = self.datos.get("centro")
        parametros  = self.datos.get("parametros", {})

        if not centro:
            return

        h, k = centro
        colorCurva = "#007bff"

        if tipoConica == "Circunferencia":
            radio = parametros.get("r", 0)
            self.lienzo.create_oval(
                self.aPixelX(h - radio), self.aPixelY(k + radio),
                self.aPixelX(h + radio), self.aPixelY(k - radio),
                outline=colorCurva, width=2
            )
            self.marcarPunto(h, k, "Centro")

        elif tipoConica == "Elipse":
            semiEjeA = parametros.get("a2", 0) ** 0.5
            semiEjeB = parametros.get("b2", 0) ** 0.5
            self.lienzo.create_oval(
                self.aPixelX(h - semiEjeA), self.aPixelY(k + semiEjeB),
                self.aPixelX(h + semiEjeA), self.aPixelY(k - semiEjeB),
                outline=colorCurva, width=2
            )
            self.marcarPunto(h, k, "Centro")

        elif tipoConica == "Hipérbola":
            semiEjeA = parametros.get("a2", 0) ** 0.5
            semiEjeB = parametros.get("b2", 0) ** 0.5
            ramaDerecha   = []
            ramaIzquierda = []

            xActual = semiEjeA
            while xActual <= 25:
                valorBajoRaiz = ((xActual ** 2) / (semiEjeA ** 2)) - 1
                if valorBajoRaiz >= 0:
                    yValor = (valorBajoRaiz * semiEjeB ** 2) ** 0.5
                    ramaDerecha.insert(0, (h + xActual, k + yValor))
                    ramaDerecha.append((h + xActual, k - yValor))
                    ramaIzquierda.insert(0, (h - xActual, k + yValor))
                    ramaIzquierda.append((h - xActual, k - yValor))
                xActual += 0.1

            self.trazarLinea(ramaDerecha,   colorCurva)
            self.trazarLinea(ramaIzquierda, colorCurva)
            self.marcarPunto(h, k, "Centro")

        elif tipoConica == "Parábola":
            parametroP  = parametros.get("p", 0)
            orientacion = parametros.get("orientacion", "vertical")
            puntos      = []

            tActual = -25
            while tActual <= 25:
                if orientacion == "horizontal":
                    xValor = (tActual ** 2) / (4 * parametroP) if parametroP != 0 else 0
                    puntos.append((h + xValor, k + tActual))
                else:
                    yValor = (tActual ** 2) / (4 * parametroP) if parametroP != 0 else 0
                    puntos.append((h + tActual, k + yValor))
                tActual += 0.2

            self.trazarLinea(puntos, colorCurva)
            self.marcarPunto(h, k, "Vértice")

    # ==========================================
    # DIBUJO DE FUNCIONES POR TRAMOS
    # ==========================================

    def dibujarFuncion(self):
        """Dibuja la función por tramos cortando el trazo en las discontinuidades."""
        funcionEvaluar     = self.datos["limites"]["funcionEvaluar"]
        puntoAnalisis      = self.datos["funcion"]["puntoAnalisis"]
        tipoDiscontinuidad = self.datos["funcion"]["tipo"]

        anchoLienzo = self.lienzo.winfo_width()
        cx     = self.centroX()
        xInicio = int((0 - cx) / self.escala) - 5 #Calcular los bordes para que no se corten
        xFin    = int((anchoLienzo - cx) / self.escala) + 5

        colorCurva  = "#dc3545"
        tramoActual = []
        xActual     = xInicio
        paso        = 0.05

        while xActual <= xFin:
            valorY = funcionEvaluar(xActual)

            # Cortar el trazo si el valor no está definido o es muy grande (discontinuidad)
            if valorY is None or valorY == "Indefinido" or abs(valorY) > 100:
                if len(tramoActual) > 1:
                    self.trazarLinea(tramoActual, colorCurva)
                tramoActual = []
            else:
                tramoActual.append((xActual, valorY))

            xActual += paso

        # Dibujar el último tramo si quedó pendiente
        if len(tramoActual) > 1:
            self.trazarLinea(tramoActual, colorCurva)

        # Marcadores visuales según el tipo de discontinuidad
        if tipoDiscontinuidad == "infinita":
            # Asíntota vertical (línea punteada)
            pixelAsintota = self.aPixelX(puntoAnalisis)
            altoLienzo    = self.lienzo.winfo_height()
            self.lienzo.create_line(pixelAsintota, 0, pixelAsintota, altoLienzo,
                                    fill="#adb5bd", dash=(6, 4))
            self.lienzo.create_text(pixelAsintota + 8, 16, text=f"x = {puntoAnalisis}",
                                    fill="#adb5bd", anchor=tk.W, font=("Arial", 9, "italic"))

        elif tipoDiscontinuidad == "removible":
            # Círculo vacío: el punto NO está definido en x = a
            valorLimite = puntoAnalisis + self.datos["funcion"]["digitos"][0]   # límite = a + d1
            pixelXAgujero = self.aPixelX(puntoAnalisis)
            pixelYAgujero = self.aPixelY(valorLimite)
            radioCirculo  = 5
            self.lienzo.create_oval(
                pixelXAgujero - radioCirculo, pixelYAgujero - radioCirculo,
                pixelXAgujero + radioCirculo, pixelYAgujero + radioCirculo,
                outline=colorCurva, width=2, fill="#f8f9fa"
            )

        elif tipoDiscontinuidad == "salto":
            d2 = self.datos["funcion"]["digitos"][1]
            d4 = self.datos["funcion"]["digitos"][3]
            valorIzquierda = puntoAnalisis + d2   # lím(x→a⁻) = a + d2
            valorDerecha   = puntoAnalisis + d4   # lím(x→a⁺) = f(a) = a + d4
            radioCirculo   = 5

            # Círculo VACÍO: límite por la izquierda (el punto NO pertenece a la rama)
            pixelXIzq = self.aPixelX(puntoAnalisis)
            pixelYIzq = self.aPixelY(valorIzquierda)
            self.lienzo.create_oval(
                pixelXIzq - radioCirculo, pixelYIzq - radioCirculo,
                pixelXIzq + radioCirculo, pixelYIzq + radioCirculo,
                outline=colorCurva, width=2, fill="#f8f9fa"
            )
            self.lienzo.create_text(pixelXIzq + 8, pixelYIzq - 14,
                                    text=f"lím izq ({puntoAnalisis}, {valorIzquierda})",
                                    fill=colorCurva, anchor=tk.W, font=("Arial", 8))

            # Círculo LLENO: valor real de f(a) (el punto SÍ pertenece)
            pixelXDer = self.aPixelX(puntoAnalisis)
            pixelYDer = self.aPixelY(valorDerecha)
            self.lienzo.create_oval(
                pixelXDer - radioCirculo, pixelYDer - radioCirculo,
                pixelXDer + radioCirculo, pixelYDer + radioCirculo,
                outline=colorCurva, width=2, fill=colorCurva
            )
            self.lienzo.create_text(pixelXDer + 8, pixelYDer + 6,
                                    text=f"f({puntoAnalisis}) = {valorDerecha}",
                                    fill=colorCurva, anchor=tk.W, font=("Arial", 8))

    # ==========================================
    # UTILIDADES DE DIBUJO
    # ==========================================

    def trazarLinea(self, puntosMath, color):
        """Dibuja una línea continua a partir de una lista de puntos (x, y) matemáticos."""
        coordenadasPixel = []
        for xMath, yMath in puntosMath:
            coordenadasPixel.extend([self.aPixelX(xMath), self.aPixelY(yMath)])
        if len(coordenadasPixel) >= 4:
            self.lienzo.create_line(coordenadasPixel, fill=color, width=2)

    def marcarPunto(self, x, y, etiqueta):
        """Dibuja un punto negro con su etiqueta de texto sobre el plano."""
        pixelX = self.aPixelX(x)
        pixelY = self.aPixelY(y)
        self.lienzo.create_oval(pixelX - 4, pixelY - 4, pixelX + 4, pixelY + 4, fill="#212529")
        self.lienzo.create_text(pixelX + 10, pixelY - 12,
                                text=f"{etiqueta} ({round(x, 1)}, {round(y, 1)})",
                                fill="#212529", anchor=tk.W, font=("Arial", 9, "bold"))