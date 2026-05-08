# interface.py - Interfaz gráfica (UI/UX)
# ============================================================================
# Interfaz usando Tkinter (built-in) o Web framework (Flask/Django)
# 
# Requisitos:
# - Campos vacíos inicialmente para completar en defensa
# - Mostrar cónica graficada
# - Mostrar análisis de funciones
# - Diseño intuitivo y profesional

import tkinter as tk
from tkinter import ttk

def iniciarInterfaz(ecuacionGeneral, formaCanonica, analisisFunciones):
    """
    Inicia la interfaz gráfica principal.
    
    Parámetros:
        ecuacionGeneral (dict): Ecuación general con pasos
        formaCanonica (dict): Forma canónica con pasos
        analisisFunciones (dict): Análisis de funciones por tramos
    """
    # TODO: Implementar interfaz con Tkinter o Web
    # 1. Crear ventana principal
    # 2. Secciones para:
    #    - Validación de RUT (solo lectura)
    #    - Construcción de ecuación general
    #    - Clasificación de cónica
    #    - Forma canónica
    #    - Gráfica (Matplotlib)
    #    - Análisis de funciones
    # 3. Campos vacíos para llenar en defensa:
    #    - Centro
    #    - Vértices
    #    - Focos
    #    - Ejes (mayor, menor, transverso, conjugado)
    #    - Directriz
    #    - Límites laterales
    #    - Tipo de discontinuidad
    
    print("Interfaz gráfica pendiente de implementación")
    print(f"Ecuación general: {ecuacionGeneral}")
    print(f"Forma canónica: {formaCanonica}")
    print(f"Análisis funciones: {analisisFunciones}")

def crearVentanaPrincipal():
    """
    Crea la ventana principal de la aplicación.
    """
    # TODO: Crear interfaz
    pass

def agregarSeccionValidacionRUT(frame):
    """
    Agrega sección de validación del RUT (solo lectura).
    """
    # TODO: Crear widgets
    pass

def agregarSeccionEcuacionGeneral(frame):
    """
    Agrega sección con construcción paso a paso de ecuación general.
    """
    # TODO: Crear widgets con pasos
    pass

def agregarSeccionFormaCanonica(frame):
    """
    Agrega sección con forma canónica y campos vacíos para completar en defensa.
    """
    # TODO: Crear widgets
    # - Centro (vacío)
    # - Vértices (vacío)
    # - Focos (vacío)
    # - Ejes (vacíos)
    # - Directriz (vacío)
    pass

def agregarSeccionGrafica(frame):
    """
    Agrega sección con gráfica de la cónica (Matplotlib embedded).
    """
    # TODO: Embeber Matplotlib en Tkinter
    pass

def agregarSeccionFunciones(frame):
    """
    Agrega sección con análisis de funciones por tramos.
    """
    # TODO: Crear widgets
    # - Fórmula de función
    # - Tabla de valores
    # - Gráfica de función
    # - Campos vacíos:
    #   - Límite izquierda (vacío)
    #   - Límite derecha (vacío)
    #   - Existe límite? (vacío)
    #   - Tipo de discontinuidad (vacío)
    #   - Justificación (vacío)
    pass
