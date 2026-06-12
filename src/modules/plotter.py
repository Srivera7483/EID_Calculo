class Plotter:

    def __init__(self, canvas, width=800, height=600):

        self.canvas = canvas

        self.width = width
        self.height = height

        # Escala matemática
        self.scale = 40

        # Centro del plano
        self.center_x = width // 2
        self.center_y = height // 2

    # =========================================
    # LIMPIAR CANVAS
    # =========================================
    def limpiar(self):

        self.canvas.delete("all")

    # =========================================
    # CONVERTIR COORDENADAS
    # =========================================
    def convertir_x(self, x):

        return self.center_x + (x * self.scale)

    def convertir_y(self, y):

        return self.center_y - (y * self.scale)

    # =========================================
    # DIBUJAR EJES
    # =========================================
    def dibujar_ejes(self):

        # Eje X
        self.canvas.create_line(
            0,
            self.center_y,
            self.width,
            self.center_y,
            fill="black"
        )

        # Eje Y
        self.canvas.create_line(
            self.center_x,
            0,
            self.center_x,
            self.height,
            fill="black"
        )

        # Marcas eje X
        for x in range(-10, 11):

            px = self.convertir_x(x)

            self.canvas.create_line(
                px,
                self.center_y - 5,
                px,
                self.center_y + 5
            )

            self.canvas.create_text(
                px,
                self.center_y + 15,
                text=str(x)
            )

        # Marcas eje Y
        for y in range(-10, 11):

            py = self.convertir_y(y)

            self.canvas.create_line(
                self.center_x - 5,
                py,
                self.center_x + 5,
                py
            )

            if y != 0:
                self.canvas.create_text(
                    self.center_x - 15,
                    py,
                    text=str(y)
                )

    # =========================================
    # DIBUJAR PUNTO
    # =========================================
    def dibujar_punto(self, x, y, color="red"):

        px = self.convertir_x(x)
        py = self.convertir_y(y)

        self.canvas.create_oval(
            px - 2,
            py - 2,
            px + 2,
            py + 2,
            fill=color,
            outline=color
        )

    # =========================================
    # DIBUJAR CIRCUNFERENCIA
    # Forma:
    # (x-h)^2 + (y-k)^2 = r^2
    # =========================================
    def dibujar_circunferencia(self, h, k, r):

        x = -r

        while x <= r:

            valor = (r * r) - (x * x)

            if valor >= 0:

                y = valor ** 0.5

                self.dibujar_punto(h + x, k + y, "blue")
                self.dibujar_punto(h + x, k - y, "blue")

            x += 0.01

    # =========================================
    # DIBUJAR ELIPSE
    # ((x-h)^2 / a^2) + ((y-k)^2 / b^2) = 1
    # =========================================
    def dibujar_elipse(self, h, k, a, b):

        x = -a

        while x <= a:

            valor = 1 - ((x * x) / (a * a))

            if valor >= 0:

                y = (valor * (b * b)) ** 0.5

                self.dibujar_punto(h + x, k + y, "green")
                self.dibujar_punto(h + x, k - y, "green")

            x += 0.01

    # =========================================
    # DIBUJAR HIPÉRBOLA
    # ((x-h)^2 / a^2) - ((y-k)^2 / b^2) = 1
    # =========================================
    def dibujar_hiperbola(self, h, k, a, b):

        x = a

        while x <= 20:

            valor = ((x * x) / (a * a)) - 1

            if valor >= 0:

                y = (valor * (b * b)) ** 0.5

                # Rama derecha
                self.dibujar_punto(h + x, k + y, "purple")
                self.dibujar_punto(h + x, k - y, "purple")

                # Rama izquierda
                self.dibujar_punto(h - x, k + y, "purple")
                self.dibujar_punto(h - x, k - y, "purple")

            x += 0.02

    # =========================================
    # DIBUJAR PARÁBOLA VERTICAL
    # (x-h)^2 = 4p(y-k)
    # =========================================
    def dibujar_parabola_vertical(self, h, k, p):

        x = -20

        while x <= 20:

            y = ((x * x) / (4 * p))

            self.dibujar_punto(h + x, k + y, "orange")

            x += 0.02

    # =========================================
    # DIBUJAR PARÁBOLA HORIZONTAL
    # (y-k)^2 = 4p(x-h)
    # =========================================
    def dibujar_parabola_horizontal(self, h, k, p):

        y = -20

        while y <= 20:

            x = ((y * y) / (4 * p))

            self.dibujar_punto(h + x, k + y, "orange")

            y += 0.02

    # =========================================
    # DIBUJAR FUNCIÓN POR TRAMOS
    # =========================================
    def dibujar_funcion(self, funcion):

        x = -10

        ultimo_x = None
        ultimo_y = None

        while x <= 10:

            y = funcion(x)

            # Saltar indefinidos
            if y == "Indefinido":

                ultimo_x = None
                ultimo_y = None

                x += 0.01
                continue

            # Saltar infinitos enormes
            if abs(y) > 1000:

                ultimo_x = None
                ultimo_y = None

                x += 0.01
                continue

            px = self.convertir_x(x)
            py = self.convertir_y(y)

            # Dibujar línea continua
            if ultimo_x is not None:

                self.canvas.create_line(
                    ultimo_x,
                    ultimo_y,
                    px,
                    py,
                    fill="red"
                )

            ultimo_x = px
            ultimo_y = py

            x += 0.01

    # =========================================
    # DIBUJAR ASÍNTOTA VERTICAL
    # =========================================
    def dibujar_asintota_vertical(self, x):

        px = self.convertir_x(x)

        self.canvas.create_line(
            px,
            0,
            px,
            self.height,
            dash=(5, 5),
            fill="gray"
        )

    # =========================================
    # ACTUALIZAR
    # =========================================
    def actualizar(self):

        self.canvas.update()