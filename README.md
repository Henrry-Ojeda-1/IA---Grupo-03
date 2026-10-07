# PIML E030 (Physics-Informed ML)

![Build Status](https://img.shields.io/badge/Status-Completed-success)
![Framework](https://img.shields.io/badge/Framework-Physics--Informed%20ML-blue)
![Code Standard](https://img.shields.io/badge/Norma-Peruvian%20E.030%20RNE-red)

---

## 🇪🇸 Versión en Español

### 1. Resumen Ejecutivo y Visión General
Este repositorio implementa un **marco de Aprendizaje Automático Físicamente Informado (PIML)** diseñado para predecir vulnerabilidades estructurales en edificaciones de concreto armado, albañilería y acero estructural en el Perú. Desarrollado bajo la **Norma Técnica E.030 (RNE)**, el proyecto une la mecánica computacional empírica con la Inteligencia Artificial Explicable (XAI).

Este repositorio garantiza la **reproducibilidad computacional** (*Sandve et al., 2013*). Todo el pipeline (desde el EDA exploratorio hasta la regresión simbólica) está integrado y es ejecutable en un único Cuaderno Jupyter Maestro (`PIML_E030.ipynb`), demostrando un flujo de trabajo transparente y libre de colinealidades.

---

### 2. Dataset Paramétrico y Prevención de Fuga de Información (`dataset_e030_v2.csv`)
Se cuenta con un dataset **100% sintético** de **2,500 configuraciones** (un *Surrogate Model* de la Norma E.030). El uso de un entorno sintético controlado permite validar los algoritmos de XAI matemáticamente antes de escalar a daños reales. La distribución oficial final es: Bajo (1108), Medio (575), Alto (676) y Crítico (141).

**Regla Determinista del Índice de Peligrosidad:**
La etiqueta objetivo (`Indice_Peligrosidad`) proviene de una regla determinista basada en el ratio de la deriva frente al límite normativo y la penalización por resonancia espectral. 
*¿Qué aporta entonces el Machine Learning?* Permite realizar un **Triage Estructural Conceptual**: inferir el riesgo de un edificio utilizando exclusivamente variables iniciales de arquitectura (Zona, Suelo, Altura, Uso) *sin necesidad de construir el modelo computacional ni ejecutar el análisis modal espectral*. Para garantizar la validez científica y evitar *Data Leakage*, **se eliminaron todas las variables derivadas de los inputs (Derivas, Cortantes, Pseudoaceleraciones)**. El modelo infiere la física oculta.

---

### 3. Metodología de Machine Learning (El "Camino B")

#### 3.1. Tratamiento de Colinealidad y Análisis No Supervisado (PCA y K-Means)
Antes del modelado, se eliminaron redundancias perfectas (ej. manteniendo `Factor_Z` y eliminando la etiqueta de texto `Zona_Sismica`; manteniendo la `Altura` en lugar de `N_Pisos` dado que $r \approx 0.99$).
* **PCA**: Se proyectó el espacio de características de diseño a componentes principales puras.
* **K-Means ($K=4$)**: Demostró empíricamente que la IA puede encontrar fronteras de agrupamiento naturales que coinciden asombrosamente con la severidad del daño, sin conocer las etiquetas.

#### 3.2. Clasificación Ordinal (XGBoost)
Dado que la severidad estructural tiene un orden inherente (`Bajo < Medio < Alto < Crítico`), se enmarcó el problema matemáticamente como **Clasificación Ordinal** (*Frank & Hall, 2001*). 
Se prioriza métricas asimétricas focalizadas en la clase **Crítico** (que representa un 5.6% de la muestra). Un Falso Negativo en esta clase (predecir como seguro un edificio inestable) es catastrófico, por lo que el *Recall* y la Distancia de Error Ordinal son los verdaderos validadores del algoritmo, superando a la exactitud (accuracy) global.

#### 3.3. Inteligencia Artificial Explicable (SHAP)
*Lundberg & Lee (2017), Mangalathu et al. (2020)*
En lugar de aceptar una "caja negra", se extraen los **Valores de Shapley**. El gráfico de dependencia revela que el modelo XGBoost descubrió autónomamente interacciones no lineales críticas (como la relación entre el Factor Z de peligro sísmico y el Índice de Rigidez Global del edificio).

#### 3.4. Regresión Simbólica con PySR (Proof of Concept)
Se emplearon algoritmos evolutivos genéticos mediante **PySR** (*Cranmer, 2023*) impulsados por *Julia*.
El objetivo de que la IA "redescubra" la ecuación $V = \frac{ZUCS}{R} P$ a partir de los datos no es un argumento circular, sino una **Prueba de Concepto (Proof of Concept)** en el paradigma de Predictabilidad (*Veridical Data Science*). Demuestra fehacientemente que el algoritmo tiene la capacidad matemática de abstraer y deducir leyes físicas subyacentes complejas puramente desde la observación estadística.

---

### 📂 Estructura del Repositorio
```text
PIML_E030/
├── README.md                           # Documentación oficial y respuestas a revisión
├── dataset_e030_v2.csv                 # Dataset paramétrico depurado (2500 casos)
├── PIML_E030.ipynb                     # Cuaderno Jupyter Maestro (Pipeline Camino B / EDA / Código fuente)
└── PIML_E030.html                      # Dashboard interactivo UI del proyecto
```

### 📦 Archivos Finales de Entrega
Para garantizar una revisión exhaustiva y reproducible, la entrega consta de la siguiente estructura alojada en la raíz del repositorio:

1. **`README.md`**: Este documento de presentación y defensa técnica.
2. **`PIML_E030.ipynb`**: El Cuaderno Jupyter maestro que contiene todo el código Python, desde el EDA hasta la Regresión Simbólica.
3. **`dataset_e030_v2.csv`**: El dataset paramétrico sintético con las 2,500 edificaciones evaluadas.
4. **`generador_dataset.py`**: El script fuente en Python que generó paramétricamente el dataset, garantizando la trazabilidad de los datos.
5. **`PIML_E030.html`**: El Dashboard interactivo web (diagrama de flujo) con los resultados y gráficos embebidos.
6. **`Respuestas_Revision_V1.md`** y **`Respuestas_Revision_V2.md`**: Matrices formales de respuesta y acción frente al feedback de los revisores.
7. **`figuras_jupyter/`** (Carpeta): Contiene las 7 gráficas de alta resolución extraídas automáticamente del cuaderno (SHAP, Matrices de Confusión, K-Means, etc.).
