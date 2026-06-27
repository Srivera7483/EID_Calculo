# main.py - Punto de entrada del programa EID_Calculo
# Proyecto MAT1186: Análisis de secciones cónicas y funciones por tramos a partir del RUT

from modules.rut_validator import validarRutConPasos, extraerDigitos, calcularV
from modules.conic import construirEcuacionGeneral, clasificarConica, mostrarEcuacion
from modules.transformations import transformarACanonica, transformarAGeneral
from modules.functions import analizarFuncionPorTramos
from ui.interface import iniciarInterfaz

def main():
    """
    Flujo principal del programa:
    1. Ingreso y validación del RUT
    2. Construcción y análisis de la cónica
    3. Análisis de funciones por tramos
    4. Interfaz gráfica con visualización
    """
    print("=== EID_Calculo: Análisis de Secciones Cónicas y Funciones por Tramos ===")

    # Paso 1: Ingreso del RUT con reintento hasta 3 intentos
    intentos = 0
    resultadoValidacion = None
    while intentos < 3:
        rut = input("Ingrese un RUT chileno válido (formato: 12345678-9): ").strip()
        resultadoValidacion = validarRutConPasos(rut)
        for paso in resultadoValidacion['pasos']:
            print(paso)
        if resultadoValidacion['valido']:
            break
        intentos += 1
        restantes = 3 - intentos
        if restantes > 0:
            print(f"RUT inválido. Le quedan {restantes} intento(s).")
        else:
            print("Número máximo de intentos alcanzado. Cerrando programa.")
            return

    print("RUT válido.")

    try:
        # Paso 2: Extracción de dígitos y cálculo de v
        digitos = extraerDigitos(rut)
        rutLimpio = rut.replace(".", "").replace("-", "").replace(" ", "").upper()
        dv = rutLimpio[-1]
        v = calcularV(dv)
        print(f"Dígitos extraídos: {digitos}")
        print(f"Dígito verificador: {dv}")
        print(f"Variable v: {v}")

        print("\n" + "="*50)
        print("FASE 1: CONSTRUCCIÓN DE LA ECUACIÓN GENERAL")
        print("="*50)
        # Paso 3: Construcción de la ecuación general
        ecuacionGeneralData = construirEcuacionGeneral(digitos, v)
        for paso in ecuacionGeneralData['pasos']:
            print(paso)

        ecuacionTexto = mostrarEcuacion(ecuacionGeneralData)
        print(f"\n>> Ecuación formateada: {ecuacionTexto}")

        # Paso 4: Clasificación de la cónica
        print("\n--- Clasificación de la Cónica ---")
        tipoConicaData = clasificarConica(ecuacionGeneralData)
        for paso in tipoConicaData['pasos']:
            print(paso)

        # Paso 5: Transformación a forma canónica
        print("\n--- Transformación a Forma Canónica ---")
        formaCanonicaData = transformarACanonica(ecuacionGeneralData)
        for paso in formaCanonicaData['pasos']:
            print(paso)

        # Paso 5b: Transformación inversa (Canónica → General)
        print("\n--- Transformación Inversa: Canónica → General ---")
        inversa = transformarAGeneral(
            formaCanonicaData['tipo'],
            formaCanonicaData['formaCanonica'],
            formaCanonicaData['centro'],
            formaCanonicaData['parametros']
        )
        for paso in inversa['pasos']:
            print(paso)

        print("\n" + "="*50)
        print("FASE 6: ANÁLISIS DE FUNCIONES POR TRAMOS")
        print("="*50)
        # Paso 6: Análisis de funciones por tramos
        analisisFunciones = analizarFuncionPorTramos(digitos)
        for paso in analisisFunciones['pasos']:
            print(paso)

        # Paso 7: Iniciar interfaz gráfica
        iniciarInterfaz(resultadoValidacion, ecuacionTexto, formaCanonicaData, analisisFunciones)

    except ZeroDivisionError as e:
        print(f"\nError matemático: división por cero — {e}")
        print("Esto puede ocurrir si v=0 o si la cónica es degenerada. Verifique los dígitos del RUT.")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        print("El programa no pudo completar el análisis. Intente con otro RUT.")


if __name__ == "__main__":
    main()