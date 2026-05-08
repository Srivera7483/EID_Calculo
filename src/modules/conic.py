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
    
    # TODO: Implementar cálculo de coeficientes básicos
    # A = (d1 + d2) / v
    # B = (d3 + d4) / v
    # C = -(d5 + d6)
    # D = -(d7 + d8)
    # E = d1 + d3 + d5 + d7
    
    pasos.append("Coeficientes sin ajustes:")
    pasos.append(f"  A = ({d1} + {d2}) / {v} = {d1 + d2} / {v}")
    pasos.append(f"  B = ({d3} + {d4}) / {v} = {d3 + d4} / {v}")
    pasos.append(f"  C = -({d5} + {d6}) = {-(d5 + d6)}")
    pasos.append(f"  D = -({d7} + {d8}) = {-(d7 + d8)}")
    pasos.append(f"  E = {d1} + {d3} + {d5} + {d7}")
    
    pasos.append("")
    pasos.append("=== PASO 2: Aplicar ajustes según reglas SII ===")
    
    # TODO: Aplicar ajustes
    # - Si d8 es impar: B → -B
    # - Si d1 = d2: B = A
    # - Si (d5 + d6) múltiplo de 3: aplicar regla de parábola
    
    pasos.append(f"Verificar d8 impar: {d8} es {'impar' if d8 % 2 != 0 else 'par'}")
    pasos.append(f"Verificar d1 = d2: {d1} {'=' if d1 == d2 else '≠'} {d2}")
    pasos.append(f"Verificar (d5 + d6) múltiplo de 3: ({d5} + {d6}) = {d5 + d6} {'es' if (d5 + d6) % 3 == 0 else 'no es'} múltiplo de 3")
    
    # Placeholder para coeficientes finales
    A = B = C = D = E = 0
    
    pasos.append("")
    pasos.append("=== Ecuación General Final ===")
    pasos.append(f"A = ?, B = ?, C = ?, D = ?, E = ?")
    
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
    
    # TODO: Implementar lógica de clasificación
    # Aplicar reglas de clasificación según A y B
    
    tipo = "Desconocida"
    descripcion = "Clasificación pendiente"
    
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
    # TODO: Implementar formateo de ecuación
    ecuacion = "Ax² + By² + Cx + Dy + E = 0"
    return ecuacion
