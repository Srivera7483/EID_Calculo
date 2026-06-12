# interface.py - Interfaz gráfica con tres pestañas
# Pestaña 1: Cálculo de RUT (Módulo 11)
# Pestaña 2: Forma Cónica (ecuación, gráfica, campos de defensa)
# Pestaña 3: Límites (función por tramos, tabla de valores, gráfica)

import tkinter as tk
from tkinter import ttk
from modules.plotter import Graficador


def iniciarInterfaz(resultadoValidacion, ecuacionTexto, datosConica, analisisFunciones):
    """Inicia la ventana principal con tres pestañas."""
    ventana = tk.Tk()
    ventana.title("EID_Calculo – Cónicas y Funciones por Tramos")
    ventana.geometry("1200x800")
    ventana.minsize(1000, 650)

    pestanas = ttk.Notebook(ventana)
    pestanas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    pestanaRut = ttk.Frame(pestanas)
    pestanaConica = ttk.Frame(pestanas)
    pestanaLimites = ttk.Frame(pestanas)
    pestanas.add(pestanaRut, text="  Cálculo de RUT  ")
    pestanas.add(pestanaConica, text="  Forma Cónica  ")
    pestanas.add(pestanaLimites, text="  Límites  ")

    construirPestanaRut(pestanaRut, resultadoValidacion)
    construirPestanaConica(pestanaConica, ecuacionTexto, datosConica)
    construirPestanaLimites(pestanaLimites, analisisFunciones)

    ventana.mainloop()


# ==========================================
# PESTAÑA 1: CÁLCULO DE RUT
# ==========================================

def construirPestanaRut(contenedor, resultado):
    """Muestra el algoritmo Módulo 11 paso a paso."""
    ttk.Label(contenedor, text="Validación de RUT – Algoritmo Módulo 11",
              font=("Arial", 16, "bold")).pack(pady=(20, 5))

    esValido = resultado.get("valido", False)
    colorEstado = "green" if esValido else "red"
    textoEstado = "✓ RUT VÁLIDO" if esValido else "✗ RUT INVÁLIDO"
    ttk.Label(contenedor, text=textoEstado, font=("Arial", 14, "bold"),
              foreground=colorEstado).pack(pady=(0, 15))

    if "detalles" not in resultado:
        return

    detalles = resultado["detalles"]

    # Información del RUT
    seccionInfo = ttk.LabelFrame(contenedor, text="Datos del RUT", padding=10)
    seccionInfo.pack(fill=tk.X, padx=20, pady=(0, 10))
    ttk.Label(seccionInfo,
              text=f"Cuerpo: {detalles['cuerpo']}    |    DV ingresado: {detalles['dvDado']}",
              font=("Arial", 11)).pack(anchor=tk.W)

    # Tabla de multiplicaciones
    seccionTabla = ttk.LabelFrame(contenedor, text="Tabla de Multiplicaciones (derecha → izquierda)", padding=10)
    seccionTabla.pack(fill=tk.X, padx=20, pady=(0, 10))

    columnas = ("Posición", "Dígito", "Multiplicador", "Producto")
    tabla = ttk.Treeview(seccionTabla, columns=columnas, show="headings", height=8)
    for columna in columnas:
        tabla.heading(columna, text=columna)
        tabla.column(columna, anchor=tk.CENTER, width=120)
    tabla.pack(fill=tk.X)

    for indice, item in enumerate(detalles["productos"]):
        tabla.insert("", tk.END, values=(indice + 1, item["digito"], item["multiplicador"], item["producto"]))

    # Desarrollo del cálculo
    seccionCalculo = ttk.LabelFrame(contenedor, text="Desarrollo del Cálculo", padding=10)
    seccionCalculo.pack(fill=tk.X, padx=20, pady=(0, 10))

    sumaProductos = " + ".join(str(p["producto"]) for p in detalles["productos"])
    lineasCalculo = [
        f"Suma de productos:  {sumaProductos}  =  {detalles['suma']}",
        f"Resto (Suma mod 11):  {detalles['suma']} mod 11  =  {detalles['resto']}",
        f"DV esperado (11 − Resto):  11 − {detalles['resto']}  =  {detalles['dvEsperado']}",
    ]
    for linea in lineasCalculo:
        ttk.Label(seccionCalculo, text=linea, font=("Arial", 11)).pack(anchor=tk.W, pady=2)

    ttk.Separator(seccionCalculo, orient="horizontal").pack(fill=tk.X, pady=8)
    ttk.Label(seccionCalculo,
              text=f"DV calculado: {detalles['dvEsperado']}   vs   DV ingresado: {detalles['dvDado']}",
              font=("Arial", 12, "bold")).pack(anchor=tk.W)


# ==========================================
# PESTAÑA 2: FORMA CÓNICA
# ==========================================

def construirPestanaConica(contenedor, ecuacionTexto, datosConica):
    """Panel izquierdo con información + panel derecho con gráfica."""
    # Panel izquierdo
    panelIzquierdo = ttk.Frame(contenedor, width=420)
    panelIzquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    panelIzquierdo.pack_propagate(False)

    crearSeccion(panelIzquierdo, "Ecuación General", ecuacionTexto)
    crearSeccion(panelIzquierdo, "Clasificación", f"Tipo: {datosConica.get('tipo', '—')}")

    textoCanonica = datosConica.get("formaCanonica", "—")
    centro = datosConica.get("centro")
    if centro:
        textoCanonica += f"\nCentro/Vértice: {centro}"
    crearSeccion(panelIzquierdo, "Forma Canónica", textoCanonica)

    crearCamposDefensa(panelIzquierdo, "Campos de Defensa Oral",
                       ["Centro", "Vértices", "Focos",
                        "Eje mayor / transverso", "Eje menor / conjugado", "Directriz"])

    # Panel derecho: gráfica
    panelDerecho = ttk.Frame(contenedor)
    panelDerecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)
    ttk.Label(panelDerecho, text="Gráfica de la Cónica", font=("Arial", 12, "bold")).pack(pady=(0, 5))

    lienzo = tk.Canvas(panelDerecho, bg="#f8f9fa", highlightthickness=0, bd=0)
    lienzo.pack(fill=tk.BOTH, expand=True)
    Graficador(lienzo).cargarDatos("conica", datosConica)


# ==========================================
# PESTAÑA 3: LÍMITES
# ==========================================

def construirPestanaLimites(contenedor, analisis):
    """Panel izquierdo con análisis + panel derecho con gráfica."""
    datosFuncion = analisis["funcion"]
    datosLimites = analisis["limites"]

    # Panel izquierdo
    panelIzquierdo = ttk.Frame(contenedor, width=450)
    panelIzquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    panelIzquierdo.pack_propagate(False)

    # Regla de selección del caso
    digitoD8 = datosFuncion["digitos"][7]
    residuo = digitoD8 % 3
    nombresTipos = {0: "Removible", 1: "Salto", 2: "Infinita"}
    crearSeccion(panelIzquierdo, "Regla de Selección",
                 f"d8 = {digitoD8}   →   d8 mod 3 = {residuo}   →   Discontinuidad {nombresTipos[residuo]}")

    # Función generada
    crearSeccion(panelIzquierdo, "Función Generada",
                 f"f(x) = {datosFuncion['funcionFormula']}\n"
                 f"Punto de análisis: x = {datosFuncion['puntoAnalisis']}")

    # Tabla de valores
    seccionTabla = ttk.LabelFrame(panelIzquierdo, text="Tabla de Valores", padding=8)
    seccionTabla.pack(fill=tk.X, pady=(0, 8))

    columnas = ("x (izq)", "f(x)", "x (der)", "f(x) ")
    tablaValores = ttk.Treeview(seccionTabla, columns=columnas, show="headings", height=4)
    for columna in columnas:
        tablaValores.heading(columna, text=columna)
        tablaValores.column(columna, anchor=tk.CENTER, width=95)
    tablaValores.pack(fill=tk.X)

    clavesIzquierda = sorted(datosLimites["valores"]["izq"].keys())
    clavesDerecha = sorted(datosLimites["valores"]["der"].keys())
    for i in range(min(len(clavesIzquierda), len(clavesDerecha))):
        xIzq = clavesIzquierda[i]
        xDer = clavesDerecha[i]
        valorIzq = datosLimites["valores"]["izq"][xIzq]
        valorDer = datosLimites["valores"]["der"][xDer]
        textoIzq = f"{valorIzq:.4f}" if valorIzq is not None else "Indef."
        textoDer = f"{valorDer:.4f}" if valorDer is not None else "Indef."
        tablaValores.insert("", tk.END, values=(f"{xIzq:.4f}", textoIzq, f"{xDer:.4f}", textoDer))

    # Resultado de límites
    puntoA = datosFuncion["puntoAnalisis"]
    crearSeccion(panelIzquierdo, "Resultado de Límites",
                 f"lím(x→{puntoA}⁻) = {datosLimites['limiteIzquierda']}\n"
                 f"lím(x→{puntoA}⁺) = {datosLimites['limiteDerecha']}\n"
                 f"¿Existe el límite? {'Sí' if datosLimites['existeLimite'] else 'No'}")

    # Campos de defensa oral
    crearCamposDefensa(panelIzquierdo, "Campos de Defensa Oral",
                       ["Límite por la izquierda", "Límite por la derecha",
                        "¿Existe el límite?", "Valor f(a)", "¿Es continua?",
                        "Tipo de discontinuidad", "Justificación"])

    # Panel derecho: gráfica
    panelDerecho = ttk.Frame(contenedor)
    panelDerecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)
    ttk.Label(panelDerecho, text="Gráfica de la Función", font=("Arial", 12, "bold")).pack(pady=(0, 5))

    lienzo = tk.Canvas(panelDerecho, bg="#f8f9fa", highlightthickness=0, bd=0)
    lienzo.pack(fill=tk.BOTH, expand=True)
    Graficador(lienzo).cargarDatos("funcion", analisis)


# ==========================================
# FUNCIONES AUXILIARES REUTILIZABLES
# ==========================================

def crearSeccion(contenedorPadre, titulo, contenido):
    """Crea un recuadro con título y texto dentro."""
    seccion = ttk.LabelFrame(contenedorPadre, text=titulo, padding=8)
    seccion.pack(fill=tk.X, pady=(0, 8))
    ttk.Label(seccion, text=contenido, font=("Arial", 10), wraplength=380).pack(anchor=tk.W)


def crearCamposDefensa(contenedorPadre, titulo, listaCampos):
    """Crea campos de texto vacíos para completar durante la defensa oral."""
    seccion = ttk.LabelFrame(contenedorPadre, text=titulo, padding=8)
    seccion.pack(fill=tk.X, pady=(0, 4))
    for nombreCampo in listaCampos:
        fila = ttk.Frame(seccion)
        fila.pack(fill=tk.X, pady=1)
        ttk.Label(fila, text=f"{nombreCampo}:", width=24).pack(side=tk.LEFT)
        ttk.Entry(fila).pack(side=tk.RIGHT, expand=True, fill=tk.X)
