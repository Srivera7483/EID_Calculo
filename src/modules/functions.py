# functions.py - Análisis de funciones por tramos y límites
# ============================================================================
# FASE 6: Análisis de funciones generadas a partir del RUT
# Punto de análisis: a = d3
# Tipo según d8 mod 3:
# - d8 ≡ 0: Discontinuidad removible
# - d8 ≡ 1: Discontinuidad de salto
# - d8 ≡ 2: Discontinuidad infinita

def generarFuncionPorTramos(digitos):
    """
    Genera una función por tramos según el RUT y clasifica el tipo de discontinuidad.
    
    Parámetros:
        digitos (list[int]): Lista de 8 dígitos [d1, d2, d3, d4, d5, d6, d7, d8]
    
    Retorna:
        dict: {
            'funcionFormula': str,
            'puntoAnalisis': int,  # a = d3
            'tipo': str,           # 'removible', 'salto', 'infinita'
            'pasos': list[str]
        }
    """
    pasos = []
    d1, d2, d3, d4, d5, d6, d7, d8 = digitos
    
    pasos.append(f"Dígitos del RUT: {digitos}")
    pasos.append(f"Punto de análisis: a = d3 = {d3}")
    pasos.append("")
    
    # Determinar tipo según d8 mod 3
    residuo = d8 % 3
    
    pasos.append(f"d8 mod 3 = {d8} mod 3 = {residuo}")
    
    if residuo == 0:
        tipo = "removible"
        pasos.append("Tipo: DISCONTINUIDAD REMOVIBLE")
        pasos.append(f"f(x) = (x - {d3})(x + {d1}) / (x - {d3})")
        funcionFormula = f"(x - {d3})(x + {d1}) / (x - {d3})"
    elif residuo == 1:
        tipo = "salto"
        pasos.append("Tipo: DISCONTINUIDAD DE SALTO")
        pasos.append(f"f(x) = {{x + {d2}, si x < {d3}")
        pasos.append(f"       {{x + {d4}, si x ≥ {d3}")
        funcionFormula = f"(x + {d2}) si x < {d3}, (x + {d4}) si x ≥ {d3}"
    else:  # residuo == 2
        tipo = "infinita"
        pasos.append("Tipo: DISCONTINUIDAD INFINITA")
        pasos.append(f"f(x) = ({d5} + 1) / (x - {d3})")
        funcionFormula = f"({d5} + 1) / (x - {d3})"
    
    return {
        'funcionFormula': funcionFormula,
        'puntoAnalisis': d3,
        'tipo': tipo,
        'pasos': pasos
    }

def calcularLimitesLaterales(funcion, puntoAnalisis, tipo):
    """
    Calcula límites laterales manualmente usando tabla de valores.
    
    Parámetros:
        funcion (str): Fórmula de la función
        puntoAnalisis (int): Punto a donde se aproxima (a)
        tipo (str): 'removible', 'salto', 'infinita'
    
    Retorna:
        dict: {
            'limiteIzquierda': float o None,
            'limiteDerecha': float o None,
            'existeLimite': bool,
            'valores': dict,  # Tabla de valores cercanos
            'pasos': list[str]
        }
    """
    pasos = []
    valores = {}
    
    pasos.append("=== CÁLCULO DE LÍMITES LATERALES ===")
    pasos.append(f"Punto de análisis: x → {puntoAnalisis}")
    pasos.append("")
    
    # TODO: Implementar cálculo de tabla de valores
    # Por la izquierda: a-1, a-0.1, a-0.01, a-0.001
    # Por la derecha: a+0.001, a+0.01, a+0.1, a+1
    
    pasos.append("Tabla de valores cercanos a x = {}:".format(puntoAnalisis))
    pasos.append("Izquierda | f(x) | Derecha | f(x)")
    pasos.append("TODO: Calcular valores")
    
    # Placeholders
    limiteIzquierda = None
    limiteDerecha = None
    existeLimite = False
    
    return {
        'limiteIzquierda': limiteIzquierda,
        'limiteDerecha': limiteDerecha,
        'existeLimite': existeLimite,
        'valores': valores,
        'pasos': pasos
    }

def analizarContinuidad(limites, puntoAnalisis, tipo):
    """
    Analiza si la función es continua en el punto y clasifica discontinuidad.
    
    Retorna:
        dict: {
            'esContinua': bool,
            'tipoDiscontinuidad': str,  # 'removible', 'salto', 'infinita', 'ninguna'
            'justificacion': str,
            'pasos': list[str]
        }
    """
    pasos = []
    
    pasos.append("=== ANÁLISIS DE CONTINUIDAD ===")
    pasos.append(f"Condición: lim(x→{puntoAnalisis}⁻) = lim(x→{puntoAnalisis}⁺) = f({puntoAnalisis})?")
    pasos.append("")
    
    # TODO: Implementar análisis según límites
    
    return {
        'esContinua': False,
        'tipoDiscontinuidad': tipo,
        'justificacion': 'TODO',
        'pasos': pasos
    }

def analizarFuncionPorTramos(digitos):
    """
    Análisis completo: genera función, calcula límites, analiza continuidad.
    
    Retorna:
        dict: Resultado del análisis completo
    """
    pasos = []
    
    # Generar función
    funcion_data = generarFuncionPorTramos(digitos)
    pasos.extend(funcion_data['pasos'])
    
    # Calcular límites
    limites_data = calcularLimitesLaterales(
        funcion_data['funcionFormula'],
        funcion_data['puntoAnalisis'],
        funcion_data['tipo']
    )
    pasos.extend(limites_data['pasos'])
    
    # Analizar continuidad
    continuidad_data = analizarContinuidad(
        limites_data,
        funcion_data['puntoAnalisis'],
        funcion_data['tipo']
    )
    pasos.extend(continuidad_data['pasos'])
    
    return {
        'funcion': funcion_data,
        'limites': limites_data,
        'continuidad': continuidad_data,
        'pasos': pasos
    }
