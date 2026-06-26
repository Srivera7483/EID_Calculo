'''
conic.py - Construcción y clasificación de secciones cónicas
============================================================================
ECUACIÓN GENERAL DE CÓNICA: Ax² + By² + Cx + Dy + E = 0
Cálculo de coeficientes a partir de los dígitos del RUT:
  A = (d1 + d2) / v
  B = (d3 + d4) / v
  C = -(d5 + d6)
  D = -(d7 + d8)
  E = d1 + d3 + d5 + d7

 Ajustes para garantizar variedad de cónicas:
   - Si d8 impar:              B → -B              (genera hipérbolas)
   - Si d1 = d2:               B = A               (genera circunferencias)
   - Si (d5 + d6) múltiplo 3:  A = 0 o B = 0       (genera parábolas)
'''

def construirEcuacionGeneral(digitos, v):
    """
    Parámetros:
        digitos (list[int]): Lista [d1, d2, d3, d4, d5, d6, d7, d8]
        v (int): Variable auxiliar según el dígito verificador

    Retorna:
        dict: {'A', 'B', 'C', 'D', 'E': float, 'pasos': list[str]}
    """
    pasos = []
    d1, d2, d3, d4, d5, d6, d7, d8 = digitos

    pasos.append(f"Dígitos del RUT: {digitos}")
    pasos.append(f"Variable v: {v}")
    pasos.append("")
    pasos.append("=== PASO 1: Calcular coeficientes básicos ===")

    # Coeficientes iniciales según las fórmulas del enunciado
    A = (d1 + d2) / v
    B = (d3 + d4) / v
    C = -(d5 + d6)
    D = -(d7 + d8)
    E = d1 + d3 + d5 + d7

    pasos.append("Coeficientes sin ajustes:")
    pasos.append(f"  A = ({d1} + {d2}) / {v} = {A}")
    pasos.append(f"  B = ({d3} + {d4}) / {v} = {B}")
    pasos.append(f"  C = -({d5} + {d6}) = {C}")
    pasos.append(f"  D = -({d7} + {d8}) = {D}")
    pasos.append(f"  E = {d1} + {d3} + {d5} + {d7} = {E}")
    pasos.append("")
    pasos.append("=== PASO 2: Aplicar ajustes para garantizar variedad de cónicas ===")

    # Condiciones que determinan qué ajuste aplicar
    d8_es_impar = d8 % 2 != 0
    d1_igual_d2 = d1 == d2
    suma_d5_d6_multiplo_3 = (d5 + d6) % 3 == 0

    pasos.append(f"Verificar d8 impar: {d8} es {'impar' if d8_es_impar else 'par'}")
    pasos.append(f"Verificar d1 = d2: {d1} {'=' if d1_igual_d2 else '≠'} {d2}")
    pasos.append(f"Verificar (d5 + d6) múltiplo de 3: ({d5} + {d6}) = {d5 + d6} {'es' if suma_d5_d6_multiplo_3 else 'no es'} múltiplo de 3")

    # Aplicar ajustes en orden
    if d8_es_impar:
        B = -B
        pasos.append("-> Ajuste: d8 impar → B cambia de signo (genera Hipérbola)")

    if d1_igual_d2:
        B = A
        pasos.append("-> Ajuste: d1 = d2 → B = A (genera Circunferencia)")

    if suma_d5_d6_multiplo_3:
        if d7 % 2 == 0:
            B = 0
            pasos.append(f"-> Ajuste: (d5+d6) múltiplo de 3 y d7={d7} par → B = 0 (Parábola vertical)")
        else:
            A = 0
            pasos.append(f"-> Ajuste: (d5+d6) múltiplo de 3 y d7={d7} impar → A = 0 (Parábola horizontal)")

    pasos.append("")
    pasos.append("=== Ecuación General Final ===")
    pasos.append(f"A = {A}, B = {B}, C = {C}, D = {D}, E = {E}")

    return {'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'pasos': pasos}


def clasificarConica(coeficientes):
    """
    Clasifica la cónica según los valores de A y B.

    Parámetros:
        coeficientes (dict): {'A': float, 'B': float, ...}

    Retorna:
        dict: {'tipo': str, 'descripcion': str, 'pasos': list[str]}

    Criterios de clasificación:
        - A = B ≠ 0         → Circunferencia
        - A·B > 0, A ≠ B    → Elipse
        - A·B < 0            → Hipérbola
        - A = 0 o B = 0      → Parábola
    """
    pasos = []
    A = coeficientes['A']
    B = coeficientes['B']

    pasos.append(f"Coeficientes: A = {A}, B = {B}")
    pasos.append("")

    # Tolerancia para comparar flotantes de forma segura, le-9 es 0.000000001
    TOLERANCIA = 1e-9

    if abs(A - B) < TOLERANCIA and A != 0: # Entonces si A y B son casi iguales a 0, se considera que es una circunferencia
        tipo = "Circunferencia"
        descripcion = "A y B son iguales y distintos de cero"
    elif A * B > 0 and abs(A - B) >= TOLERANCIA: # Si poseen el mismo signo, y ladiferencia es mayor a la tolerancia y que son distintos.
        tipo = "Elipse"
        descripcion = "A y B tienen el mismo signo pero son distintos"
    elif A * B < 0: # Si poseen signos opuestos
        tipo = "Hipérbola"
        descripcion = "A y B tienen signos opuestos"
    elif (A == 0 and B != 0) or (A != 0 and B == 0): # Si exactamente uno de los coeficientes (A o B) es cero
        tipo = "Parábola"
        descripcion = "Exactamente uno de los coeficientes (A o B) es cero"
    else:
        tipo = "Desconocida/Degenerada"
        descripcion = "Los coeficientes no forman una cónica válida"

    pasos.append(f"Evaluación: {descripcion}")
    pasos.append(f"Resultado: {tipo}")

    return {'tipo': tipo, 'descripcion': descripcion, 'pasos': pasos}


def mostrarEcuacion(coeficientes):
    """
    Formatea la ecuación general como texto legible: "Ax² + By² + Cx + Dy + E = 0".
    Maneja correctamente coeficientes negativos en cualquier posición.

    Retorna:
        str: Ecuación formateada
    """
    A = coeficientes.get('A', 0)
    B = coeficientes.get('B', 0)
    C = coeficientes.get('C', 0)
    D = coeficientes.get('D', 0)
    E = coeficientes.get('E', 0)

    # Construir lista de términos no nulos como (valor, texto_sin_signo)
    terminos = []
    if A != 0: terminos.append((A, f"{abs(A)}x²")) # Va a imprimir solo si es distinto de 0.
    if B != 0: terminos.append((B, f"{abs(B)}y²"))
    if C != 0: terminos.append((C, f"{abs(C)}x"))
    if D != 0: terminos.append((D, f"{abs(D)}y"))
    if E != 0: terminos.append((E, f"{abs(E)}"))

    if not terminos:
        return "0 = 0"

    # El primer término lleva signo negativo solo si es negativo
    valorPrimero, textoPrimero = terminos[0]
    ecuacion = f"-{textoPrimero}" if valorPrimero < 0 else textoPrimero

    # Los términos siguientes llevan " + " o " - " según el signo
    for valor, texto in terminos[1:]:
        if valor < 0:
            ecuacion += f" - {texto}"
        else:
            ecuacion += f" + {texto}"

    ecuacion += " = 0"
    return ecuacion
