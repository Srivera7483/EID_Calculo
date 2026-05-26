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
    
    tipo_conica = "Desconocida"
    formaCanonica = ""
    centro = None
    parametros = {}
    
    if A != 0 and B != 0:
        # Elipse, Hipérbola, Circunferencia
        h = -C / (2 * A)
        k = -D / (2 * B)
        
        term_x_add = (C / (2 * A))**2
        term_y_add = (D / (2 * B))**2
        
        F = -E + A * term_x_add + B * term_y_add
        
        pasos.append("PASO 1: Agrupar y factorizar términos")
        pasos.append(f"{A}(x² + {C/A:.2f}x) + {B}(y² + {D/B:.2f}y) = {-E}")
        
        pasos.append("PASO 2: Completar cuadrados")
        pasos.append(f"{A}(x² + {C/A:.2f}x + {term_x_add:.2f}) + {B}(y² + {D/B:.2f}y + {term_y_add:.2f}) = {-E} + {A*term_x_add:.2f} + {B*term_y_add:.2f}")
        pasos.append(f"{A}(x - {h:.2f})² + {B}(y - {k:.2f})² = {F:.2f}")
        
        centro = (round(h, 2), round(k, 2))
        
        if F != 0:
            denom_x = F / A
            denom_y = F / B
            formaCanonica = f"(x - {h:.2f})² / {denom_x:.2f} + (y - {k:.2f})² / {denom_y:.2f} = 1"
            
            if A == B:
                tipo_conica = "Circunferencia"
                formaCanonica = f"(x - {h:.2f})² + (y - {k:.2f})² = {F/A:.2f}"
                parametros['r'] = (F/A)**0.5 if F/A > 0 else 0
            elif A * B > 0:
                tipo_conica = "Elipse"
            else:
                tipo_conica = "Hipérbola"
                
            parametros['a2'] = abs(denom_x)
            parametros['b2'] = abs(denom_y)
        else:
            formaCanonica = f"{A}(x - {h:.2f})² + {B}(y - {k:.2f})² = 0"
            tipo_conica = "Cónica Degenerada (Punto)"
            
    elif A == 0 and B != 0 and C != 0:
        # Parábola horizontal
        tipo_conica = "Parábola"
        k = -D / (2 * B)
        term_y_add = (D / (2 * B))**2
        Ky = B * term_y_add - E
        h = Ky / C
        
        pasos.append("PASO 1: Agrupar variable al cuadrado")
        pasos.append(f"{B}(y² + {D/B:.2f}y) = {-C}x + {-E}")
        
        pasos.append("PASO 2: Completar cuadrados")
        pasos.append(f"{B}(y² + {D/B:.2f}y + {term_y_add:.2f}) = {-C}x - {E} + {B*term_y_add:.2f}")
        pasos.append(f"{B}(y - {k:.2f})² = {-C}(x - {h:.2f})")
        
        formaCanonica = f"(y - {k:.2f})² = {-C/B:.2f}(x - {h:.2f})"
        centro = (round(h, 2), round(k, 2))  # En realidad es el vértice
        parametros['p'] = (-C/B) / 4
        
    elif B == 0 and A != 0 and D != 0:
        # Parábola vertical
        tipo_conica = "Parábola"
        h = -C / (2 * A)
        term_x_add = (C / (2 * A))**2
        Kx = A * term_x_add - E
        k = Kx / D
        
        pasos.append("PASO 1: Agrupar variable al cuadrado")
        pasos.append(f"{A}(x² + {C/A:.2f}x) = {-D}y + {-E}")
        
        pasos.append("PASO 2: Completar cuadrados")
        pasos.append(f"{A}(x² + {C/A:.2f}x + {term_x_add:.2f}) = {-D}y - {E} + {A*term_x_add:.2f}")
        pasos.append(f"{A}(x - {h:.2f})² = {-D}(y - {k:.2f})")
        
        formaCanonica = f"(x - {h:.2f})² = {-D/A:.2f}(y - {k:.2f})"
        centro = (round(h, 2), round(k, 2))  # Vértice
        parametros['p'] = (-D/A) / 4
    else:
        tipo_conica = "Caso no soportado/Línea recta"
        formaCanonica = "No aplicable"
    
    pasos.append("")
    pasos.append(f"-> Ecuación Canónica Resultante: {formaCanonica}")
    if centro:
        pasos.append(f"-> Centro/Vértice: {centro}")
    
    return {
        'tipo': tipo_conica,
        'formaCanonica': formaCanonica,
        'centro': centro,
        'parametros': parametros,
        'pasos': pasos
    }

def transformarAGeneral(formaCanonica, centro, parametros):
    """
    Transforma la ecuación canónica de vuelta a forma general.
    
    Parámetros:
        formaCanonica (str): Ecuación en forma canónica
        centro (tuple): (h, k)
        parametros (dict): Parámetros según el tipo de cónica
    
    Retorna:
        dict: {
            'ecuacionGeneral': str,
            'coeficientes': {'A': float, 'B': float, 'C': float, 'D': float, 'E': float},
            'pasos': list[str]
        }
    """
    pasos = []
    
    pasos.append("=== TRANSFORMACIÓN CANÓNICA → GENERAL ===")
    pasos.append(f"Forma canónica: {formaCanonica}")
    pasos.append(f"Centro: {centro}")
    
    # TODO: Implementar expansión paso a paso
    # 1. Expandir binomios
    # 2. Distribuir términos
    # 3. Reagrupar en forma general
    
    pasos.append("")
    pasos.append("PASO 1: Expandir binomios")
    pasos.append("TODO: Mostrar expansión algebraica")
    
    # Placeholders
    ecuacionGeneral = "Ax² + By² + Cx + Dy + E = 0"
    coeficientes = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}
    
    return {
        'ecuacionGeneral': ecuacionGeneral,
        'coeficientes': coeficientes,
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
