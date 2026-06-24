# transformations.py - Transformación entre ecuación general y canónica
# ============================================================================
# GENERAL → CANÓNICA:
#   1. Completar cuadrados para x e y
#   2. Identificar tipo de cónica y calcular parámetros (centro, semiejes, etc.)
#
# CANÓNICA → GENERAL (inversa):
#   1. Expandir la forma canónica algebraicamente
#   2. Reorganizar términos para obtener Ax² + By² + Cx + Dy + E = 0


def transformarACanonica(coeficientes):
    """
    Transforma la ecuación general a forma canónica completando cuadrados.

    Parámetros:
        coeficientes (dict): {'A', 'B', 'C', 'D', 'E': float}

    Retorna:
        dict: {
            'tipo': str,
            'formaCanonica': str,
            'centro': tuple(float, float) o None,
            'parametros': dict,
            'geometria': dict,
            'pasos': list[str]
        }
    """
    pasos = []
    A = coeficientes['A']
    B = coeficientes['B']
    C = coeficientes['C']
    D = coeficientes['D']
    E = coeficientes['E']

    pasos.append("=== TRANSFORMACIÓN GENERAL → CANÓNICA ===")
    pasos.append(f"Ecuación general: {A}x² + {B}y² + {C}x + {D}y + {E} = 0")
    pasos.append("")

    tipoConica   = "Desconocida"
    formaCanonica = ""
    centro       = None
    parametros   = {}

    if A != 0 and B != 0:
        # ── Caso: Circunferencia, Elipse o Hipérbola ──────────────────────────
        # El centro (h, k) se obtiene directamente al completar cuadrados
        h = -C / (2 * A)
        k = -D / (2 * B)

        # Términos que se suman a ambos lados para completar el cuadrado
        completacionX = (C / (2 * A)) ** 2
        completacionY = (D / (2 * B)) ** 2

        # Término independiente del lado derecho tras reordenar
        terminoLadoDerecho = -E + A * completacionX + B * completacionY

        pasos.append("PASO 1: Agrupar y factorizar términos con x e y")
        pasos.append(f"{A}(x² + {C/A:.2f}x) + {B}(y² + {D/B:.2f}y) = {-E}")

        pasos.append("PASO 2: Completar cuadrados")
        pasos.append(
            f"{A}(x² + {C/A:.2f}x + {completacionX:.2f}) + "
            f"{B}(y² + {D/B:.2f}y + {completacionY:.2f}) = "
            f"{-E} + {A*completacionX:.2f} + {B*completacionY:.2f}"
        )
        pasos.append(f"{A}(x - {h:.2f})² + {B}(y - {k:.2f})² = {terminoLadoDerecho:.2f}")

        centro = (round(h, 2), round(k, 2))

        if terminoLadoDerecho != 0:
            # Dividimos por F para igualar a 1 (forma canónica estándar)
            denominadorX = terminoLadoDerecho / A
            denominadorY = terminoLadoDerecho / B

            # Clasificar con tolerancia para comparar flotantes de forma segura
            if abs(A - B) < 1e-9:
                tipoConica = "Circunferencia"
                radio2 = terminoLadoDerecho / A
                formaCanonica = f"(x - {h:.2f})² + (y - {k:.2f})² = {radio2:.4f}"
                parametros['r'] = radio2 ** 0.5 if radio2 > 0 else 0
            elif A * B > 0:
                tipoConica = "Elipse"
                formaCanonica = f"(x - {h:.2f})² / {denominadorX:.2f} + (y - {k:.2f})² / {denominadorY:.2f} = 1"
            else:
                tipoConica = "Hipérbola"
                formaCanonica = f"(x - {h:.2f})² / {denominadorX:.2f} + (y - {k:.2f})² / {denominadorY:.2f} = 1"

            parametros['a2'] = abs(denominadorX)
            parametros['b2'] = abs(denominadorY)
        else:
            formaCanonica = f"{A}(x - {h:.2f})² + {B}(y - {k:.2f})² = 0"
            tipoConica = "Cónica Degenerada (Punto)"

    elif A == 0 and B != 0 and C != 0:
        # ── Caso: Parábola horizontal  (y² = ...)  ────────────────────────────
        tipoConica = "Parábola"
        k = -D / (2 * B)
        completacionY = (D / (2 * B)) ** 2
        terminoLibre = B * completacionY - E
        h = terminoLibre / C

        pasos.append("PASO 1: Agrupar la variable al cuadrado (y²)")
        pasos.append(f"{B}(y² + {D/B:.2f}y) = {-C}x + {-E}")

        pasos.append("PASO 2: Completar cuadrados en y")
        pasos.append(f"{B}(y² + {D/B:.2f}y + {completacionY:.2f}) = {-C}x - {E} + {B*completacionY:.2f}")
        pasos.append(f"{B}(y - {k:.2f})² = {-C}(x - {h:.2f})")

        formaCanonica = f"(y - {k:.2f})² = {-C/B:.2f}(x - {h:.2f})"
        centro = (round(h, 2), round(k, 2))    # En parábola, este punto es el vértice
        parametros['p']           = (-C / B) / 4
        parametros['orientacion'] = 'horizontal'

    elif B == 0 and A != 0 and D != 0:
        # ── Caso: Parábola vertical  (x² = ...)  ─────────────────────────────
        tipoConica = "Parábola"
        h = -C / (2 * A)
        completacionX = (C / (2 * A)) ** 2
        terminoLibre = A * completacionX - E
        k = terminoLibre / D

        pasos.append("PASO 1: Agrupar la variable al cuadrado (x²)")
        pasos.append(f"{A}(x² + {C/A:.2f}x) = {-D}y + {-E}")

        pasos.append("PASO 2: Completar cuadrados en x")
        pasos.append(f"{A}(x² + {C/A:.2f}x + {completacionX:.2f}) = {-D}y - {E} + {A*completacionX:.2f}")
        pasos.append(f"{A}(x - {h:.2f})² = {-D}(y - {k:.2f})")

        formaCanonica = f"(x - {h:.2f})² = {-D/A:.2f}(y - {k:.2f})"
        centro = (round(h, 2), round(k, 2))    # Vértice
        parametros['p']           = (-D / A) / 4
        parametros['orientacion'] = 'vertical'

    else:
        tipoConica    = "Caso no soportado / Línea recta"
        formaCanonica = "No aplicable"

    pasos.append("")
    pasos.append(f"-> Ecuación Canónica Resultante: {formaCanonica}")
    if centro:
        pasos.append(f"-> Centro/Vértice: {centro}")

    # Calcular parámetros geométricos adicionales (vértices, focos, excentricidad...)
    datosGeometricos = calcularParametros(tipoConica, coeficientes, centro, parametros)
    pasos.append("")
    pasos.extend(datosGeometricos['pasos'])

    return {
        'tipo':         tipoConica,
        'formaCanonica': formaCanonica,
        'centro':       centro,
        'parametros':   parametros,
        'geometria':    datosGeometricos,
        'pasos':        pasos
    }


def transformarAGeneral(tipoConica, formaCanonica, centro, parametros):
    """
    Transforma la forma canónica de vuelta a la ecuación general.
    Muestra paso a paso la expansión algebraica.

    Parámetros:
        tipoConica    (str):   Tipo de cónica
        formaCanonica (str):   Ecuación canónica (para referencia visual)
        centro        (tuple): (h, k) centro o vértice
        parametros    (dict):  Parámetros geométricos (a2, b2, r, p, orientacion)

    Retorna:
        dict: {'ecuacionGeneral': str, 'coeficientes': dict, 'pasos': list[str]}
    """
    pasos = []
    pasos.append("=== TRANSFORMACIÓN CANÓNICA → GENERAL ===")
    pasos.append(f"Forma canónica: {formaCanonica}")
    pasos.append(f"Centro/Vértice: {centro}")
    pasos.append("")

    if centro is None:
        pasos.append("No se puede realizar la transformación inversa: centro no definido.")
        return {'ecuacionGeneral': "N/A", 'coeficientes': {}, 'pasos': pasos}

    h, k = centro

    if tipoConica in ("Circunferencia", "Elipse", "Hipérbola"):
        a2 = parametros.get('a2', 1)
        b2 = parametros.get('b2', 1)

        if tipoConica == "Circunferencia":
            radio  = parametros.get('r', 0)
            radio2 = radio * radio

            pasos.append("PASO 1: Partimos de la forma canónica")
            pasos.append(f"(x - {h:.2f})² + (y - {k:.2f})² = {radio2:.2f}")
            pasos.append("")

            pasos.append("PASO 2: Expandir binomios al cuadrado")
            pasos.append(f"(x² - {2*h:.2f}x + {h*h:.2f}) + (y² - {2*k:.2f}y + {k*k:.2f}) = {radio2:.2f}")
            pasos.append("")

            A, B  = 1, 1
            C, D  = -2 * h, -2 * k
            E     = h*h + k*k - radio2

            pasos.append("PASO 3: Reagrupar en forma general")
            pasos.append(f"x² + y² - {2*h:.2f}x - {2*k:.2f}y + {E:.2f} = 0")

        else:
            # Elipse o Hipérbola
            signo  = "+" if tipoConica == "Elipse" else "-"
            coefA  = 1 / a2
            coefB  = 1 / b2 if tipoConica == "Elipse" else -1 / b2

            pasos.append("PASO 1: Partimos de la forma canónica")
            pasos.append(f"(x - {h:.2f})²/{a2:.2f} {signo} (y - {k:.2f})²/{b2:.2f} = 1")
            pasos.append("")

            pasos.append("PASO 2: Multiplicar todo por los denominadores")
            pasos.append(f"{coefA:.4f}(x - {h:.2f})² + {coefB:.4f}(y - {k:.2f})² = 1")
            pasos.append("")

            pasos.append("PASO 3: Expandir binomios al cuadrado")
            pasos.append(
                f"{coefA:.4f}(x² - {2*h:.2f}x + {h*h:.2f}) + "
                f"{coefB:.4f}(y² - {2*k:.2f}y + {k*k:.2f}) = 1"
            )
            pasos.append("")

            A = coefA
            B = coefB
            C = -2 * h * coefA
            D = -2 * k * coefB
            E = coefA * (h*h) + coefB * (k*k) - 1

            pasos.append("PASO 4: Reagrupar en forma general Ax² + By² + Cx + Dy + E = 0")
            pasos.append(f"{A:.4f}x² + {B:.4f}y² + ({C:.4f})x + ({D:.4f})y + ({E:.4f}) = 0")

    elif tipoConica == "Parábola":
        p           = parametros.get('p', 0)
        orientacion = parametros.get('orientacion', 'vertical')

        if orientacion == 'vertical':
            pasos.append("PASO 1: Partimos de la forma canónica")
            pasos.append(f"(x - {h:.2f})² = {4*p:.2f}(y - {k:.2f})")
            pasos.append("")

            pasos.append("PASO 2: Expandir binomio izquierdo")
            pasos.append(f"x² - {2*h:.2f}x + {h*h:.2f} = {4*p:.2f}y - {4*p*k:.2f}")
            pasos.append("")

            A = 1
            B = 0
            C = -2 * h
            D = -4 * p
            E = h*h + 4*p*k

            pasos.append("PASO 3: Reagrupar")
            pasos.append(f"{A}x² + ({C:.2f})x + ({D:.2f})y + ({E:.2f}) = 0")

        else:   # horizontal
            pasos.append("PASO 1: Partimos de la forma canónica")
            pasos.append(f"(y - {k:.2f})² = {4*p:.2f}(x - {h:.2f})")
            pasos.append("")

            pasos.append("PASO 2: Expandir binomio izquierdo")
            pasos.append(f"y² - {2*k:.2f}y + {k*k:.2f} = {4*p:.2f}x - {4*p*h:.2f}")
            pasos.append("")

            A = 0
            B = 1
            C = -4 * p
            D = -2 * k
            E = k*k + 4*p*h

            pasos.append("PASO 3: Reagrupar")
            pasos.append(f"{B}y² + ({C:.2f})x + ({D:.2f})y + ({E:.2f}) = 0")

    else:
        A, B, C, D, E = 0, 0, 0, 0, 0
        pasos.append("Tipo de cónica no soportado para la transformación inversa.")

    pasos.append("")
    pasos.append(f"→ Ecuación General recuperada: A={A:.4f}, B={B:.4f}, C={C:.4f}, D={D:.4f}, E={E:.4f}")

    return {
        'ecuacionGeneral': f"{A:.4f}x² + {B:.4f}y² + ({C:.4f})x + ({D:.4f})y + ({E:.4f}) = 0",
        'coeficientes':    {'A': A, 'B': B, 'C': C, 'D': D, 'E': E},
        'pasos':           pasos
    }


def calcularParametros(tipo, coeficientes, centro, parametros):
    """
    Calcula los parámetros geométricos de la cónica:
    vértices, focos, semiejes, excentricidad y directriz/asíntotas.

    Parámetros:
        tipo         (str):   Tipo de cónica
        coeficientes (dict):  Coeficientes A, B, C, D, E
        centro       (tuple): (h, k) centro o vértice
        parametros   (dict):  a2, b2, r, p, orientacion según corresponda

    Retorna:
        dict: {
            'vertices', 'focos': list[tuple],
            'excentricidad', 'ejeTransverso', 'ejeConjugado': float o None,
            'directriz': str o None,
            'pasos': list[str]
        }
    """
    pasos = []
    pasos.append("=== PARÁMETROS GEOMÉTRICOS ===")

    vertices      = []
    focos         = []
    excentricidad = None
    ejeTransverso = None
    ejeConjugado  = None
    directriz     = None

    if centro is None:
        pasos.append("No se pueden calcular parámetros: centro no definido.")
        return {
            'vertices': [], 'focos': [], 'excentricidad': None,
            'ejeTransverso': None, 'ejeConjugado': None, 'directriz': None,
            'pasos': pasos
        }

    h, k = centro

    if tipo == "Circunferencia":
        radio = parametros.get('r', 0)

        # Los "vértices" de la circunferencia son los cuatro puntos cardinales
        vertices = [
            (round(h + radio, 4), k),
            (round(h - radio, 4), k),
            (h, round(k + radio, 4)),
            (h, round(k - radio, 4))
        ]
        focos         = [(h, k)]     # En una circunferencia el foco coincide con el centro
        excentricidad = 0.0
        ejeTransverso = round(2 * radio, 4)
        ejeConjugado  = round(2 * radio, 4)

        pasos.append(f"Radio: r = √{radio**2:.4f} = {radio:.4f}")
        pasos.append(f"Vértices (puntos cardinales): {vertices}")
        pasos.append(f"Centro (único foco): ({h}, {k})")
        pasos.append(f"Excentricidad: e = 0 (circunferencia perfecta)")
        pasos.append(f"Diámetro: {ejeTransverso:.4f}")

    elif tipo == "Elipse":
        a2 = parametros.get('a2', 1)
        b2 = parametros.get('b2', 1)

        # Convenio: 'a' siempre es el semieje MAYOR
        if a2 >= b2:
            # Eje mayor en dirección horizontal (x)
            semiEjeMayor = a2 ** 0.5
            semiEjeMenor = b2 ** 0.5
            distanciaFocal2 = a2 - b2
            distanciaFocal  = distanciaFocal2 ** 0.5 if distanciaFocal2 >= 0 else 0
            vertices = [
                (round(h + semiEjeMayor, 4), k),
                (round(h - semiEjeMayor, 4), k),
                (h, round(k + semiEjeMenor, 4)),
                (h, round(k - semiEjeMenor, 4))
            ]
            focos = [
                (round(h + distanciaFocal, 4), k),
                (round(h - distanciaFocal, 4), k)
            ]
            pasos.append(f"Semieje mayor (a): √{a2:.4f} = {semiEjeMayor:.4f} (dirección x)")
            pasos.append(f"Semieje menor (b): √{b2:.4f} = {semiEjeMenor:.4f} (dirección y)")
        else:
            # Eje mayor en dirección vertical (y)
            semiEjeMayor = b2 ** 0.5
            semiEjeMenor = a2 ** 0.5
            distanciaFocal2 = b2 - a2
            distanciaFocal  = distanciaFocal2 ** 0.5 if distanciaFocal2 >= 0 else 0
            vertices = [
                (h, round(k + semiEjeMayor, 4)),
                (h, round(k - semiEjeMayor, 4)),
                (round(h + semiEjeMenor, 4), k),
                (round(h - semiEjeMenor, 4), k)
            ]
            focos = [
                (h, round(k + distanciaFocal, 4)),
                (h, round(k - distanciaFocal, 4))
            ]
            pasos.append(f"Semieje mayor (a): √{b2:.4f} = {semiEjeMayor:.4f} (dirección y)")
            pasos.append(f"Semieje menor (b): √{a2:.4f} = {semiEjeMenor:.4f} (dirección x)")

        ejeTransverso = round(2 * semiEjeMayor, 4)
        ejeConjugado  = round(2 * semiEjeMenor, 4)
        excentricidad = round(distanciaFocal / semiEjeMayor, 4) if semiEjeMayor > 0 else 0

        pasos.append(f"c (distancia focal): √(a²-b²) = √{distanciaFocal2:.4f} = {distanciaFocal:.4f}")
        pasos.append(f"Focos: {focos}")
        pasos.append(f"Vértices: {vertices}")
        pasos.append(f"Excentricidad: e = c/a = {excentricidad}  (0 < e < 1 → Elipse)")
        pasos.append(f"Eje mayor (2a): {ejeTransverso},  Eje menor (2b): {ejeConjugado}")

    elif tipo == "Hipérbola":
        a2 = parametros.get('a2', 1)
        b2 = parametros.get('b2', 1)
        semiEjeTransverso = a2 ** 0.5
        semiEjeConjugado  = b2 ** 0.5
        distanciaFocal2   = a2 + b2
        distanciaFocal    = distanciaFocal2 ** 0.5
        excentricidad     = round(distanciaFocal / semiEjeTransverso, 4) if semiEjeTransverso > 0 else 0

        # Vértices sobre el eje transverso (horizontal por defecto)
        vertices = [
            (round(h + semiEjeTransverso, 4), k),
            (round(h - semiEjeTransverso, 4), k)
        ]
        focos = [
            (round(h + distanciaFocal, 4), k),
            (round(h - distanciaFocal, 4), k)
        ]
        ejeTransverso = round(2 * semiEjeTransverso, 4)
        ejeConjugado  = round(2 * semiEjeConjugado, 4)

        # Asíntotas: y - k = ±(b/a)(x - h)
        pendienteAsintota = round(semiEjeConjugado / semiEjeTransverso, 4) if semiEjeTransverso > 0 else 0
        directriz = (
            f"y - {k} = ±{pendienteAsintota}(x - {h})  "
            f"[Asíntotas: y = {pendienteAsintota}x + {round(k - pendienteAsintota*h, 4)} "
            f"e y = {-pendienteAsintota}x + {round(k + pendienteAsintota*h, 4)}]"
        )

        pasos.append(f"Semieje transverso (a): √{a2:.4f} = {semiEjeTransverso:.4f}")
        pasos.append(f"Semieje conjugado  (b): √{b2:.4f} = {semiEjeConjugado:.4f}")
        pasos.append(f"c = √(a²+b²) = √{distanciaFocal2:.4f} = {distanciaFocal:.4f}")
        pasos.append(f"Vértices: {vertices}")
        pasos.append(f"Focos: {focos}")
        pasos.append(f"Excentricidad: e = c/a = {excentricidad}  (e > 1 → Hipérbola)")
        pasos.append(f"Eje transverso (2a): {ejeTransverso},  Eje conjugado (2b): {ejeConjugado}")
        pasos.append(f"Asíntotas: {directriz}")

    elif tipo == "Parábola":
        parametroP  = parametros.get('p', 0)
        orientacion = parametros.get('orientacion', 'vertical')
        excentricidad = 1.0

        if orientacion == 'vertical':
            # Forma canónica: (x-h)² = 4p(y-k)
            foco     = (h, round(k + parametroP, 4))
            focos    = [foco]
            vertices = [(h, k)]
            directriz = f"y = {round(k - parametroP, 4)}"

            pasos.append(f"Vértice: ({h}, {k})")
            pasos.append(f"Parámetro p: {parametroP:.4f}")
            pasos.append(f"Foco: {foco}")
            pasos.append(f"Directriz: {directriz}")
            pasos.append(f"Apertura: {'hacia arriba' if parametroP > 0 else 'hacia abajo'}")

        else:
            # Forma canónica: (y-k)² = 4p(x-h)
            foco     = (round(h + parametroP, 4), k)
            focos    = [foco]
            vertices = [(h, k)]
            directriz = f"x = {round(h - parametroP, 4)}"

            pasos.append(f"Vértice: ({h}, {k})")
            pasos.append(f"Parámetro p: {parametroP:.4f}")
            pasos.append(f"Foco: {foco}")
            pasos.append(f"Directriz: {directriz}")
            pasos.append(f"Apertura: {'hacia la derecha' if parametroP > 0 else 'hacia la izquierda'}")

        pasos.append(f"Excentricidad: e = 1 (Parábola)")

    else:
        pasos.append(f"Tipo '{tipo}' no soportado para el cálculo de parámetros.")

    return {
        'vertices':      vertices,
        'focos':         focos,
        'excentricidad': excentricidad,
        'ejeTransverso': ejeTransverso,
        'ejeConjugado':  ejeConjugado,
        'directriz':     directriz,
        'pasos':         pasos
    }
