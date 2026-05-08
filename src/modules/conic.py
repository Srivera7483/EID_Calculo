class Conic:

    def __init__(self, A, B, C, D, E):

        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.E = E

        self.tipo = self.clasificar()

    # -----------------------------------
    # Clasifica la cónica
    # -----------------------------------
    def clasificar(self):

        if (self.A == self.B) and (self.A != 0):
            return "Circunferencia"

        elif (self.A == 0) or (self.B == 0):
            return "Parábola"

        elif (self.A * self.B) < 0:
            return "Hipérbola"

        elif (self.A * self.B) > 0 and (self.A != self.B):
            return "Elipse"

        return "Desconocida"

    # -----------------------------------
    # Genera ecuación general
    # -----------------------------------
    def obtener_ecuacion_general(self):

        ecuacion = (
            f"{self.A}x² + "
            f"{self.B}y² + "
            f"{self.C}x + "
            f"{self.D}y + "
            f"{self.E} = 0"
        )

        return ecuacion

    # -----------------------------------
    # Devuelve información
    # -----------------------------------
    def obtener_info(self):

        return {
            "A": self.A,
            "B": self.B,
            "C": self.C,
            "D": self.D,
            "E": self.E,
            "tipo": self.tipo
        }

    # -----------------------------------
    # Representación en texto
    # -----------------------------------
    def __str__(self):

        return (
            f"Tipo: {self.tipo}\n"
            f"Ecuación: {self.obtener_ecuacion_general()}"
        )