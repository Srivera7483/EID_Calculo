# interface.py - Interfaz gráfica con tres pestañas
# Pestaña 1: Cálculo de RUT (Módulo 11)
# Pestaña 2: Forma Cónica (ecuación, gráfica, campos de defensa)
# Pestaña 3: Límites (función por tramos, tabla de valores, gráfica)

import tkinter as tk
from tkinter import ttk
from modules.plotter import Plotter


def iniciarInterfaz(resultadoValidacion, ecuacionTexto, formaCanonicaData, analisisFunciones):
    """Inicia la ventana principal con tres pestañas."""
    root = tk.Tk()
    root.title("EID_Calculo – Cónicas y Funciones")
    root.geometry("1200x800")
    root.minsize(1000, 650)

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)
    notebook.add(tab1, text="  Cálculo de RUT  ")
    notebook.add(tab2, text="  Forma Cónica  ")
    notebook.add(tab3, text="  Límites  ")

    _tab_rut(tab1, resultadoValidacion)
    _tab_conica(tab2, ecuacionTexto, formaCanonicaData)
    _tab_limites(tab3, analisisFunciones)

    root.mainloop()


# --- Pestaña 1: RUT ---

def _tab_rut(frame, resultado):
    """Muestra el algoritmo Módulo 11 paso a paso."""
    ttk.Label(frame, text="Validación de RUT – Algoritmo Módulo 11",
              font=("Arial", 16, "bold")).pack(pady=(20, 5))

    valido = resultado.get("valido", False)
    color = "green" if valido else "red"
    texto = "✓ RUT VÁLIDO" if valido else "✗ RUT INVÁLIDO"
    ttk.Label(frame, text=texto, font=("Arial", 14, "bold"),
              foreground=color).pack(pady=(0, 15))

    if "detalles" not in resultado:
        return

    det = resultado["detalles"]

    # Info del RUT
    info = ttk.LabelFrame(frame, text="Datos del RUT", padding=10)
    info.pack(fill=tk.X, padx=20, pady=(0, 10))
    ttk.Label(info, text=f"Cuerpo: {det['cuerpo']}    |    DV ingresado: {det['dvDado']}",
              font=("Arial", 11)).pack(anchor=tk.W)

    # Tabla de multiplicaciones
    tf = ttk.LabelFrame(frame, text="Tabla de Multiplicaciones (derecha → izquierda)", padding=10)
    tf.pack(fill=tk.X, padx=20, pady=(0, 10))

    cols = ("Posición", "Dígito", "Multiplicador", "Producto")
    tabla = ttk.Treeview(tf, columns=cols, show="headings", height=8)
    for col in cols:
        tabla.heading(col, text=col)
        tabla.column(col, anchor=tk.CENTER, width=120)
    tabla.pack(fill=tk.X)

    for i, item in enumerate(det["productos"]):
        tabla.insert("", tk.END, values=(i + 1, item["digito"], item["multiplicador"], item["producto"]))

    # Cálculos finales
    calc = ttk.LabelFrame(frame, text="Desarrollo del Cálculo", padding=10)
    calc.pack(fill=tk.X, padx=20, pady=(0, 10))

    productos_str = " + ".join(str(p["producto"]) for p in det["productos"])
    for texto in [
        f"Suma de productos:  {productos_str}  =  {det['suma']}",
        f"Resto (Suma mod 11):  {det['suma']} mod 11  =  {det['resto']}",
        f"DV esperado (11 − Resto):  11 − {det['resto']}  =  {det['dvEsperado']}",
    ]:
        ttk.Label(calc, text=texto, font=("Arial", 11)).pack(anchor=tk.W, pady=2)

    ttk.Separator(calc, orient="horizontal").pack(fill=tk.X, pady=8)
    ttk.Label(calc, text=f"DV calculado: {det['dvEsperado']}   vs   DV ingresado: {det['dvDado']}",
              font=("Arial", 12, "bold")).pack(anchor=tk.W)


# --- Pestaña 2: Cónica ---

def _tab_conica(frame, ecuacionTexto, datos):
    """Panel izquierdo con info + panel derecho con gráfica."""
    # Panel izquierdo
    izq = ttk.Frame(frame, width=420)
    izq.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    izq.pack_propagate(False)

    # Ecuación general
    _seccion(izq, "Ecuación General", ecuacionTexto)

    # Clasificación
    _seccion(izq, "Clasificación", f"Tipo: {datos.get('tipo', '—')}")

    # Forma canónica
    texto_canon = datos.get("formaCanonica", "—")
    centro = datos.get("centro")
    if centro:
        texto_canon += f"\nCentro/Vértice: {centro}"
    _seccion(izq, "Forma Canónica", texto_canon)

    # Campos de defensa oral (vacíos)
    _campos_defensa(izq, "Campos de Defensa Oral",
                    ["Centro", "Vértices", "Focos",
                     "Eje mayor / transverso", "Eje menor / conjugado", "Directriz"])

    # Panel derecho: gráfica
    der = ttk.Frame(frame)
    der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)
    ttk.Label(der, text="Gráfica de la Cónica", font=("Arial", 12, "bold")).pack(pady=(0, 5))

    canvas = tk.Canvas(der, bg="#f8f9fa", highlightthickness=0, bd=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    Plotter(canvas).set_data("conica", datos)


# --- Pestaña 3: Límites ---

def _tab_limites(frame, analisis):
    """Panel izquierdo con análisis + panel derecho con gráfica."""
    funcion = analisis["funcion"]
    limites = analisis["limites"]

    # Panel izquierdo
    izq = ttk.Frame(frame, width=450)
    izq.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    izq.pack_propagate(False)

    # Regla de selección
    d8 = funcion["digitos"][7]
    residuo = d8 % 3
    tipos = {0: "Removible", 1: "Salto", 2: "Infinita"}
    _seccion(izq, "Regla de Selección",
             f"d8 = {d8}   →   d8 mod 3 = {residuo}   →   Discontinuidad {tipos[residuo]}")

    # Función generada
    _seccion(izq, "Función Generada",
             f"f(x) = {funcion['funcionFormula']}\nPunto de análisis: x = {funcion['puntoAnalisis']}")

    # Tabla de valores
    tf = ttk.LabelFrame(izq, text="Tabla de Valores", padding=8)
    tf.pack(fill=tk.X, pady=(0, 8))

    cols = ("x (izq)", "f(x)", "x (der)", "f(x) ")
    tabla = ttk.Treeview(tf, columns=cols, show="headings", height=4)
    for col in cols:
        tabla.heading(col, text=col)
        tabla.column(col, anchor=tk.CENTER, width=95)
    tabla.pack(fill=tk.X)

    keys_i = sorted(limites["valores"]["izq"].keys())
    keys_d = sorted(limites["valores"]["der"].keys())
    for i in range(min(len(keys_i), len(keys_d))):
        xi, xd = keys_i[i], keys_d[i]
        fi = limites["valores"]["izq"][xi]
        fd = limites["valores"]["der"][xd]
        fi_str = f"{fi:.4f}" if fi is not None else "Indef."
        fd_str = f"{fd:.4f}" if fd is not None else "Indef."
        tabla.insert("", tk.END, values=(f"{xi:.4f}", fi_str, f"{xd:.4f}", fd_str))

    # Resultado de límites
    a = funcion["puntoAnalisis"]
    _seccion(izq, "Resultado de Límites",
             f"lím(x→{a}⁻) = {limites['limiteIzquierda']}\n"
             f"lím(x→{a}⁺) = {limites['limiteDerecha']}\n"
             f"¿Existe el límite? {'Sí' if limites['existeLimite'] else 'No'}")

    # Campos de defensa oral
    _campos_defensa(izq, "Campos de Defensa Oral",
                    ["Límite por la izquierda", "Límite por la derecha",
                     "¿Existe el límite?", "Valor f(a)", "¿Es continua?",
                     "Tipo de discontinuidad", "Justificación"])

    # Panel derecho: gráfica
    der = ttk.Frame(frame)
    der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)
    ttk.Label(der, text="Gráfica de la Función", font=("Arial", 12, "bold")).pack(pady=(0, 5))

    canvas = tk.Canvas(der, bg="#f8f9fa", highlightthickness=0, bd=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    Plotter(canvas).set_data("funcion", analisis)


# --- Helpers reutilizables ---

def _seccion(parent, titulo, contenido):
    """Crea un LabelFrame con texto."""
    sec = ttk.LabelFrame(parent, text=titulo, padding=8)
    sec.pack(fill=tk.X, pady=(0, 8))
    ttk.Label(sec, text=contenido, font=("Arial", 10), wraplength=380).pack(anchor=tk.W)

def _campos_defensa(parent, titulo, campos):
    """Crea campos de texto vacíos para la defensa oral."""
    sec = ttk.LabelFrame(parent, text=titulo, padding=8)
    sec.pack(fill=tk.X, pady=(0, 4))
    for campo in campos:
        row = ttk.Frame(sec)
        row.pack(fill=tk.X, pady=1)
        ttk.Label(row, text=f"{campo}:", width=24).pack(side=tk.LEFT)
        ttk.Entry(row).pack(side=tk.RIGHT, expand=True, fill=tk.X)
