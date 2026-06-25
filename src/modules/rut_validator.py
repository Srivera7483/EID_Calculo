def validarRutConPasos(rut):
    """
    Valida un RUT chileno usando el algoritmo módulo 11.
    """
    pasos = []
    pasos.append(f"RUT ingresado: {rut}")

    # Eliminar puntos, guiones y espacios; convertir a mayúsculas
    rutLimpio = rut.replace(".", "").replace("-", "").replace(" ", "").upper()
    pasos.append(f"RUT limpio (sin formato): {rutLimpio}")

    # Verificar formato: 8 dígitos + 1 dígito verificador (0-9 o K)
    formatoValido = (
        len(rutLimpio) == 9
        and rutLimpio[:-1].isdigit()
        and (rutLimpio[-1].isdigit() or rutLimpio[-1] == 'K')
    )

    if not formatoValido:
        pasos.append("Formato inválido: debe tener 8 dígitos + DV (0-9 o K)")
        return {'valido': False, 'pasos': pasos}

    cuerpo = rutLimpio[:-1]   # Los 8 dígitos del RUT
    dvIngresado = rutLimpio[-1]
    pasos.append(f"Cuerpo: {cuerpo}  |  DV ingresado: {dvIngresado}")

    # Multiplicadores del algoritmo módulo 11 (se aplican de derecha a izquierda)
    multiplicadores = [2, 3, 4, 5, 6, 7, 2, 3]
    pasos.append(f"Multiplicadores (de derecha a izquierda): {multiplicadores}")

    # Calcular la suma de cada dígito multiplicado por su factor
    sumaTotal = 0
    detalleProductos = []
    for posicion in range(8):
        digitoActual = int(cuerpo[7 - posicion])   # Recorre de derecha a izquierda
        factor = multiplicadores[posicion]
        producto = digitoActual * factor
        sumaTotal += producto
        detalleProductos.append(f"{digitoActual} × {factor} = {producto}")

    pasos.append(f"Productos: {' + '.join(detalleProductos)} = {sumaTotal}")

    # Calcular el resto y determinar el DV esperado
    resto = sumaTotal % 11
    pasos.append(f"Suma mod 11 = {sumaTotal} mod 11 = {resto}")

    if resto == 0:
        dvEsperado = '0'
    elif resto == 1:
        dvEsperado = 'K'
    else:
        dvEsperado = str(11 - resto)

    pasos.append(f"DV esperado: {dvEsperado}")

    # Comparar el DV ingresado con el esperado
    esValido = dvIngresado == dvEsperado
    resultado = "VÁLIDO" if esValido else "INVÁLIDO"
    pasos.append(f"Comparación: DV ingresado ({dvIngresado}) == DV esperado ({dvEsperado})? → {resultado}")

    detalles = {
        'cuerpo': cuerpo,
        'dvDado': dvIngresado,
        'dvEsperado': dvEsperado,
        'multiplicadores': multiplicadores,
        'suma': sumaTotal,
        'resto': resto,
        'productos': [
            {
                'digito': int(cuerpo[7 - i]),
                'multiplicador': multiplicadores[i],
                'producto': int(cuerpo[7 - i]) * multiplicadores[i]
            }
            for i in range(8)
        ]
    }

    return {'valido': esValido, 'pasos': pasos, 'detalles': detalles}


def extraerDigitos(rut):
    
    rutLimpio = rut.replace(".", "").replace("-", "").replace(" ", "").upper()
    cuerpo = rutLimpio[:-1]   # Ignorar el último carácter (DV)
    return [int(digito) for digito in cuerpo]


def calcularV(dv):
    """
    Calcula la variable auxiliar 'v' a partir del dígito verificador.
    Esta variable se usa para calcular los coeficientes de la ecuación cónica.

    Parámetros:
        dv (str): Dígito verificador ('0'-'9' o 'K')

    Retorna:
        int: 10 si DV='K', 11 si DV='0', el valor numérico en cualquier otro caso

    Ejemplos:
        'K' → 10,  '0' → 11,  '5' → 5
    """
    if dv == 'K':
        return 10
    elif dv == '0':
        return 11
    else:
        return int(dv)