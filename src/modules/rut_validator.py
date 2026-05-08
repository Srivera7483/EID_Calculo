# rutValidator.py - Validación del RUT chileno usando algoritmo módulo 11
# ============================================================================
# ALGORITMO MÓDULO 11 (Estándar SII Chile):
# 1. Multiplicar cada dígito del RUT (de derecha a izquierda) por [2,3,4,5,6,7,2,3]
# 2. Sumar todos los productos
# 3. Calcular resto de la suma dividido por 11
# 4. DV = 11 - resto (con excepciones: si resto=0 → DV=0, si resto=1 → DV=K)
# Esto detecta errores: si cambias un dígito, el DV no coincidirá.

def validarRutConPasos(rut):
    """
    Valida RUT chileno usando algoritmo módulo 11 y retorna pasos detallados.
    
    Parámetros:
        rut (str): RUT en formato "12345678-9" o "12345678K"

    Retorna:
        dict: {'valido': bool, 'pasos': list[str]} con pasos detallados del proceso
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

def extraerDigitos(rut):
    """
    Extrae los 8 dígitos del cuerpo del RUT (sin el DV).

    Parámetros:
        rut (str): RUT válido en cualquier formato (ej: "12345678-9", "12.345.678-9")

    Retorna:
        list[int]: Lista de 8 dígitos [d1, d2, d3, d4, d5, d6, d7, d8]

    Ejemplo: 
        entrada: "12345678-9"
        salida: [1, 2, 3, 4, 5, 6, 7, 8]
    """
    # Limpiar RUT: quitar puntos, guiones y espacios, convertir a mayúsculas
    rutLimpio = rut.replace(".", "").replace("-", "").replace(" ", "").upper()
    cuerpo = rutLimpio[:-1]  # Extraer los 8 primeros caracteres (ignorar DV)
    return [int(d) for d in cuerpo]

def calcularV(dv):
    """
    Calcula la variable auxiliar 'v' según el dígito verificador del RUT.
    
    Esta variable se usa para calcular los coeficientes de la ecuación cónica
    (A, B según contexto.md)

    Parámetros:
        dv (str): Dígito verificador ('0'-'9' o 'K')

    Retorna:
        int: v = 10 si DV='K', 11 si DV='0', valor numérico si DV='1'-'9'

    Ejemplo:
        'K' → 10
        '0' → 11
        '5' → 5
    """
    if dv == 'K':
        return 10  # Letra K mapea a 10
    elif dv == '0':
        return 11  # Dígito 0 mapea a 11
    else:
        return int(dv)  # Otros dígitos se usan directamente