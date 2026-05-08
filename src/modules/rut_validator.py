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
    rutLimpio = rut.replace(".", "").replace("-", "").replace(" ", "").upper()
    pasos.append(f"RUT limpio: {rutLimpio}")

    # Verificar formato básico del RUT limpio
    # Debe tener exactamente 9 caracteres: 8 dígitos + 1 DV
    longitudCorrecta = len(rutLimpio) == 9
    cuerpoEsDigitos = rutLimpio[:-1].isdigit()  # Primeros 8 son números
    dvEsValido = rutLimpio[-1].isdigit() or rutLimpio[-1] == 'K'  # Último es 0-9 o K

    if not (longitudCorrecta and cuerpoEsDigitos and dvEsValido):
        pasos.append("Formato inválido: debe tener 8 dígitos + DV (0-9 o K)")
        return {'valido': False, 'pasos': pasos}

    cuerpo = rutLimpio[:-1]
    dvDado = rutLimpio[-1]
    pasos.append(f"Cuerpo: {cuerpo}, DV dado: {dvDado}")

    # Multiplicadores
    multiplicadores = [2, 3, 4, 5, 6, 7, 2, 3]
    pasos.append(f"Multiplicadores (de derecha a izquierda): {multiplicadores}")

    # Cálculo de la suma de productos
    # Multiplicar cada dígito del cuerpo por su multiplicador correspondiente (de derecha a izquierda)
    suma = 0
    detalleProductos = []
    for i in range(8):
        digito = int(cuerpo[7 - i])  # Dígito desde la derecha (índice 7 a 0)
        multiplicador = multiplicadores[i]
        producto = digito * multiplicador
        suma += producto
        detalleProductos.append(f"{digito} * {multiplicador} = {producto}")
    
    pasos.append(f"Productos: {' + '.join(detalleProductos)} = {suma}")

    # Calcular resto de la suma dividido por 11
    resto = suma % 11
    pasos.append(f"Suma % 11 = {resto}")

    # Calcular DV esperado según el resto
    if resto == 0:
        dvEsperado = '0'  # Si resto 0, DV = 0
    elif resto == 1:
        dvEsperado = 'K'  # Si resto 1, DV = K
    else:
        dvEsperado = str(11 - resto)  # DV = 11 - resto
    
    pasos.append(f"DV esperado: {dvEsperado}")

    # Verificar si coincide
    valido = dvDado == dvEsperado
    pasos.append(f"¿DV dado ({dvDado}) == DV esperado ({dvEsperado})? {valido}")

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