# interface.py - Interfaz gráfica (UI/UX)
# ============================================================================

import tkinter as tk
from tkinter import ttk
from modules.plotter import Plotter

def iniciarInterfaz(resultadoValidacion, ecuacionTexto, formaCanonicaData, analisisFunciones):
    
    #Inicia la interfaz grafica principal.
    
    root = crearVentanaPrincipal()
    
    # Creamos un sistema de pestañas para mantener el diseño limpio y profesional
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Crear los frames para cada pestaña
    pestana_rut = ttk.Frame(notebook)
    pestana_conicas = ttk.Frame(notebook)
    pestana_funciones = ttk.Frame(notebook)
    
    notebook.add(pestana_rut, text="Cálculo de RUT")
    notebook.add(pestana_conicas, text="Forma Cónica")
    notebook.add(pestana_funciones, text="Límites")
    
    # ==========================================
    # PESTAÑA 0: RUT
    # ==========================================
    agregarSeccionValidacionRUT(pestana_rut, resultadoValidacion)
    
    # ==========================================
    # PESTAÑA 1: CONICAS
    # ==========================================
    frame_izq_conicas = ttk.Frame(pestana_conicas, width=400)
    frame_izq_conicas.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    
    agregarSeccionEcuacionGeneral(frame_izq_conicas, ecuacionTexto)
    ttk.Separator(frame_izq_conicas, orient='horizontal').pack(fill='x', pady=5)
    
    agregarSeccionFormaCanonica(frame_izq_conicas, formaCanonicaData['formaCanonica'])
    
    frame_der_conicas = ttk.Frame(pestana_conicas)
    frame_der_conicas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    agregarSeccionGrafica(frame_der_conicas, tipo_grafico="conica", data=formaCanonicaData)

    # ==========================================
    # PESTAÑA 2: FUNCIONES
    # ==========================================
    frame_izq_func = ttk.Frame(pestana_funciones, width=400)
    frame_izq_func.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    
    agregarSeccionFunciones(frame_izq_func, analisisFunciones)
    
    frame_der_func = ttk.Frame(pestana_funciones)
    frame_der_func.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    agregarSeccionGrafica(frame_der_func, tipo_grafico="funcion", data=analisisFunciones)

    # Iniciar el loop de la ventana
    root.mainloop()

def crearVentanaPrincipal():
    
    #Crea la ventana principal de la aplicacion.
    
    root = tk.Tk()
    root.title("EID_Calculo - Analisis de Conicas y Funciones ")
    root.geometry("1100x750")
    root.minsize(900, 600)
    return root

def agregarSeccionValidacionRUT(frame, resultadoValidacion):
    """Agrega seccion de validacion del RUT mostrando los pasos del cálculo."""
    ttk.Label(frame, text="Análisis y Validación de RUT (Módulo 11)", font=("Arial", 16, "bold")).pack(anchor=tk.N, pady=(20, 10))
    
    estado = "VÁLIDO" if resultadoValidacion.get('valido', False) else "INVÁLIDO"
    color = "green" if estado == "VÁLIDO" else "red"
    ttk.Label(frame, text=f"Resultado: {estado}", font=("Arial", 14, "bold"), foreground=color).pack(anchor=tk.N, pady=(0, 20))
    
    if 'detalles' not in resultadoValidacion:
        ttk.Label(frame, text="No hay detalles de validación disponibles.").pack()
        return
        
    detalles = resultadoValidacion['detalles']
    
    # Tabla Treeview para los multiplicadores
    columnas = ("Digito", "Multiplicador", "Producto")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=8)
    tabla.heading("Digito", text="Dígito del RUT")
    tabla.heading("Multiplicador", text="Multiplicador")
    tabla.heading("Producto", text="Producto")
    
    tabla.column("Digito", anchor=tk.CENTER, width=150)
    tabla.column("Multiplicador", anchor=tk.CENTER, width=150)
    tabla.column("Producto", anchor=tk.CENTER, width=150)
    
    tabla.pack(pady=10)
    
    for item in detalles['productos']:
        tabla.insert("", tk.END, values=(item['digito'], item['multiplicador'], item['producto']))
        
    # Desglose de fórmulas
    frame_formulas = ttk.Frame(frame)
    frame_formulas.pack(pady=20)
    
    fuente_formula = ("Arial", 12)
    
    ttk.Label(frame_formulas, text=f"1. Suma total de los productos = {detalles['suma']}", font=fuente_formula).pack(anchor=tk.W, pady=5)
    ttk.Label(frame_formulas, text=f"2. Resto de dividir la suma por 11 (Módulo 11) = {detalles['resto']}", font=fuente_formula).pack(anchor=tk.W, pady=5)
    ttk.Label(frame_formulas, text=f"3. Fórmula del Dígito Verificador (11 - Resto) = 11 - {detalles['resto']} = {detalles['dvEsperado']}", font=fuente_formula).pack(anchor=tk.W, pady=5)
    
    ttk.Separator(frame_formulas, orient='horizontal').pack(fill='x', pady=10)
    
    ttk.Label(frame_formulas, text=f"DV Calculado = {detalles['dvEsperado']}", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=2)
    ttk.Label(frame_formulas, text=f"DV Ingresado = {detalles['dvDado']}", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=2)

def agregarSeccionEcuacionGeneral(frame, ecuacionGeneral):
    
    #Agrega seccion con construccion paso a paso de ecuacion general.
    
    ttk.Label(frame, text="Construccion Ecuacion General", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(5, 5))
    # Muestra la ecuacion que viene del backend
    ttk.Label(frame, text=f"Resultado:\n{ecuacionGeneral}", justify=tk.LEFT).pack(anchor=tk.W)

def agregarSeccionFormaCanonica(frame, formaCanonica):
    
    #Agrega seccion con forma canonica y campos vacios para completar en la defensa.
    
    ttk.Label(frame, text="Forma Canonica y Clasificacion", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(5, 5))
    ttk.Label(frame, text=f"Ecuacion:\n{formaCanonica}", justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 10))
    
    ttk.Label(frame, text="Campos de Defensa Oral:", font=("Arial", 10, "italic")).pack(anchor=tk.W, pady=5)
    
    # Campos vacios
    campos = ["Centro", "Vertices", "Focos", "Eje mayor / transverso", "Eje menor / conjugado", "Directriz"]
    
    for campo in campos:
        row = ttk.Frame(frame)
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text=f"{campo}:", width=22).pack(side=tk.LEFT)
        ttk.Entry(row).pack(side=tk.RIGHT, expand=True, fill=tk.X)

def agregarSeccionGrafica(frame, tipo_grafico, data):
    
    #Agrega seccion con grafica de la conica o funcion usando la clase Plotter.
    
    titulo = "Grafica de la Conica" if tipo_grafico == "conica" else "Grafica de la Funcion"
    ttk.Label(frame, text=titulo, font=("Arial", 12, "bold")).pack(pady=(0, 10))
    
    # Crear el Canvas nativo para el Plotter
    canvas = tk.Canvas(frame, bg="white", highlightthickness=1, highlightbackground="gray")
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Para que el plotter se adapte, necesitamos esperar a que el canvas se dibuje
    frame.update_idletasks() 
    width = canvas.winfo_width() if canvas.winfo_width() > 10 else 600
    height = canvas.winfo_height() if canvas.winfo_height() > 10 else 500

    # Instanciar el Plotter manual
    graficador = Plotter(canvas, width=width, height=height)
    graficador.dibujar_ejes()
    
    # Dibujar gráfica real
    if tipo_grafico == "conica" and data:
        tipo = data.get('tipo', '')
        centro = data.get('centro')
        params = data.get('parametros', {})
        
        if centro:
            h, k = centro
            if tipo == 'Circunferencia':
                graficador.dibujar_circunferencia(h, k, params.get('r', 0))
            elif tipo == 'Elipse':
                graficador.dibujar_elipse(h, k, params.get('a2', 0)**0.5, params.get('b2', 0)**0.5)
            elif tipo == 'Hipérbola':
                graficador.dibujar_hiperbola(h, k, params.get('a2', 0)**0.5, params.get('b2', 0)**0.5)
            elif tipo == 'Parábola':
                p = params.get('p', 0)
                if params.get('orientacion') == 'horizontal':
                    graficador.dibujar_parabola_horizontal(h, k, p)
                else:
                    graficador.dibujar_parabola_vertical(h, k, p)
                    
    elif tipo_grafico == "funcion" and data:
        f_eval = data['limites']['f_eval']
        punto = data['funcion']['puntoAnalisis']
        
        # Dibujar función
        graficador.dibujar_funcion(f_eval)
        
        # Dibujar asíntota si es discontinuidad infinita
        if data['funcion']['tipo'] == 'infinita':
            graficador.dibujar_asintota_vertical(punto)
        
    graficador.actualizar()

def agregarSeccionFunciones(frame, analisisFunciones):
    """
    Agrega sección con análisis de funciones por tramos.
    """
    ttk.Label(frame, text="Análisis de Funciones", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
    ttk.Label(frame, text=f"Caso generado:\n{analisisFunciones['funcion']['funcionFormula']}", justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 10))
    
    ttk.Label(frame, text="Campos de Defensa Oral:", font=("Arial", 10, "italic")).pack(anchor=tk.W, pady=5)
    
    # Campos vacíos exigidos por la rúbrica (Fase 6)
    campos = [
        "Límite por la izquierda", 
        "Límite por la derecha", 
        "¿Existe el límite?", 
        "Valor f(a)", 
        "¿Es continua?", 
        "Tipo de discontinuidad", 
        "Justificación"
    ]
    
    for campo in campos:
        row = ttk.Frame(frame)
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text=f"{campo}:", width=22).pack(side=tk.LEFT)
        ttk.Entry(row).pack(side=tk.RIGHT, expand=True, fill=tk.X)
