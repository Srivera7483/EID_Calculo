# rut_validator.py - Validación del RUT chileno usando algoritmo módulo 11

def validar_rut_con_pasos(rut):
    """
    Valida RUT y retorna pasos detallados para mostrar.

    Returns:
        dict: {'valido': bool, 'pasos': list[str]}
    """
    pasos = []
    pasos.append(f"RUT ingresado: {rut}")

    # Limpiar RUT
    rut_limpio = rut.replace(".", "").replace("-", "").replace(" ", "").upper()
    pasos.append(f"RUT limpio: {rut_limpio}")

    # Verificar formato
    if len(rut_limpio) != 9 or not rut_limpio[:-1].isdigit() or not (rut_limpio[-1].isdigit() or rut_limpio[-1] == 'K'):
        pasos.append("Formato inválido: debe tener 8 dígitos + DV (0-9 o K)")
        return {'valido': False, 'pasos': pasos}

    cuerpo = rut_limpio[:-1]
    dv_dado = rut_limpio[-1]
    pasos.append(f"Cuerpo: {cuerpo}, DV dado: {dv_dado}")

    # Multiplicadores
    multiplicadores = [2, 3, 4, 5, 6, 7, 2, 3]
    pasos.append(f"Multiplicadores (de derecha a izquierda): {multiplicadores}")

    # Cálculo suma
    suma = 0
    detalle = []
    for i in range(8):
        digito = int(cuerpo[7 - i])
        mult = multiplicadores[i]
        prod = digito * mult
        suma += prod
        detalle.append(f"{digito} * {mult} = {prod}")
    pasos.append(f"Productos: {' + '.join(detalle)} = {suma}")

    # Resto
    resto = suma % 11
    pasos.append(f"Suma % 11 = {resto}")

    # DV esperado
    if resto == 0:
        dv_esperado = '0'
    elif resto == 1:
        dv_esperado = 'K'
    else:
        dv_esperado = str(11 - resto)
    pasos.append(f"DV esperado: {dv_esperado}")

    valido = dv_dado == dv_esperado
    pasos.append(f"¿DV dado == DV esperado? {valido}")

    return {'valido': valido, 'pasos': pasos}

def extraer_digitos(rut):
    """
    Extrae los 8 dígitos del cuerpo del RUT.

    Args:
        rut (str): RUT válido.

    Returns:
        list[int]: Lista de 8 dígitos [d1, d2, d3, d4, d5, d6, d7, d8].

    Ejemplo: Para "12345678-9", retorna [1, 2, 3, 4, 5, 6, 7, 8]
    """
    # Limpiar RUT
    rut = rut.replace(".", "").replace("-", "").replace(" ", "").upper()
    cuerpo = rut[:-1]  # 8 dígitos
    return [int(d) for d in cuerpo]

def calcular_v(dv):
    """
    Calcula la variable auxiliar v según el dígito verificador.

    Args:
        dv (str): Dígito verificador ('0'-'9' o 'K').

    Returns:
        int: v = 10 si DV='K', 11 si DV='0', DV numérico si '1'-'9'.

    Ejemplo: 'K' → 10, '0' → 11, '5' → 5
    """
    if dv == 'K':
        return 10
    elif dv == '0':
        return 11
    else:
        return int(dv)