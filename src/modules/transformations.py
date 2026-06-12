# transformations.py - Transformación entre ecuación general y canónica
# ============================================================================
# TRANSFORMACIÓN GENERAL → CANÓNICA:
# 1. Completar cuadrados para x e y
# 2. Factorizar y simplificar
# 3. Identificar centro, vértices, focos, etc.
#
# TRANSFORMACIÓN INVERSA CANÓNICA → GENERAL:
# 1. Expandir la forma canónica
# 2. Reorganizar términos
# 3. Obtener coeficientes A, B, C, D, E

def transformarACanonica(coeficientes):
    """
    Transforma la ecuación general a forma canónica completando cuadrados.
    
    Parámetros:
        coeficientes (dict): {'A': float, 'B': float, 'C': float, 'D': float, 'E': float}
    
    Retorna:
        dict: {
            'tipo': str,
            'formaCanonica': str,
            'centro': (float, float) o None,
            'parametros': dict,  # Contiene a, b, c, etc. según la cónica
            'pasos': list[str]
        }
    
    La función debe mostrar todos los pasos algebraicos de completación de cuadrados.
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
    
    # Variables iniciales para los resultados
    tipoConica = "Desconocida"
    formaCanonica = ""
    centro = None
    parametros = {}
    
    if A != 0 and B != 0:
        # Caso 1: Elipse, Hipérbola o Circunferencia
        # Las coordenadas del centro (h, k) se obtienen de completar el cuadrado
        h = -C / (2 * A)
        k = -D / (2 * B)
        
        # Términos que necesitamos sumar a ambos lados para completar el cuadrado perfecto
        termXAdd = (C / (2 * A))**2
        termYAdd = (D / (2 * B))**2
        
        # F es el término independiente del lado derecho tras reordenar
        F = -E + A * termXAdd + B * termYAdd
        
        pasos.append("PASO 1: Agrupar y factorizar términos")
        pasos.append(f"{A}(x² + {C/A:.2f}x) + {B}(y² + {D/B:.2f}y) = {-E}")
        
        pasos.append("PASO 2: Completar cuadrados")
        pasos.append(f"{A}(x² + {C/A:.2f}x + {termXAdd:.2f}) + {B}(y² + {D/B:.2f}y + {termYAdd:.2f}) = {-E} + {A*termXAdd:.2f} + {B*termYAdd:.2f}")
        pasos.append(f"{A}(x - {h:.2f})² + {B}(y - {k:.2f})² = {F:.2f}")
        
        centro = (round(h, 2), round(k, 2))
        
        if F != 0:
            # Dividimos todo entre F para igualar la ecuación a 1 (forma canónica estándar)
            denomX = F / A
            denomY = F / B
            formaCanonica = f"(x - {h:.2f})² / {denomX:.2f} + (y - {k:.2f})² / {denomY:.2f} = 1"
            
            # Identificamos el tipo de cónica según los coeficientes
            if A == B:
                tipoConica = "Circunferencia"
                formaCanonica = f"(x - {h:.2f})² + (y - {k:.2f})² = {F/A:.2f}"
                parametros['r'] = (F/A)**0.5 if F/A > 0 else 0
            elif A * B > 0:
                tipoConica = "Elipse"
            else:
                tipoConica = "Hipérbola"
                
            parametros['a2'] = abs(denomX)
            parametros['b2'] = abs(denomY)
        else:
            formaCanonica = f"{A}(x - {h:.2f})² + {B}(y - {k:.2f})² = 0"
            tipoConica = "Cónica Degenerada (Punto)"
            
    elif A == 0 and B != 0 and C != 0:
        # Caso 2: Parábola horizontal (y al cuadrado)
        tipoConica = "Parábola"
        k = -D / (2 * B)
        termYAdd = (D / (2 * B))**2
        Ky = B * termYAdd - E
        h = Ky / C
        
        pasos.append("PASO 1: Agrupar variable al cuadrado")
        pasos.append(f"{B}(y² + {D/B:.2f}y) = {-C}x + {-E}")
        
        pasos.append("PASO 2: Completar cuadrados")
        pasos.append(f"{B}(y² + {D/B:.2f}y + {termYAdd:.2f}) = {-C}x - {E} + {B*termYAdd:.2f}")
        pasos.append(f"{B}(y - {k:.2f})² = {-C}(x - {h:.2f})")
        
        formaCanonica = f"(y - {k:.2f})² = {-C/B:.2f}(x - {h:.2f})"
        centro = (round(h, 2), round(k, 2))  # En realidad es el vértice
        parametros['p'] = (-C/B) / 4
        parametros['orientacion'] = 'horizontal'
        
    elif B == 0 and A != 0 and D != 0:
        # Caso 3: Parábola vertical (x al cuadrado)
        tipoConica = "Parábola"
        h = -C / (2 * A)
        termXAdd = (C / (2 * A))**2
        Kx = A * termXAdd - E
        k = Kx / D
        
        pasos.append("PASO 1: Agrupar variable al cuadrado")
        pasos.append(f"{A}(x² + {C/A:.2f}x) = {-D}y + {-E}")
        
        pasos.append("PASO 2: Completar cuadrados")
        pasos.append(f"{A}(x² + {C/A:.2f}x + {termXAdd:.2f}) = {-D}y - {E} + {A*termXAdd:.2f}")
        pasos.append(f"{A}(x - {h:.2f})² = {-D}(y - {k:.2f})")
        
        formaCanonica = f"(x - {h:.2f})² = {-D/A:.2f}(y - {k:.2f})"
        centro = (round(h, 2), round(k, 2))  # Vértice
        parametros['p'] = (-D/A) / 4
        parametros['orientacion'] = 'vertical'
    else:
        # Caso de fallback, cuando los coeficientes no permiten formar una cónica regular
        tipoConica = "Caso no soportado/Línea recta"
        formaCanonica = "No aplicable"
    
    pasos.append("")
    pasos.append(f"-> Ecuación Canónica Resultante: {formaCanonica}")
    if centro:
        pasos.append(f"-> Centro/Vértice: {centro}")
    
    return {
        'tipo': tipoConica,
        'formaCanonica': formaCanonica,
        'centro': centro,
        'parametros': parametros,
        'pasos': pasos
    }

def transformarAGeneral(tipoConica, formaCanonica, centro, parametros):
    """
    Transforma la ecuación canónica de vuelta a la forma general.
    Muestra paso a paso la expansión algebraica (requerido por el PDF).
    
    Parámetros:
        tipoConica (str): Tipo de cónica
        formaCanonica (str): Ecuación en forma canónica (para referencia)
        centro (tuple): (h, k)
        parametros (dict): Parámetros según el tipo de cónica
    
    Retorna:
        dict: {'ecuacionGeneral': str, 'coeficientes': dict, 'pasos': list[str]}
    """
    pasos = []
    pasos.append("=== TRANSFORMACIÓN CANÓNICA → GENERAL ===")
    pasos.append(f"Forma canónica: {formaCanonica}")
    pasos.append(f"Centro/Vértice: {centro}")
    pasos.append("")
    
    if centro is None:
        pasos.append("No se puede realizar la transformación inversa.")
        return {'ecuacionGeneral': "N/A", 'coeficientes': {}, 'pasos': pasos}
    
    h, k = centro
    
    if tipoConica in ("Circunferencia", "Elipse", "Hipérbola"):
        # Obtener denominadores
        a2 = parametros.get('a2', 1)
        b2 = parametros.get('b2', 1)
        
        if tipoConica == "Circunferencia":
            r = parametros.get('r', 0)
            r2 = r * r
            
            pasos.append("PASO 1: Partimos de la forma canónica")
            pasos.append(f"(x - {h:.2f})² + (y - {k:.2f})² = {r2:.2f}")
            pasos.append("")
            
            pasos.append("PASO 2: Expandir binomios")
            pasos.append(f"(x² - {2*h:.2f}x + {h*h:.2f}) + (y² - {2*k:.2f}y + {k*k:.2f}) = {r2:.2f}")
            pasos.append("")
            
            pasos.append("PASO 3: Reagrupar")
            E = h*h + k*k - r2
            pasos.append(f"x² + y² - {2*h:.2f}x - {2*k:.2f}y + {E:.2f} = 0")
            
            A, B = 1, 1
            C, D = -2*h, -2*k
        else:
            # Elipse o Hipérbola
            signo = "+" if tipoConica == "Elipse" else "-"
            
            pasos.append("PASO 1: Partimos de la forma canónica")
            pasos.append(f"(x - {h:.2f})²/{a2:.2f} {signo} (y - {k:.2f})²/{b2:.2f} = 1")
            pasos.append("")
            
            pasos.append("PASO 2: Multiplicar todo por los denominadores")
            if tipoConica == "Elipse":
                coefA = 1/a2
                coefB = 1/b2
            else:
                coefA = 1/a2
                coefB = -1/b2
            
            pasos.append(f"{coefA:.4f}(x - {h:.2f})² + {coefB:.4f}(y - {k:.2f})² = 1")
            pasos.append("")
            
            pasos.append("PASO 3: Expandir binomios")
            pasos.append(f"{coefA:.4f}(x² - {2*h:.2f}x + {h*h:.2f}) + {coefB:.4f}(y² - {2*k:.2f}y + {k*k:.2f}) = 1")
            pasos.append("")
            
            A = coefA
            B = coefB
            C = -2*h*coefA
            D = -2*k*coefB
            E = coefA*(h*h) + coefB*(k*k) - 1
            
            pasos.append("PASO 4: Reagrupar en forma general Ax² + By² + Cx + Dy + E = 0")
            pasos.append(f"{A:.4f}x² + {B:.4f}y² + ({C:.4f})x + ({D:.4f})y + ({E:.4f}) = 0")
    
    elif tipoConica == "Parábola":
        p = parametros.get('p', 0)
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
            C = -2*h
            D = -4*p
            E = h*h + 4*p*k
            
            pasos.append("PASO 3: Reagrupar")
            pasos.append(f"{A}x² + ({C:.2f})x + ({D:.2f})y + ({E:.2f}) = 0")
        else:
            pasos.append("PASO 1: Partimos de la forma canónica")
            pasos.append(f"(y - {k:.2f})² = {4*p:.2f}(x - {h:.2f})")
            pasos.append("")
            
            pasos.append("PASO 2: Expandir binomio izquierdo")
            pasos.append(f"y² - {2*k:.2f}y + {k*k:.2f} = {4*p:.2f}x - {4*p*h:.2f}")
            pasos.append("")
            
            A = 0
            B = 1
            C = -4*p
            D = -2*k
            E = k*k + 4*p*h
            
            pasos.append("PASO 3: Reagrupar")
            pasos.append(f"{B}y² + ({C:.2f})x + ({D:.2f})y + ({E:.2f}) = 0")
    else:
        A, B, C, D, E = 0, 0, 0, 0, 0
        pasos.append("Tipo de cónica no soportado para transformación inversa.")
    
    pasos.append("")
    pasos.append(f"→ Ecuación General recuperada: A={A:.4f}, B={B:.4f}, C={C:.4f}, D={D:.4f}, E={E:.4f}")
    
    return {
        'ecuacionGeneral': f"{A:.4f}x² + {B:.4f}y² + ({C:.4f})x + ({D:.4f})y + ({E:.4f}) = 0",
        'coeficientes': {'A': A, 'B': B, 'C': C, 'D': D, 'E': E},
        'pasos': pasos
    }

def calcularParametros(tipo, coeficientes, centro):
    """
    Calcula vértices, focos, ejes, etc. según el tipo de cónica.
    
    Retorna:
        dict: {
            'vertices': list,
            'focos': list,
            'excentricidad': float,
            'ejeTransverso': float o None,
            'ejeConjugado': float o None,
            'directriz': str o None,
            'pasos': list[str]
        }
    """
    # TODO: Implementar cálculos específicos según tipo de cónica
    pasos = []
    pasos.append(f"Calculando parámetros para {tipo}...")
    
    return {
        'vertices': [],
        'focos': [],
        'excentricidad': None,
        'pasos': pasos
    }
