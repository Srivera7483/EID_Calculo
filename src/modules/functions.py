# functions.py - Análisis de funciones por tramos y límites laterales
# ============================================================================
# FASE 6: Función generada desde los dígitos del RUT
#
# Punto de análisis: a = d3
# Tipo de discontinuidad según d8 mod 3:
#   0 → Discontinuidad removible
#   1 → Discontinuidad de salto
#   2 → Discontinuidad infinita (asintótica)


def generarFuncionPorTramos(digitos):
    """
    Genera la función por tramos y clasifica el tipo de discontinuidad.

    Parámetros:
        digitos (list[int]): [d1, d2, d3, d4, d5, d6, d7, d8]

    Retorna:
        dict: {
            'funcionFormula': str,
            'puntoAnalisis': int,   # a = d3
            'tipo': str,            # 'removible', 'salto' o 'infinita'
            'digitos': list[int],
            'pasos': list[str]
        }
    """
    pasos = []
    d1, d2, d3, d4, d5, d6, d7, d8 = digitos

    pasos.append(f"Dígitos del RUT: {digitos}")
    pasos.append(f"Punto de análisis: a = d3 = {d3}")
    pasos.append("")

    # El residuo de d8 mod 3 determina el tipo de discontinuidad
    residuo = d8 % 3
    pasos.append(f"d8 mod 3 = {d8} mod 3 = {residuo}")

    if residuo == 0:
        tipo = "removible"
        pasos.append("Tipo: DISCONTINUIDAD REMOVIBLE")
        pasos.append(f"f(x) = (x - {d3})(x + {d1}) / (x - {d3})")
        formula = f"(x - {d3})(x + {d1}) / (x - {d3})"

    elif residuo == 1:
        tipo = "salto"
        pasos.append("Tipo: DISCONTINUIDAD DE SALTO")
        pasos.append(f"f(x) = {{x + {d2},  si x < {d3}")
        pasos.append(f"       {{x + {d4},  si x ≥ {d3}")
        formula = f"(x + {d2}) si x < {d3},  (x + {d4}) si x ≥ {d3}"

    else:   # residuo == 2
        tipo = "infinita"
        pasos.append("Tipo: DISCONTINUIDAD INFINITA (asintótica)")
        pasos.append(f"f(x) = ({d5} + 1) / (x - {d3})")
        formula = f"({d5} + 1) / (x - {d3})"

    return {
        'funcionFormula': formula,
        'puntoAnalisis': d3,
        'tipo': tipo,
        'digitos': digitos,
        'pasos': pasos
    }


def calcularLimitesLaterales(formula, puntoAnalisis, tipo, digitos):
    """
    Calcula los límites laterales evaluando la función en valores cercanos al punto.

    Parámetros:
        formula (str): Fórmula de la función (solo para referencia visual)
        puntoAnalisis (int): Punto 'a' donde se analiza la discontinuidad
        tipo (str): 'removible', 'salto' o 'infinita'
        digitos (list[int]): Dígitos del RUT

    Retorna:
        dict: {
            'limiteIzquierda', 'limiteDerecha': float o str (±∞),
            'existeLimite': bool,
            'valores': dict,
            'funcionEvaluar': callable,
            'pasos': list[str]
        }
    """
    pasos = []
    d1, d2, d3, d4, d5, d6, d7, d8 = digitos

    pasos.append("=== CÁLCULO DE LÍMITES LATERALES ===")
    pasos.append(f"Punto de análisis: x → {puntoAnalisis}")
    pasos.append("")

    def evaluar(x):
        """Evalúa f(x) según el tipo de función. Retorna None si no está definida."""
        try:
            if tipo == 'removible':
                if x == d3:
                    return None        # El punto no está definido (denominador cero)
                return (x - d3) * (x + d1) / (x - d3)
            elif tipo == 'salto':
                return x + d2 if x < d3 else x + d4
            elif tipo == 'infinita':
                if x == d3:
                    return None        # El punto no está definido (asíntota vertical)
                return (d5 + 1) / (x - d3)
        except ZeroDivisionError:
            return None

    # Valores por la izquierda: nos acercamos al punto desde abajo
    desplazamientosIzquierda = [-1, -0.1, -0.01, -0.001]
    valoresIzquierda = {}
    for desplazamiento in desplazamientosIzquierda:
        xCercano = puntoAnalisis + desplazamiento
        valoresIzquierda[xCercano] = evaluar(xCercano)

    # Valores por la derecha: nos acercamos al punto desde arriba
    desplazamientosDerecha = [0.001, 0.01, 0.1, 1]
    valoresDerecha = {}
    for desplazamiento in desplazamientosDerecha:
        xCercano = puntoAnalisis + desplazamiento
        valoresDerecha[xCercano] = evaluar(xCercano)

    # Mostrar tabla de valores
    pasos.append(f"Tabla de valores cercanos a x = {puntoAnalisis}:")
    pasos.append(f"{'Izquierda (x)':<15} | {'f(x)':<15} || {'Derecha (x)':<15} | {'f(x)':<15}")
    pasos.append("-" * 68)

    for i in range(4):
        xIzq = puntoAnalisis + desplazamientosIzquierda[3 - i]   # De más lejano a más cercano
        fIzq = valoresIzquierda[xIzq]
        textofIzq = f"{fIzq:.4f}" if fIzq is not None else "Indefinido"

        xDer = puntoAnalisis + desplazamientosDerecha[i]          # De más cercano a más lejano
        fDer = valoresDerecha[xDer]
        textofDer = f"{fDer:.4f}" if fDer is not None else "Indefinido"

        pasos.append(f"{xIzq:<15.4f} | {textofIzq:<15} || {xDer:<15.4f} | {textofDer:<15}")

    # Estimar los límites usando el valor más cercano al punto
    fIzqCercano = valoresIzquierda[puntoAnalisis - 0.001]
    fDerCercano = valoresDerecha[puntoAnalisis + 0.001]

    if tipo == 'infinita':
        # Los límites tienden a ±∞
        limiteIzquierda = "-∞" if fIzqCercano < 0 else "+∞"
        limiteDerecha   = "-∞" if fDerCercano < 0 else "+∞"
    else:
        limiteIzquierda = round(fIzqCercano, 2)
        limiteDerecha   = round(fDerCercano, 2)

    existeLimite = (limiteIzquierda == limiteDerecha) and (tipo != 'infinita')

    pasos.append("")
    pasos.append(f"Límite por la izquierda (lím x→{puntoAnalisis}⁻): {limiteIzquierda}")
    pasos.append(f"Límite por la derecha   (lím x→{puntoAnalisis}⁺): {limiteDerecha}")
    pasos.append(f"¿Existe el límite ordinario?: {'Sí' if existeLimite else 'No'}")

    return {
        'limiteIzquierda': limiteIzquierda,
        'limiteDerecha':   limiteDerecha,
        'existeLimite':    existeLimite,
        'valores':         {'izq': valoresIzquierda, 'der': valoresDerecha},
        'pasos':           pasos,
        'funcionEvaluar':  evaluar
    }


def analizarContinuidad(limites, puntoAnalisis, tipo):
    """
    Determina si la función es continua en el punto y justifica la discontinuidad.

    Parámetros:
        limites (dict): Resultado de calcularLimitesLaterales
        puntoAnalisis (int): Punto 'a' de análisis
        tipo (str): 'removible', 'salto' o 'infinita'

    Retorna:
        dict: {'esContinua': bool, 'tipoDiscontinuidad': str, 'justificacion': str, 'pasos': list[str]}
    """
    pasos = []
    pasos.append("=== ANÁLISIS DE CONTINUIDAD ===")
    pasos.append(f"Condición: lím(x→{puntoAnalisis}⁻) = lím(x→{puntoAnalisis}⁺) = f({puntoAnalisis})?")
    pasos.append("")

    valorEnPunto = limites['funcionEvaluar'](puntoAnalisis)
    textoValor = f"{valorEnPunto:.2f}" if valorEnPunto is not None else "Indefinido"
    pasos.append(f"Valor de la función en el punto: f({puntoAnalisis}) = {textoValor}")

    # La función NO es continua en ninguno de los tres tipos de discontinuidad
    esContinua = False

    if tipo == 'removible':
        justificacion = (
            f"El límite existe y vale {limites['limiteIzquierda']}, "
            f"pero f({puntoAnalisis}) no está definida (denominador cero). "
            f"Es una discontinuidad evitable/removible."
        )
    elif tipo == 'salto':
        justificacion = (
            f"Los límites laterales existen pero son distintos: "
            f"{limites['limiteIzquierda']} ≠ {limites['limiteDerecha']}. "
            f"Es una discontinuidad de salto."
        )
    elif tipo == 'infinita':
        justificacion = (
            f"La función crece sin límite cerca de x={puntoAnalisis} "
            f"(tiende a {limites['limiteIzquierda']} por la izquierda y "
            f"{limites['limiteDerecha']} por la derecha). "
            f"Es una discontinuidad asintótica infinita."
        )

    pasos.append(f"Justificación: {justificacion}")

    return {
        'esContinua':        esContinua,
        'tipoDiscontinuidad': tipo,
        'justificacion':     justificacion,
        'pasos':             pasos
    }


def analizarFuncionPorTramos(digitos):
    """
    Análisis completo de la función por tramos:
    1. Genera la función según los dígitos del RUT
    2. Calcula los límites laterales
    3. Analiza la continuidad en el punto

    Parámetros:
        digitos (list[int]): [d1, d2, ..., d8]

    Retorna:
        dict: {'funcion', 'limites', 'continuidad', 'pasos'}
    """
    pasos = []

    funcionData = generarFuncionPorTramos(digitos)
    pasos.extend(funcionData['pasos'])

    limitesData = calcularLimitesLaterales(
        funcionData['funcionFormula'],
        funcionData['puntoAnalisis'],
        funcionData['tipo'],
        funcionData['digitos']
    )
    pasos.extend(limitesData['pasos'])

    continuidadData = analizarContinuidad(
        limitesData,
        funcionData['puntoAnalisis'],
        funcionData['tipo']
    )
    pasos.extend(continuidadData['pasos'])

    return {
        'funcion':     funcionData,
        'limites':     limitesData,
        'continuidad': continuidadData,
        'pasos':       pasos
    }
