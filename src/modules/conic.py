# conic.py - Construcción y clasificación de secciones cónicas
# ============================================================================
# ECUACIÓN GENERAL DE CÓNICA: Ax² + By² + Cx + Dy + E = 0
# 
# Cálculo de coeficientes según dígitos del RUT:
# - A = (d1 + d2) / v
# - B = (d3 + d4) / v
# - C = -(d5 + d6)
# - D = -(d7 + d8)
# - E = d1 + d3 + d5 + d7
#
# Ajustes para variedad de cónicas:
# - Si d8 impar: B → -B (genera hipérbolas)
# - Si d1 = d2: B = A (genera circunferencias)
# - Si (d5 + d6) múltiplo de 3: A = 0 o B = 0 (genera parábolas)

def construirEcuacionGeneral(digitos, v):
    """
    Construye la ecuación general de la cónica a partir de los dígitos del RUT.
    
    Parámetros:
        digitos (list[int]): Lista de 8 dígitos [d1, d2, d3, d4, d5, d6, d7, d8]
        v (int): Variable auxiliar según dígito verificador (10, 11, o numérico 1-9)
    
    Retorna:
        dict: {'A': float, 'B': float, 'C': float, 'D': float, 'E': float, 'pasos': list[str]}
    
    Incluye pasos detallados de cada cálculo.
    """
    pasos = []
    pasos.append(f"Dígitos del RUT: {digitos}")
    pasos.append(f"Variable v: {v}")
    pasos.append("")
    pasos.append("=== PASO 1: Calcular coeficientes básicos ===")
    
    # Extractar dígitos
    d1, d2, d3, d4, d5, d6, d7, d8 = digitos
    
    # Calcular coeficientes básicos
    A_calc = (d1 + d2) / v
    B_calc = (d3 + d4) / v
    C_calc = -(d5 + d6)
    D_calc = -(d7 + d8)
    E_calc = d1 + d3 + d5 + d7
    
    pasos.append("Coeficientes sin ajustes:")
    pasos.append(f"  A = ({d1} + {d2}) / {v} = {A_calc}")
    pasos.append(f"  B = ({d3} + {d4}) / {v} = {B_calc}")
    pasos.append(f"  C = -({d5} + {d6}) = {C_calc}")
    pasos.append(f"  D = -({d7} + {d8}) = {D_calc}")
    pasos.append(f"  E = {d1} + {d3} + {d5} + {d7} = {E_calc}")
    
    pasos.append("")
    pasos.append("=== PASO 2: Aplicar ajustes según reglas SII ===")
    
    A = A_calc
    B = B_calc
    C = C_calc
    D = D_calc
    E = E_calc
    
    es_d8_impar = d8 % 2 != 0
    es_d1_igual_d2 = d1 == d2
    es_d5_d6_mult_3 = (d5 + d6) % 3 == 0
    
    pasos.append(f"Verificar d8 impar: {d8} es {'impar' if es_d8_impar else 'par'}")
    pasos.append(f"Verificar d1 = d2: {d1} {'=' if es_d1_igual_d2 else '≠'} {d2}")
    pasos.append(f"Verificar (d5 + d6) múltiplo de 3: ({d5} + {d6}) = {d5 + d6} {'es' if es_d5_d6_mult_3 else 'no es'} múltiplo de 3")
    
    # Aplicar ajustes en orden
    if es_d8_impar:
        B = -B
        pasos.append("-> Ajuste aplicado: d8 es impar, por lo tanto B cambia de signo (B = -B)")
        
    if es_d1_igual_d2:
        B = A
        pasos.append("-> Ajuste aplicado: d1 = d2, por lo tanto B = A (genera circunferencia)")
        
    if es_d5_d6_mult_3:
        A = 0
        pasos.append("-> Ajuste aplicado: (d5 + d6) es múltiplo de 3, por lo tanto A = 0 (genera parábola)")
    
    pasos.append("")
    pasos.append("=== Ecuación General Final ===")
    pasos.append(f"A = {A}, B = {B}, C = {C}, D = {D}, E = {E}")
    
    return {
        'A': A,
        'B': B,
        'C': C,
        'D': D,
        'E': E,
        'pasos': pasos
    }

def clasificarConica(coeficientes):
    """
    Clasifica la cónica según sus coeficientes.
    
    Parámetros:
        coeficientes (dict): {'A': float, 'B': float, 'C': float, 'D': float, 'E': float}
    
    Retorna:
        dict: {'tipo': str, 'descripcion': str, 'pasos': list[str]}
    
    Clasificación:
    - Circunferencia: A = B ≠ 0
    - Elipse: A y B mismo signo, A ≠ B
    - Hipérbola: A y B signos opuestos
    - Parábola: Exactamente A = 0 o B = 0 (pero no ambos)
    """
    pasos = []
    A = coeficientes['A']
    B = coeficientes['B']
    
    pasos.append(f"Coeficientes: A = {A}, B = {B}")
    pasos.append("")
    
    # Lógica de clasificación
    if A == B and A != 0:
        tipo = "Circunferencia"
        descripcion = "A y B son iguales y distintos de cero"
    elif A * B > 0 and A != B:
        tipo = "Elipse"
        descripcion = "A y B tienen el mismo signo pero son distintos"
    elif A * B < 0:
        tipo = "Hipérbola"
        descripcion = "A y B tienen signos opuestos"
    elif (A == 0 and B != 0) or (A != 0 and B == 0):
        tipo = "Parábola"
        descripcion = "Exactamente A o B es cero"
    else:
        tipo = "Desconocida/Degenerada"
        descripcion = "Los coeficientes no forman una cónica válida"
        
    pasos.append(f"Evaluación: {descripcion}")
    pasos.append(f"Resultado: {tipo}")
    
    return {
        'tipo': tipo,
        'descripcion': descripcion,
        'pasos': pasos
    }

def mostrarEcuacion(coeficientes):
    """
    Formatea la ecuación general para mostrarla de forma legible.
    
    Retorna:
        str: Ecuación formateada como "Ax² + By² + Cx + Dy + E = 0"
    """
    A = coeficientes.get('A', 0)
    B = coeficientes.get('B', 0)
    C = coeficientes.get('C', 0)
    D = coeficientes.get('D', 0)
    E = coeficientes.get('E', 0)
    
    terminos = []
    if A != 0: terminos.append(f"{A}x²")
    if B != 0: terminos.append(f"{B}y²")
    if C != 0: terminos.append(f"{C}x")
    if D != 0: terminos.append(f"{D}y")
    if E != 0: terminos.append(f"{E}")
    
    if not terminos:
        return "0 = 0"
        
    ecuacion = terminos[0]
    for termino in terminos[1:]:
        if termino.startswith("-"):
            ecuacion += f" - {termino[1:]}"
        else:
            ecuacion += f" + {termino}"
            
    ecuacion += " = 0"
    return ecuacion
