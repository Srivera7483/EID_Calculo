# main.py - Punto de entrada del programa EID_Calculo
# Proyecto MAT1186: Análisis de secciones cónicas y funciones por tramos a partir del RUT

from modules.rut_validator import validar_rut_con_pasos, extraer_digitos, calcular_v
# from modules.conic import construir_ecuacion_general, clasificar_conica
# from modules.transformations import transformar_a_canonica
# from modules.plotter import graficar_conica
# from modules.functions import analizar_funcion_por_tramos
# from ui.interface import iniciar_interfaz

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
    resultado_validacion = validar_rut_con_pasos(rut)
    for paso in resultado_validacion['pasos']:
        print(paso)
    
    if not resultado_validacion['valido']:
        print("RUT inválido. Intente nuevamente.")
        return
    
    print("RUT válido.")
    
    # Paso 3: Extracción de dígitos y cálculo de v
    digitos = extraer_digitos(rut)
    rut_limpio = rut.replace(".", "").replace("-", "").replace(" ", "").upper()
    dv = rut_limpio[-1]
    v = calcular_v(dv)
    print(f"Dígitos extraídos: {digitos}")
    print(f"Dígito verificador: {dv}")
    print(f"Variable v: {v}")
    
    # Paso 4: Construcción de la ecuación general (pendiente)
    # ecuacion_general = construir_ecuacion_general(digitos)
    # print(f"Ecuación general: {ecuacion_general}")
    
    # Paso 5: Clasificación de la cónica (pendiente)
    # tipo_conica = clasificar_conica(ecuacion_general)
    # print(f"Tipo de cónica: {tipo_conica}")
    
    # Paso 6: Transformación a forma canónica (pendiente)
    # forma_canonica = transformar_a_canonica(ecuacion_general)
    # print(f"Forma canónica: {forma_canonica}")
    
    # Paso 7: Análisis de funciones por tramos (pendiente)
    # analisis_funciones = analizar_funcion_por_tramos(digitos)
    # print(f"Análisis de funciones: {analisis_funciones}")
    
    # Paso 8: Iniciar interfaz gráfica (pendiente)
    # iniciar_interfaz(ecuacion_general, forma_canonica, analisis_funciones)

if __name__ == "__main__":
    main()