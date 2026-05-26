class ConicTransformer:

    def __init__(self, conica):

        self.conica = conica
        self.pasos = []

    # -----------------------------------
    # Decide transformación
    # -----------------------------------
    def transformar(self):

        tipo = self.conica.tipo

        if tipo == "Circunferencia":
            return self.transformar_circunferencia()

        elif tipo == "Elipse":
            return self.transformar_elipse()

        elif tipo == "Hipérbola":
            return self.transformar_hiperbola()

        elif tipo == "Parábola":
            return self.transformar_parabola()

    # -----------------------------------
    # Completa cuadrados
    # -----------------------------------
    def completar_cuadrado(self, termino):

        mitad = termino / 2

        cuadrado = mitad * mitad

        return mitad, cuadrado

    # -----------------------------------
    # Circunferencia
    # -----------------------------------
    def transformar_circunferencia(self):

        A = self.conica.A
        C = self.conica.C
        D = self.conica.D
        E = self.conica.E

        self.pasos.append("Transformación circunferencia")

        hx, cx = self.completar_cuadrado(C / A)
        hy, cy = self.completar_cuadrado(D / A)

        radio = (cx + cy - E / A)

        ecuacion = (
            f"(x + {hx})² + "
            f"(y + {hy})² = {radio}"
        )

        return ecuacion

    # -----------------------------------
    # Elipse
    # -----------------------------------
    def transformar_elipse(self):

        self.pasos.append("Transformación elipse")

        return "Forma canónica elipse"

    # -----------------------------------
    # Hipérbola
    # -----------------------------------
    def transformar_hiperbola(self):

        self.pasos.append("Transformación hipérbola")

        return "Forma canónica hipérbola"

    # -----------------------------------
    # Parábola
    # -----------------------------------
    def transformar_parabola(self):

        self.pasos.append("Transformación parábola")

        return "Forma canónica parábola"

    # -----------------------------------
    # Devuelve pasos
    # -----------------------------------
    def mostrar_pasos(self):

        return "\n".join(self.pasos)