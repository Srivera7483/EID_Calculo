# main.py - Punto de entrada del programa EID_Calculo
# Proyecto MAT1186: Análisis de secciones cónicas y funciones por tramos a partir del RUT

from modules.rut_validator import validarRutConPasos, extraerDigitos, calcularV
from modules.conic import construirEcuacionGeneral, clasificarConica, mostrarEcuacion
# from modules.transformations import transformarACanonica
# from modules.plotter import graficarConica
from modules.functions import analizarFuncionPorTramos
# from ui.interface import iniciarInterfaz

def main():
    """
    Flujo principal del programa:
    1. Ingreso y validación del RUT
    2. Construcción y análisis de la cónica
    3. Análisis de funciones por tramos
    4. Interfaz gráfica con visualización
    """
    print("=== EID_Calculo: Análisis de Secciones Cónicas y Funciones por Tramos ===")
    
    # Paso 1: Ingreso del RUT
    rut = input("Ingrese un RUT chileno válido (formato: 12345678-9): ").strip()
    
    # Paso 2: Validación del RUT con pasos
    resultadoValidacion = validarRutConPasos(rut)
    for paso in resultadoValidacion['pasos']:
        print(paso)
    
    if not resultadoValidacion['valido']:
        print("RUT inválido. Intente nuevamente.")
        return
    
    print("RUT válido.")
    
    # Paso 3: Extracción de dígitos y cálculo de v
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
    # Paso 4: Construcción de la ecuación general
    ecuacionGeneralData = construirEcuacionGeneral(digitos, v)
    for paso in ecuacionGeneralData['pasos']:
        print(paso)
        
    ecuacionTexto = mostrarEcuacion(ecuacionGeneralData)
    print(f"\n>> Ecuación formateada: {ecuacionTexto}")
    
    # Paso 5: Clasificación de la cónica
    print("\n--- Clasificación de la Cónica ---")
    tipoConicaData = clasificarConica(ecuacionGeneralData)
    for paso in tipoConicaData['pasos']:
        print(paso)
    
    # Paso 6: Transformación a forma canónica (pendiente)
    # formaCanonica = transformarACanonica(ecuacionGeneralData)
    # print(f"Forma canónica: {formaCanonica}")
    
    print("\n" + "="*50)
    print("FASE 6: ANÁLISIS DE FUNCIONES POR TRAMOS")
    print("="*50)
    # Paso 7: Análisis de funciones por tramos
    analisisFunciones = analizarFuncionPorTramos(digitos)
    for paso in analisisFunciones['pasos']:
        print(paso)
    
    # Paso 8: Iniciar interfaz gráfica (pendiente)
    # iniciarInterfaz(ecuacionGeneralData, None, analisisFunciones)

if __name__ == "__main__":
    main()