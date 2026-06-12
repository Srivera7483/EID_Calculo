# interface.py - Interfaz gráfica del proyecto EID_Calculo
# ============================================================================
# Construye la ventana principal con tres pestañas:
#   1. Cálculo de RUT   → Muestra el algoritmo Módulo 11 paso a paso
#   2. Forma Cónica      → Ecuación general, canónica, gráfica y campos de defensa
#   3. Límites           → Función por tramos, tabla de valores, gráfica y campos
# ============================================================================

import tkinter as tk
from tkinter import ttk
from modules.plotter import Plotter


# ════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ════════════════════════════════════════════════════════════════════════

def iniciarInterfaz(resultadoValidacion, ecuacionTexto, formaCanonicaData, analisisFunciones):
    """Inicia la interfaz gráfica principal con las tres pestañas."""

    root = _crear_ventana()

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Crear pestañas
    tab_rut    = ttk.Frame(notebook)
    tab_conica = ttk.Frame(notebook)
    tab_limite = ttk.Frame(notebook)

    notebook.add(tab_rut,    text="  Cálculo de RUT  ")
    notebook.add(tab_conica, text="  Forma Cónica  ")
    notebook.add(tab_limite, text="  Límites  ")

    # ── Pestaña 1: RUT ──────────────────────────────────────────────
    _construir_tab_rut(tab_rut, resultadoValidacion)

    # ── Pestaña 2: Cónica ───────────────────────────────────────────
    _construir_tab_conica(tab_conica, ecuacionTexto, formaCanonicaData)

    # ── Pestaña 3: Límites ──────────────────────────────────────────
    _construir_tab_limites(tab_limite, analisisFunciones)

    root.mainloop()


def _crear_ventana():
    """Crea y configura la ventana principal."""
    root = tk.Tk()
    root.title("EID_Calculo – Análisis de Cónicas y Funciones")
    root.geometry("1200x800")
    root.minsize(1000, 650)
    return root


# ════════════════════════════════════════════════════════════════════════
# PESTAÑA 1: CÁLCULO DE RUT
# ════════════════════════════════════════════════════════════════════════

def _construir_tab_rut(frame, resultado):
    """Muestra paso a paso el algoritmo Módulo 11."""

    # Título
    ttk.Label(frame, text="Validación de RUT – Algoritmo Módulo 11",
              font=("Arial", 16, "bold")).pack(pady=(20, 5))

    # Estado con color
    valido = resultado.get("valido", False)
    texto_estado = "✓ RUT VÁLIDO" if valido else "✗ RUT INVÁLIDO"
    color = "green" if valido else "red"
    ttk.Label(frame, text=texto_estado,
              font=("Arial", 14, "bold"), foreground=color).pack(pady=(0, 15))

    # Si no hay detalles, salir
    if "detalles" not in resultado:
        ttk.Label(frame, text="Sin detalles disponibles.").pack()
        return

    det = resultado["detalles"]

    # ── Información del RUT ─────────────────────────────────────────
    info = ttk.LabelFrame(frame, text="Datos del RUT", padding=10)
    info.pack(fill=tk.X, padx=20, pady=(0, 10))
    ttk.Label(info, text=f"Cuerpo: {det['cuerpo']}    |    DV ingresado: {det['dvDado']}",
              font=("Arial", 11)).pack(anchor=tk.W)

    # ── Tabla de multiplicaciones ───────────────────────────────────
    tabla_frame = ttk.LabelFrame(frame, text="Tabla de Multiplicaciones (derecha → izquierda)", padding=10)
    tabla_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

    cols = ("Posición", "Dígito", "Multiplicador", "Producto")
    tabla = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8)
    for col in cols:
        tabla.heading(col, text=col)
        tabla.column(col, anchor=tk.CENTER, width=120)
    tabla.pack(fill=tk.X)

    for i, item in enumerate(det["productos"]):
        tabla.insert("", tk.END, values=(
            i + 1, item["digito"], item["multiplicador"], item["producto"]))

    # ── Desarrollo matemático ───────────────────────────────────────
    calc = ttk.LabelFrame(frame, text="Desarrollo del Cálculo", padding=10)
    calc.pack(fill=tk.X, padx=20, pady=(0, 10))

    pasos = [
        f"Suma de productos:  {' + '.join(str(p['producto']) for p in det['productos'])}  =  {det['suma']}",
        f"Resto (Suma mod 11):  {det['suma']} mod 11  =  {det['resto']}",
        f"DV esperado (11 − Resto):  11 − {det['resto']}  =  {det['dvEsperado']}",
    ]
    for p in pasos:
        ttk.Label(calc, text=p, font=("Arial", 11)).pack(anchor=tk.W, pady=2)

    ttk.Separator(calc, orient="horizontal").pack(fill=tk.X, pady=8)

    ttk.Label(calc, text=f"DV calculado: {det['dvEsperado']}   vs   DV ingresado: {det['dvDado']}",
              font=("Arial", 12, "bold")).pack(anchor=tk.W)


# ════════════════════════════════════════════════════════════════════════
# PESTAÑA 2: FORMA CÓNICA
# ════════════════════════════════════════════════════════════════════════

def _construir_tab_conica(frame, ecuacionTexto, formaCanonicaData):
    """Panel izquierdo con ecuaciones + panel derecho con gráfica."""

    # Panel izquierdo (scroll)
    izq = ttk.Frame(frame, width=420)
    izq.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    izq.pack_propagate(False)

    # Ecuación general
    sec = ttk.LabelFrame(izq, text="Ecuación General", padding=8)
    sec.pack(fill=tk.X, pady=(0, 8))
    ttk.Label(sec, text=ecuacionTexto, font=("Arial", 11)).pack(anchor=tk.W)

    # Tipo de cónica
    tipo = formaCanonicaData.get("tipo", "—")
    sec2 = ttk.LabelFrame(izq, text="Clasificación", padding=8)
    sec2.pack(fill=tk.X, pady=(0, 8))
    ttk.Label(sec2, text=f"Tipo: {tipo}", font=("Arial", 11, "bold")).pack(anchor=tk.W)

    # Forma canónica
    sec3 = ttk.LabelFrame(izq, text="Forma Canónica", padding=8)
    sec3.pack(fill=tk.X, pady=(0, 8))
    ttk.Label(sec3, text=formaCanonicaData.get("formaCanonica", "—"),
              font=("Arial", 11), wraplength=380).pack(anchor=tk.W)

    centro = formaCanonicaData.get("centro")
    if centro:
        ttk.Label(sec3, text=f"Centro/Vértice: {centro}",
                  font=("Arial", 10)).pack(anchor=tk.W, pady=(4, 0))

    # Campos de defensa oral (vacíos, según PDF)
    sec4 = ttk.LabelFrame(izq, text="Campos de Defensa Oral", padding=8)
    sec4.pack(fill=tk.X, pady=(0, 4))

    campos = ["Centro", "Vértices", "Focos",
              "Eje mayor / transverso", "Eje menor / conjugado", "Directriz"]
    for campo in campos:
        row = ttk.Frame(sec4)
        row.pack(fill=tk.X, pady=1)
        ttk.Label(row, text=f"{campo}:", width=22).pack(side=tk.LEFT)
        ttk.Entry(row).pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Panel derecho: gráfica
    der = ttk.Frame(frame)
    der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)

    ttk.Label(der, text="Gráfica de la Cónica",
              font=("Arial", 12, "bold")).pack(pady=(0, 5))

    canvas = tk.Canvas(der, bg="#f8f9fa", highlightthickness=0, bd=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    graficador = Plotter(canvas)
    graficador.set_data("conica", formaCanonicaData)


# ════════════════════════════════════════════════════════════════════════
# PESTAÑA 3: LÍMITES
# ════════════════════════════════════════════════════════════════════════

def _construir_tab_limites(frame, analisis):
    """Panel izquierdo con análisis + panel derecho con gráfica."""

    funcion = analisis["funcion"]
    limites = analisis["limites"]

    # Panel izquierdo
    izq = ttk.Frame(frame, width=450)
    izq.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    izq.pack_propagate(False)

    # ── Regla de selección del caso (requerido por el PDF) ──────────
    sec_regla = ttk.LabelFrame(izq, text="Regla de Selección", padding=8)
    sec_regla.pack(fill=tk.X, pady=(0, 8))

    d8 = funcion["digitos"][7]
    residuo = d8 % 3
    nombres = {0: "Removible", 1: "Salto", 2: "Infinita"}

    ttk.Label(sec_regla,
              text=f"d8 = {d8}   →   d8 mod 3 = {residuo}   →   Discontinuidad {nombres[residuo]}",
              font=("Arial", 10)).pack(anchor=tk.W)

    # ── Función generada ────────────────────────────────────────────
    sec_func = ttk.LabelFrame(izq, text="Función Generada", padding=8)
    sec_func.pack(fill=tk.X, pady=(0, 8))
    ttk.Label(sec_func, text=f"f(x) = {funcion['funcionFormula']}",
              font=("Arial", 11)).pack(anchor=tk.W)
    ttk.Label(sec_func, text=f"Punto de análisis: x = {funcion['puntoAnalisis']}",
              font=("Arial", 10)).pack(anchor=tk.W, pady=(4, 0))

    # ── Tabla de valores (requerida por el PDF) ─────────────────────
    sec_tabla = ttk.LabelFrame(izq, text="Evidencia Computacional – Tabla de Valores", padding=8)
    sec_tabla.pack(fill=tk.X, pady=(0, 8))

    cols = ("x (izq)", "f(x)", "x (der)", "f(x) ")
    tabla = ttk.Treeview(sec_tabla, columns=cols, show="headings", height=4)
    for col in cols:
        tabla.heading(col, text=col)
        tabla.column(col, anchor=tk.CENTER, width=95)
    tabla.pack(fill=tk.X)

    # Datos de la tabla
    vals_izq = limites["valores"]["izq"]
    vals_der = limites["valores"]["der"]
    keys_izq = sorted(vals_izq.keys())
    keys_der = sorted(vals_der.keys())

    for i in range(min(len(keys_izq), len(keys_der))):
        xi = keys_izq[i]
        xd = keys_der[i]
        fi = f"{vals_izq[xi]:.4f}" if vals_izq[xi] is not None else "Indef."
        fd = f"{vals_der[xd]:.4f}" if vals_der[xd] is not None else "Indef."
        tabla.insert("", tk.END, values=(f"{xi:.4f}", fi, f"{xd:.4f}", fd))

    # ── Resultado de los límites ────────────────────────────────────
    sec_lim = ttk.LabelFrame(izq, text="Resultado de Límites", padding=8)
    sec_lim.pack(fill=tk.X, pady=(0, 8))

    ttk.Label(sec_lim, text=f"lím(x→{funcion['puntoAnalisis']}⁻) = {limites['limiteIzquierda']}",
              font=("Arial", 10)).pack(anchor=tk.W)
    ttk.Label(sec_lim, text=f"lím(x→{funcion['puntoAnalisis']}⁺) = {limites['limiteDerecha']}",
              font=("Arial", 10)).pack(anchor=tk.W)
    existe = "Sí" if limites["existeLimite"] else "No"
    ttk.Label(sec_lim, text=f"¿Existe el límite? {existe}",
              font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(4, 0))

    # ── Campos de defensa oral (vacíos, según PDF) ──────────────────
    sec_def = ttk.LabelFrame(izq, text="Campos de Defensa Oral", padding=8)
    sec_def.pack(fill=tk.X, pady=(0, 4))

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
        row = ttk.Frame(sec_def)
        row.pack(fill=tk.X, pady=1)
        ttk.Label(row, text=f"{campo}:", width=24).pack(side=tk.LEFT)
        ttk.Entry(row).pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Panel derecho: gráfica
    der = ttk.Frame(frame)
    der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)

    ttk.Label(der, text="Gráfica de la Función",
              font=("Arial", 12, "bold")).pack(pady=(0, 5))

    canvas = tk.Canvas(der, bg="#f8f9fa", highlightthickness=0, bd=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    graficador = Plotter(canvas)
    graficador.set_data("funcion", analisis)
