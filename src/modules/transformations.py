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
    
    # TODO: Implementar completación de cuadrados paso a paso
    # 1. Agrupar términos en x
    # 2. Agrupar términos en y
    # 3. Completar cuadrados
    # 4. Factorizar
    # 5. Identificar centro y parámetros
    
    pasos.append("PASO 1: Agrupar términos por variable")
    pasos.append(f"({A}x² + {C}x) + ({B}y² + {D}y) + {E} = 0")
    
    pasos.append("")
    pasos.append("PASO 2: Completar cuadrados (ver detalles algebraicos)")
    pasos.append("TODO: Mostrar factorización y completación")
    
    # Placeholders
    formaCanonica = "(x - h)²/a² ± (y - k)²/b² = 1"
    centro = (0, 0)
    parametros = {}
    
    return {
        'tipo': 'Desconocida',
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
