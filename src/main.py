# main.py - Punto de entrada del programa EID_Calculo
# Proyecto MAT1186: Análisis de secciones cónicas y funciones por tramos a partir del RUT

from modules.rut_validator import validarRutConPasos, extraerDigitos, calcularV
# from modules.conic import construirEcuacionGeneral, clasificarConica
# from modules.transformations import transformarACanonica
# from modules.plotter import graficarConica
# from modules.functions import analizarFuncionPorTramos
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
    
    # Paso 4: Construcción de la ecuación general (pendiente)
    # ecuacionGeneral = construirEcuacionGeneral(digitos)
    # print(f"Ecuación general: {ecuacionGeneral}")
    
    # Paso 5: Clasificación de la cónica (pendiente)
    # tipoConica = clasificarConica(ecuacionGeneral)
    # print(f"Tipo de cónica: {tipoConica}")
    
    # Paso 6: Transformación a forma canónica (pendiente)
    # formaCanonica = transformarACanonica(ecuacionGeneral)
    # print(f"Forma canónica: {formaCanonica}")
    
    # Paso 7: Análisis de funciones por tramos (pendiente)
    # analisisFunciones = analizarFuncionPorTramos(digitos)
    # print(f"Análisis de funciones: {analisisFunciones}")
    
    # Paso 8: Iniciar interfaz gráfica (pendiente)
    # iniciarInterfaz(ecuacionGeneral, formaCanonica, analisisFunciones)

if __name__ == "__main__":
    main()