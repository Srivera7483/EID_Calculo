# CONTEXTO DEL PROYECTO - MAT1186
## Análisis y Modelamiento de Secciones Cónicas y Funciones por Tramos a partir del RUT

**Versión:** 2026  
**Asignatura:** MAT1186 - Introducción al Cálculo  
**Universidad:** Pontificia Universidad Católica de Temuco  
**Ponderación:** 25% de la calificación final  

---

## 1. DESCRIPCIÓN GENERAL DEL PROYECTO

Este es un proyecto integrado que combina **matemáticas**, **programación** y **trabajo colaborativo**. El objetivo principal es desarrollar una aplicación en Python que:

1. Valide un RUT chileno válido
2. Genere automáticamente una ecuación cónica a partir de sus dígitos
3. Clasifique y transforme la cónica a su forma canónica
4. Grafique la cónica en el plano cartesiano
5. Analice funciones por tramos generadas del mismo RUT, estudiando límites y continuidad

### Competencias a desarrollar:
- **Actuación ética:** Responsabilidad en el trabajo colaborativo y códigos de ética internos
- **Aprendizaje autónomo:** Gestión independiente del aprendizaje matemático y computacional
- **Aplicación de ciencias de la Ingeniería:** Implementación de modelos matemáticos con razonamiento lógico deductivo

---

## 2. ORGANIZACIÓN DEL EQUIPO

### Conformación:
- **Exactamente 3 integrantes** (sin excepciones)
- **1 Líder designado** responsable de coordinación y comunicación
- **1 Código de Ética interno** que regule el trabajo y resolución de conflictos

### Responsabilidades:
- División clara de tareas con evidencia de participación (mínimo 3 commits por integrante)
- Uso obligatorio de GitHub como repositorio
- Comunicación efectiva y resolución colaborativa de problemas

---

## 3. ESTRUCTURA DEL PROYECTO

### 3.1 FASE 1: Fundamento Matemático

#### Validación del RUT
- Implementar correctamente el **algoritmo oficial del módulo 11**
- Verificar que el dígito verificador sea válido
- Mostrar paso a paso el procedimiento de validación

#### Variable auxiliar `v` según dígito verificador:
```
v = 10,  si DV = K
v = 11,  si DV = 0
v = DV,  si DV ∈ [1, 9]
```

#### Construcción de la ecuación general: `Ax² + By² + Cx + Dy + E = 0`

**Cálculo de coeficientes:**
- `A = (d₁ + d₂) / v`
- `B = (d₃ + d₄) / v`
- `C = -(d₅ + d₆)`
- `D = -(d₇ + d₈)`
- `E = d₁ + d₃ + d₅ + d₇`

**Ajustes para obtener variedad de cónicas:**

| Condición | Ajuste | Efecto |
|-----------|--------|--------|
| d₈ es impar | B → -B | Genera hipérbolas |
| d₁ = d₂ | B = A | Genera circunferencias |
| (d₅ + d₆) múltiplo de 3 | A = 0 o B = 0 | Genera parábolas |

#### Clasificación automática de la cónica:
- **Circunferencia:** A = B ≠ 0
- **Elipse:** A y B mismo signo, A ≠ B
- **Hipérbola:** A y B signos opuestos
- **Parábola:** Exactamente A = 0 o B = 0

#### Transformación a forma canónica:
- Mostrar **paso a paso** todos los cálculos algebraicos
- Completar cuadrados para x e y
- Indicar centro, parámetros, vértices, focos según corresponda
- Mostrar el procedimiento inverso (canónica → general)

---

### 3.2 FASE 2: Desarrollo del Programa

#### Requerimientos funcionales mínimos:

1. Ingreso y validación del RUT chileno real
2. Mostrar paso a paso la validación del RUT
3. Extraer correctamente los 8 dígitos del cuerpo
4. Mostrar construcción paso a paso de la ecuación general
5. Construir la ecuación general automáticamente
6. Determinar el tipo de cónica (automático)
7. Mostrar la ecuación general en pantalla
8. Mostrar la forma canónica cuando corresponda
9. Resolver y mostrar transformación general → canónica
10. Resolver y mostrar transformación inversa canónica → general
11. Graficar correctamente la cónica en el plano cartesiano
12. Presentar interfaz intuitiva, ordenada y visualmente adecuada
13. Incorporar módulo de análisis de funciones por tramos

#### Restricciones tecnológicas:

**❌ PROHIBIDO:**
- `numpy`, `math`, `sympy`, `scipy`, `pandas`
- Cualquier librería de álgebra computacional o cálculo simbólico
- Evaluación automática de funciones o límites

**✅ PERMITIDO:**
- Cualquier framework web (Flask, Django, FastAPI, etc.)
- Cualquier librería de UI (Pygame, Tkinter, Web frameworks, etc.)
- Librerías **solo para construcción de interfaz gráfica**

**OBLIGATORIO:**
- Todos los cálculos matemáticos implementados **manualmente**
- Código modular y bien organizado
- Manejo básico de errores para RUTs inválidos

---

### 3.3 FASE 3: Desarrollo Profesional del Código

#### Estructura del repositorio:

```
nombre-proyecto/
├── README.md
├── contexto.md
├── .gitignore
├── requirements.txt
├── codigo_etica.md
│
├── src/
│   ├── main.py                 # Punto de entrada
│   ├── __init__.py
│   │
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── rut_validator.py    # Validación RUT
│   │   ├── conic.py            # Construcción y clasificación cónicas
│   │   ├── transformations.py  # Transformaciones general↔canónica
│   │   ├── plotter.py          # Graficación
│   │   └── functions.py        # Análisis de funciones por tramos
│   │
│   └── ui/
│       ├── __init__.py
│       └── interface.py        # Interfaz gráfica
│
└── tests/
    ├── __init__.py
    ├── test_rut.py
    ├── test_conic.py
    └── test_functions.py
```

#### Criterios de calidad:

1. **GitHub obligatorio** con evidencia de colaboración
2. Mínimo **3 commits por integrante**
3. **Organización modular:** responsabilidades separadas en archivos
4. **Nombres claros:** variables, funciones y archivos significativos
5. **Comentarios pertinentes:** solo los necesarios (no excesivos)
6. **Manejo de errores:** validación de entrada especialmente para RUTs
7. **Calificación grupal:** todo el equipo responde por el trabajo

---

### 3.4 FASE 4: Casos de Prueba y Visualización Gráfica

#### Requerimientos:

- Probar con **múltiples RUTs válidos**
- Evidenciar las **4 cónicas:** circunferencia, parábola, elipse, hipérbola
- Graficación **matemáticamente correcta** y coherente con la ecuación
- **NO** se aceptan RUTs inválidos o inventados

#### Elementos interactivos en la interfaz:

Campos de texto **inicialmente vacíos** para completar durante la defensa:
- Centro
- Vértices
- Focos
- Eje mayor / eje transverso
- Eje menor / eje conjugado
- Directriz

**Objetivo:** El estudiante debe identificar y ubicar correctamente estos elementos según el análisis matemático durante la defensa oral.

#### Criterios de interfaz:

- Presentación intuitiva, ordenada y consistente
- Visualmente agradable
- Interacción clara para usuario y equipo docente
- Evitar soluciones incompletas, confusas o improvisadas

---

### 3.5 FASE 5: Defensa Oral

#### Formato:
- **Grupal:** todos participan
- **Aleatorio:** el docente selecciona quién responde cada pregunta
- **Enfoque:** código, decisiones de implementación, comprensión matemática

#### Aspectos a evaluar:

- Validación correcta del RUT
- Construcción de coeficientes
- Clasificación correcta de cónicas
- Lógica de graficación
- Transformaciones general ↔ canónica
- Estructura del programa
- Aporte individual de cada integrante

#### Durante la defensa se puede solicitar:

- Completar campos de cónica en la interfaz
- Explicar el funcionamiento del código
- Justificar decisiones de implementación
- Demostrar comprensión matemática de centro, focos, vértices, etc.

**⚠️ NOTA:** Si el grupo no demuestra comprensión del funcionamiento general, no justifica decisiones o no domina matemáticamente el problema, **afecta la calificación grupal**.

---

### 3.6 FASE 6: Análisis de Funciones por Tramos

#### Objetivo:
Analizar funciones generadas automáticamente a partir del RUT, estudiando **límites laterales**, **continuidad** y **tipos de discontinuidad** mediante implementación **manual** (sin librerías de cálculo simbólico).

#### Punto de análisis:
```
a = d₃
```

#### Tipos de funciones a generar:

##### **Caso 1: Discontinuidad Removible**
```
f₁(x) = (x - a)(x + d₁) / (x - a)

Límite cuando x → a: a + d₁
Comportamiento: Existe un punto no definido en x = a
```

##### **Caso 2: Discontinuidad de Salto**
```
f(x) = { x + d₂, si x < a
       { x + d₄, si x ≥ a

lim f(x) (x→a⁻) = a + d₂
lim f(x) (x→a⁺) = a + d₄

Si son distintos → Discontinuidad de salto
```

##### **Caso 3: Discontinuidad Infinita**
```
f(x) = (d₅ + 1) / (x - a)

Comportamiento: Función crece/decrece sin límite
Asíntota vertical en x = a
```

#### Regla de selección del caso:

| d₈ mod 3 | Caso |
|----------|------|
| ≡ 0 (múltiplo) | Discontinuidad removible |
| ≡ 1 (residuo 1) | Discontinuidad de salto |
| ≡ 2 (residuo 2) | Discontinuidad infinita |

#### Requerimientos del sistema:

**Análisis automático:**
- Identificar puntos críticos
- Calcular límites laterales: `lim(x→a⁻) f(x)` y `lim(x→a⁺) f(x)`
- Determinar si el límite existe
- Analizar continuidad en el punto
- Clasificar tipo de discontinuidad
- **Justificar matemáticamente** por qué es ese tipo

**Evidencia computacional:**
- Tabla de valores cercanos al punto a:
  - Por izquierda: a-1, a-0.1, a-0.01, a-0.001
  - Por derecha: a+0.001, a+0.01, a+0.1, a+1
- Observar comportamiento de la función al aproximarse al punto crítico

**Representación gráfica:**
- Graficar la función completa
- Mostrar claramente el comportamiento en torno al punto crítico
- Evidenciar visualmente: continuidad, salto, ruptura o crecimiento infinito
- Para discontinuidad removible: mostrar punto no definido
- Para discontinuidad infinita: evidenciar tendencia a infinito

#### Interfaz del módulo:

Campos **inicialmente vacíos** para completar durante defensa:

- Límite por la izquierda
- Límite por la derecha
- Conclusión sobre existencia del límite
- Valor de la función en el punto (si existe)
- Conclusión sobre continuidad
- Tipo de discontinuidad
- Justificación escrita del comportamiento

**Objetivo:** El estudiante interpreta la información y demuestra comprensión del concepto de límite.

#### Restricciones de implementación:

**❌ PROHIBIDO:**
- `numpy`, `math`, `sympy`, `scipy`, `pandas`
- Simplificación automática de expresiones
- Evaluación automática de límites

**✅ OBLIGATORIO:**
- Implementar **manualmente** todos los cálculos
- Lógica propia para simplificar, calcular límites, clasificar discontinuidades
- Generar tablas de valores con código propio

**✅ PERMITIDO:**
- Librerías exclusivas para construcción de interfaz gráfica

#### Evaluación en defensa:

Se puede solicitar:
- Explicar comportamiento en un punto específico
- Justificar existencia/no existencia del límite
- Completar campos vacíos de la interfaz
- Clasificar correctamente la discontinuidad
- Interpretar la gráfica generada
- Relacionar evidencia computacional con análisis matemático

**Objetivo:** Evaluar capacidad para relacionar **algoritmos**, **análisis matemático** y **comprensión conceptual del límite**.

---

## 4. STACK TECNOLÓGICO RECOMENDADO

### Backend/Lógica:
- **Lenguaje:** Python 3.9+
- **Validación RUT:** Implementación manual
- **Cálculos matemáticos:** Sin librerías (manual)
- **Estructuras:** Clases y módulos bien organizados

### Interfaz Gráfica (elige una):
- **Web:** Flask + HTML/CSS/JavaScript (Matplotlib para gráficos)
- **Desktop:** Tkinter (built-in) + Matplotlib
- **Moderna:** PyQt6 + Matplotlib
- **Web moderna:** Django + Plotly/Chart.js

### Graficación:
- **Matplotlib:** Para gráficos estáticos (permitido, no es álgebra computacional)
- **Plotly:** Para gráficos interactivos en web

### Versionamiento:
- **GitHub:** Repositorio remoto obligatorio
- **.gitignore:** Ignorar `__pycache__`, `.venv`, archivos temporales
- **requirements.txt:** Dependencias del proyecto

---

## 5. CONVENCIONES DE CÓDIGO

### Naming:
```python
# Variables y funciones: snake_case
rut_ingresado = "20123456-K"
def validar_rut(rut):
    pass

# Constantes: UPPER_SNAKE_CASE
MODULO_11 = 11
DIGITOS_RUT = 8

# Clases: PascalCase
class ConicaEcuacion:
    pass
```

### Estructura de funciones:
```python
def calcular_coeficiente_a(d1, d2, v):
    """
    Calcula el coeficiente A de la ecuación cónica.
    
    Args:
        d1, d2: Dígitos del RUT
        v: Variable auxiliar del dígito verificador
    
    Returns:
        float: Coeficiente A = (d1 + d2) / v
    """
    return (d1 + d2) / v
```

### Manejo de errores:
```python
try:
    resultado = operacion_matematica()
except ValueError as e:
    print(f"Error en cálculo: {e}")
except ZeroDivisionError:
    print("Error: División por cero")
```

---

## 6. HITOS Y CRONOGRAMA

| Fase | Descripción | Entregable |
|------|-------------|-----------|
| 1 | Fundamento matemático | Documentación de la lógica |
| 2 | Desarrollo del programa | Código fuente funcional |
| 3 | Desarrollo profesional | Repositorio GitHub actualizado |
| 4 | Casos de prueba | RUTs de prueba, gráficos |
| 5 | Defensa oral | Presentación grupal |
| 6 | Funciones por tramos | Módulo completo integrado |

---

## 7. RECURSOS Y REFERENCIAS

### Matemáticas:
- Secciones cónicas: ecuación general → forma canónica
- Límites laterales y continuidad
- Tipos de discontinuidad
- Transformaciones algebraicas

### Documentación:
- [Algoritmo Módulo 11 (RUT Chile)](https://www.sii.cl/)
- Python Documentation
- GitHub Best Practices

### Herramientas útiles (verificación):
- Wolfram Alpha (para verificar cálculos)
- GeoGebra (para visualizar cónicas)
- Desmos (para graficar funciones)

---

## 8. CHECKLIST FINAL DE ENTREGA

### Antes de la defensa, verificar:

- [ ] **RUT Validado:** Algoritmo módulo 11 correcto
- [ ] **Ecuación General:** Calculada paso a paso, mostrada correctamente
- [ ] **Clasificación:** Identificada correctamente (círculo, elipse, hipérbola, parábola)
- [ ] **Forma Canónica:** Transformación completa y justificada
- [ ] **Gráfica:** Matemáticamente correcta y coherente
- [ ] **Interfaz:** Limpia, intuitiva, sin campos vacíos pre-completados
- [ ] **Funciones por Tramos:** Módulo funcional con análisis de límites y discontinuidades
- [ ] **Código:** Modular, documentado, nombres significativos
- [ ] **GitHub:** Actualizado, 3+ commits por integrante
- [ ] **Código de Ética:** Documento redactado y firmado por el equipo
- [ ] **Defensa:** Todos preparados para explicar su código

---

## 9. NOTAS IMPORTANTES

⚠️ **El proyecto representa el 25% de la calificación final.**

⚠️ **Grupos de exactamente 3 integrantes, sin excepciones.**

⚠️ **La calificación es grupal.** Si un integrante no puede explicar su parte, afecta a todos.

⚠️ **GitHub es obligatorio.** Sin evidencia de colaboración (commits), se puede penalizar.

⚠️ **Todos los cálculos deben ser manuales.** El uso de librerías matemáticas resulta en penalización.

⚠️ **La defensa es aleatoria.** Cualquier integrante puede ser seleccionado para responder cualquier pregunta.

---

## 10. CONTACTO Y DUDAS

- **Profesor:** Equipo docente MAT1186
- **Repositorio central:** GitHub del curso
- **Formato entrega:** Código fuente + enlace repositorio GitHub
- **Fecha límite:** La informada por el equipo docente

---

**Última actualización:** Versión 2026 - Higueras, N. Oyarzo, F.

*Este documento es una guía de referencia para todo el equipo. Manténlo actualizado en el repositorio.*