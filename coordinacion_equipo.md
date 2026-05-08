e# Plan de Coordinación - Proyecto MAT1186 (Cálculo)

Para evitar "topones" (conflictos de *merge* en Git) y asegurar que los 3 trabajen en paralelo de forma eficiente, la clave es dividir el proyecto por **módulos independientes**. Según el `contexto.md`, la arquitectura sugerida permite exactamente esto.

Aquí tienes la propuesta de división de roles:

---

## 🧑‍💻 Integrante 1: Benjamín (Lógica de Cónicas y RUT)
**Enfoque:** Validaciones iniciales y álgebra de secciones cónicas.
Trabajarás de forma independiente generando la lógica matemática que luego el frontend consumirá.

**Archivos asignados:**
- `src/modules/rut_validator.py`: Algoritmo módulo 11 para validar el RUT y extraer los dígitos.
- `src/modules/conic.py`: Construcción de los coeficientes ($A, B, C, D, E$) y lógica de clasificación (Saber si es elipse, parábola, etc.).
- `src/modules/transformations.py`: Lógica para completar cuadrados y pasar de ecuación general a canónica, y viceversa.
- `tests/test_rut.py` y `tests/test_conic.py`.

*¿Cómo evitar topones?* Tú solo te encargas de recibir strings/números y devolver diccionarios o tuplas con los resultados matemáticos. No toques nada de la interfaz gráfica ni de los gráficos.

---

## 🧑‍💻 Integrante 2: Sebastián (Análisis de Funciones por Tramos)
**Enfoque:** Lógica de límites, continuidad y discontinuidad.
Al igual que Benjamín, Sebastián trabajará en el backend pero en un archivo completamente separado, enfocado en la Fase 6 del proyecto.

**Archivos asignados:**
- `src/modules/functions.py`: 
  - Lógica para identificar el caso de la función según el RUT ($d_8 \pmod 3$).
  - Cálculo manual de límites laterales en el punto $a = d_3$.
  - Lógica para clasificar la discontinuidad (removible, de salto o infinita).
  - Algoritmo para generar las tablas de valores (arrays de valores $x$ e $y$ cercanos al punto crítico).
- `tests/test_functions.py`.
- Redacción del `codigo_etica.md`.

*¿Cómo evitar topones?* Toda la lógica de límites de Sebastián vive en `functions.py`. No se cruza en absoluto con el código de cónicas de Benjamín.

---

## 🧑‍💻 Integrante 3: [Tercer Integrante] (UI, Gráficos e Integración)
**Enfoque:** Interfaz gráfica (Tkinter, PyQt o Web), Matplotlib y orquestación.
Esta persona unirá todo. Necesitará importar las funciones de Benjamín y Sebastián, y conectarlas a los botones y gráficos.

**Archivos asignados:**
- `src/main.py`: El script principal que inicia la aplicación.
- `src/ui/interface.py`: Creación de la ventana, botones, y los campos de texto vacíos (centro, vértices, límites, etc.) que pide la pauta para la defensa.
- `src/modules/plotter.py`: Funciones usando **Matplotlib** para graficar tanto las cónicas (usando la ecuación de Benjamín) como las funciones por tramos (usando los datos de Sebastián, prestando atención a los saltos o asíntotas).
- `requirements.txt`.

*¿Cómo evitar topones?* El Integrante 3 debe definir *funciones mock* (funciones vacías que devuelven datos falsos) al principio, para poder armar la interfaz visual mientras Benjamín y Sebastián terminan sus lógicas reales. Una vez que ellos terminen, el Integrante 3 simplemente cambia el *mock* por la importación real.

---

## 📝 Reglas de Git para el equipo
Para que esto funcione a la perfección en sus ramas (como `devBenjaminDeLaFuente` y `Avances-Sebastian-Rivera`):

1. **Nunca trabajen en el mismo archivo.** Si alguien necesita hacer un cambio en un archivo de otro, pídanselo por mensaje.
2. **Estructura inicial:** Alguien (ej. Benjamín) debe crear la estructura de carpetas vacía (`src/`, `src/modules/`, etc.) y los archivos `.py` en blanco. Hacer un commit en `Desarrollo` y que los 3 hagan `git pull` de eso **antes** de empezar a programar.
3. **Commits atómicos:** Hagan commits por cada funcionalidad pequeña ("Terminada validación de RUT", "Agregado cálculo de límite lateral", etc.), mínimo los 3 requeridos por la pauta.
