import tkinter as tk
from tkinter import ttk
from modules.plotter import Plotter

def iniciar_interfaz(ecuacion_general, forma_canonica, analisis_funciones, rut_info="12345678-9"):
    """
    Inicia la ventana principal de la interfaz gráfica de usuario.
    """
    root = tk.Tk()
    root.title("EID_Calculo - Análisis de Cónicas y Funciones")
    root.geometry("1200x700") # Un poco más ancho para que quepa bien el canvas de 800x600
    
    # FRAME IZQUIERDO: Datos y Defensa
    frame_izquierdo = ttk.Frame(root, padding="10")
    frame_izquierdo.pack(side=tk.LEFT, fill=tk.Y, expand=False)
    
    # Sección 1: Resultados Automáticos
    ttk.Label(frame_izquierdo, text="Resultados del Análisis", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=5)
    ttk.Label(frame_izquierdo, text=f"RUT validado: {rut_info}").pack(anchor=tk.W)
    ttk.Label(frame_izquierdo, text=f"Ecuación General:\n{ecuacion_general}").pack(anchor=tk.W, pady=5)
    ttk.Label(frame_izquierdo, text=f"Forma Canónica:\n{forma_canonica}").pack(anchor=tk.W, pady=5)
    ttk.Label(frame_izquierdo, text=f"Caso de Función:\n{analisis_funciones}").pack(anchor=tk.W, pady=5)
    
    ttk.Separator(frame_izquierdo, orient='horizontal').pack(fill='x', pady=10)
    
    # Sección 2: Campos vacíos para la Defensa (Cónicas)
    ttk.Label(frame_izquierdo, text="Cónica", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=5)
    
    campos_conica = ["Centro", "Vértices", "Focos", "Eje mayor / transverso", "Eje menor / conjugado", "Directriz"]
    for campo in campos_conica:
        row = ttk.Frame(frame_izquierdo)
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text=f"{campo}:", width=20).pack(side=tk.LEFT)
        ttk.Entry(row).pack(side=tk.RIGHT, expand=True, fill=tk.X)

    ttk.Separator(frame_izquierdo, orient='horizontal').pack(fill='x', pady=10)

    # Sección 3: Campos vacíos para la Defensa (Límites y Continuidad)
    ttk.Label(frame_izquierdo, text="Funciones", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=5)
    
    campos_funciones = [
        "Límite por la izquierda", "Límite por la derecha", 
        "¿Existe el límite?", "Valor f(a)", 
        "¿Es continua?", "Tipo de discontinuidad", "Justificación"
    ]
    for campo in campos_funciones:
        row = ttk.Frame(frame_izquierdo)
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text=f"{campo}:", width=20).pack(side=tk.LEFT)
        ttk.Entry(row).pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # FRAME DERECHO: Gráficos
    frame_derecho = ttk.Frame(root, padding="10")
    frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    ttk.Label(frame_derecho, text="Representación Gráfica", font=("Arial", 12, "bold")).pack(pady=5)
    
    # 1. Crear el Canvas nativo de Tkinter
    canvas = tk.Canvas(frame_derecho, width=800, height=600, bg="white", highlightthickness=1, highlightbackground="black")
    canvas.pack(pady=10)

    # 2. Instanciar la clase Plotter
    graficador = Plotter(canvas, width=800, height=600)
    
    # 3. Dibujar los ejes
    graficador.dibujar_ejes()
    
    graficador.actualizar()

    root.mainloop()
