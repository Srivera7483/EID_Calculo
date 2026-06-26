# EID_Calculo – MAT1186 Introducción al Cálculo

**Pontificia Universidad Católica de Temuco**  
Asignatura: MAT1186 – Introducción al Cálculo  
Ponderación: 25% de la calificación final

---

## Descripción

Aplicación en Python que, a partir de un **RUT chileno válido**, genera y analiza secciones cónicas y funciones por tramos. Todos los cálculos matemáticos están implementados **manualmente**, sin el uso de librerías de álgebra computacional.

---

## Funcionalidades

1. **Validación del RUT** mediante el algoritmo oficial Módulo 11, mostrando cada paso.
2. **Ecuación General de la Cónica** `Ax² + By² + Cx + Dy + E = 0`, calculada a partir de los dígitos del RUT.
3. **Clasificación automática** de la cónica (circunferencia, elipse, hipérbola, parábola).
4. **Transformación a forma canónica** completando cuadrados, con desarrollo paso a paso.
5. **Transformación inversa** canónica → general, con expansión algebraica paso a paso.
6. **Graficación** de la cónica en el plano cartesiano (canvas interactivo con zoom y desplazamiento).
7. **Análisis de funciones por tramos**: límites laterales, continuidad y tipo de discontinuidad.
8. **Interfaz gráfica** con tres pestañas: Cálculo RUT, Forma Cónica, Límites.

---

## Estructura del Proyecto

```
EID_Calculo/
├── README.md
├── requirements.txt
├── codigo_etica.md
├── eidMaterial/
│   ├── contexto.md
│   ├── coordinacion_equipo.md
│   └── codigo_etica.md
│
└── src/
    ├── main.py                  # Punto de entrada
    ├── modules/
    │   ├── rut_validator.py     # Validación RUT (Módulo 11)
    │   ├── conic.py             # Construcción y clasificación de cónicas
    │   ├── transformations.py   # Transformaciones general ↔ canónica
    │   ├── plotter.py           # Graficación en canvas Tkinter
    │   └── functions.py         # Análisis de funciones por tramos
    └── ui/
        └── interface.py         # Interfaz gráfica (3 pestañas)
```

---

## Requisitos

- Python 3.9 o superior
- `tkinter` (incluido en la instalación estándar de Python)
- `matplotlib` (solo si se usa para graficación alternativa)

```bash
pip install -r requirements.txt
```

---

## Cómo Ejecutar

```bash
# Activar entorno virtual (si aplica)
source .venv/bin/activate

# Ejecutar desde la raíz del proyecto
python src/main.py
```

El programa pedirá ingresar un **RUT chileno válido** (formato `12345678-9`). Tiene hasta 3 intentos. Tras validarlo, abre la interfaz gráfica con las tres pestañas.

---

## Convenciones de Código

- **Variables y funciones**: `camelCase`
- **Clases**: `PascalCase`
- **Comentarios**: solo los necesarios, explicando decisiones no obvias

---

## Integrantes
______________________________________________
| Nombre                | Rol                 |
|-----------------------|---------------------|
| Benjamín De La Fuente | Jefe de grupo       |
| Sebastian Rivera      | Suplente            |
| Rodrigo Reyes         | Integrante          |
-----------------------------------------------
---

## Tecnologías

- **Lenguaje:** Python 3.9+
- **Interfaz gráfica:** Tkinter (built-in)
- **Versionamiento:** Git + GitHub