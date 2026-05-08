# plotter.py - Graficación de secciones cónicas
# ============================================================================
# Usa Matplotlib para graficar la cónica en el plano cartesiano.
# Debe mostrar correctamente:
# - Centro, vértices, focos
# - Ejes de simetría
# - Asíntotas (si corresponde)
# - Directriz (si corresponde)

import matplotlib.pyplot as plt

def graficarConica(coeficientes, formaCanonica, parametros):
    """
    Grafica la cónica en el plano cartesiano.
    
    Parámetros:
        coeficientes (dict): {'A': float, 'B': float, 'C': float, 'D': float, 'E': float}
        formaCanonica (str): Ecuación en forma canónica
        parametros (dict): Centro, vértices, focos, etc.
    
    Retorna:
        matplotlib.figure.Figure: Figura con la gráfica
    """
    # TODO: Implementar graficación según tipo de cónica
    # 1. Crear figura y eje
    # 2. Generar puntos de la cónica
    # 3. Plotear cónica
    # 4. Agregar elementos (centro, vértices, focos, ejes)
    # 5. Formatear y mostrar
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # TODO: Plotear cónica
    # ax.plot(x, y, 'b-', linewidth=2, label='Cónica')
    
    # TODO: Plotear elementos
    # Centro
    # ax.plot(centro[0], centro[1], 'ro', markersize=8, label='Centro')
    
    # Vértices
    # ax.plot(vertices_x, vertices_y, 'gs', markersize=8, label='Vértices')
    
    # Focos
    # ax.plot(focos_x, focos_y, 'mo', markersize=8, label='Focos')
    
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(formaCanonica)
    ax.legend()
    
    return fig

def mostrarGrafica(fig):
    """
    Muestra la gráfica en pantalla.
    """
    plt.show()
