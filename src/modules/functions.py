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
        'digitos': digitos,
        'pasos': pasos
    }

def calcularLimitesLaterales(funcion, puntoAnalisis, tipo, digitos):
    """
    Calcula límites laterales manualmente usando tabla de valores.
    """
    pasos = []
    valores = {'izq': {}, 'der': {}}
    d1, d2, d3, d4, d5, d6, d7, d8 = digitos
    
    pasos.append("=== CÁLCULO DE LÍMITES LATERALES ===")
    pasos.append(f"Punto de análisis: x → {puntoAnalisis}")
    pasos.append("")
    
    def evaluar(x):
        try:
            if tipo == 'removible':
                if x == d3: return None
                return (x - d3) * (x + d1) / (x - d3)
            elif tipo == 'salto':
                return x + d2 if x < d3 else x + d4
            elif tipo == 'infinita':
                if x == d3: return None
                return (d5 + 1) / (x - d3)
        except ZeroDivisionError:
            return None
            
    # Valores por la izquierda
    delta_izq = [-1, -0.1, -0.01, -0.001]
    for d in delta_izq:
        x_val = puntoAnalisis + d
        valores['izq'][x_val] = evaluar(x_val)
        
    # Valores por la derecha
    delta_der = [0.001, 0.01, 0.1, 1]
    for d in delta_der:
        x_val = puntoAnalisis + d
        valores['der'][x_val] = evaluar(x_val)
    
    pasos.append("Tabla de valores cercanos a x = {}:".format(puntoAnalisis))
    pasos.append(f"{'Izquierda (x)':<15} | {'f(x)':<15} || {'Derecha (x)':<15} | {'f(x)':<15}")
    pasos.append("-" * 68)
    
    for i in range(4):
        x_i = puntoAnalisis + delta_izq[3-i]  # De más lejano a más cercano
        f_i = valores['izq'][x_i]
        str_i = f"{f_i:.4f}" if f_i is not None else "Indefinido"
        
        x_d = puntoAnalisis + delta_der[i]    # De más cercano a más lejano
        f_d = valores['der'][x_d]
        str_d = f"{f_d:.4f}" if f_d is not None else "Indefinido"
        
        pasos.append(f"{x_i:<15.4f} | {str_i:<15} || {x_d:<15.4f} | {str_d:<15}")

    # Estimación de límites (tomando el valor más cercano)
    val_izq_cercano = valores['izq'][puntoAnalisis - 0.001]
    val_der_cercano = valores['der'][puntoAnalisis + 0.001]
    
    if tipo == 'infinita':
        limiteIzquierda = "-∞" if val_izq_cercano < 0 else "+∞"
        limiteDerecha = "-∞" if val_der_cercano < 0 else "+∞"
    else:
        limiteIzquierda = round(val_izq_cercano, 2)
        limiteDerecha = round(val_der_cercano, 2)
        
    existeLimite = (limiteIzquierda == limiteDerecha) and (tipo != 'infinita')
    
    pasos.append("")
    pasos.append(f"Límite por la izquierda: {limiteIzquierda}")
    pasos.append(f"Límite por la derecha: {limiteDerecha}")
    pasos.append(f"¿Existe el límite ordinario?: {'Sí' if existeLimite else 'No'}")
    
    return {
        'limiteIzquierda': limiteIzquierda,
        'limiteDerecha': limiteDerecha,
        'existeLimite': existeLimite,
        'valores': valores,
        'pasos': pasos,
        'f_eval': evaluar
    }

def analizarContinuidad(limites, puntoAnalisis, tipo):
    """
    Analiza si la función es continua en el punto y clasifica discontinuidad.
    """
    pasos = []
    
    pasos.append("=== ANÁLISIS DE CONTINUIDAD ===")
    pasos.append(f"Condición: lim(x→{puntoAnalisis}⁻) = lim(x→{puntoAnalisis}⁺) = f({puntoAnalisis})?")
    pasos.append("")
    
    f_eval = limites['f_eval']
    valor_en_punto = f_eval(puntoAnalisis)
    
    str_valor = f"{valor_en_punto:.2f}" if valor_en_punto is not None else "Indefinido"
    pasos.append(f"Valor de la función en el punto f({puntoAnalisis}): {str_valor}")
    
    esContinua = False
    justificacion = ""
    
    if tipo == 'removible':
        justificacion = f"El límite existe y vale {limites['limiteIzquierda']}, pero la función no está definida en x={puntoAnalisis} (denominador cero). Es una discontinuidad evitable/removible."
    elif tipo == 'salto':
        justificacion = f"Los límites laterales existen pero son diferentes ({limites['limiteIzquierda']} ≠ {limites['limiteDerecha']}). Es una discontinuidad de salto."
    elif tipo == 'infinita':
        justificacion = f"La función crece sin tope cerca de x={puntoAnalisis} (tendencia a {limites['limiteIzquierda']}/{limites['limiteDerecha']}). Es una discontinuidad asintótica infinita."
        
    pasos.append(f"Justificación: {justificacion}")
    
    return {
        'esContinua': esContinua,
        'tipoDiscontinuidad': tipo,
        'justificacion': justificacion,
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
        funcion_data['tipo'],
        funcion_data['digitos']
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
