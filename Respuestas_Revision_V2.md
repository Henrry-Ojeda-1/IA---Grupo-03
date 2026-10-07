# Matriz de Resolución de Observaciones (Revisión V2)
**Proyecto:** PIML E030 (Machine Learning Físicamente Informado)

Este documento estructura las respuestas formales a la retroalimentación recibida, respondiendo directamente a cada punto del revisor y detallando las acciones implementadas en el código para subsanarlos.

---

## PARTE I: FEEDBACK GENERAL

### 1. Falta de Código EDA y Reproducibilidad (T2)
**Observación exacta del revisor:** 
> *"Pero la T2 pedía un EDA ejecutado en Python, y el repositorio no tiene código ni figuras. Solo hay dos .docx, el CSV y el README. El informe afirma resultados (...) que no se pueden verificar porque no hay notebook, gráficos ni números. Tampoco está el script que genera el dataset, así que el proceso no es reproducible."*

**Respuesta y Acción Implementada:**
Se acepta la observación de acuerdo a las reglas de investigación reproducible (*Sandve et al., 2013*). En la revisión anterior hubo una omisión en la subida de los archivos. 
* **Acción:** Se ha consolidado todo el proyecto en un enfoque monolítico. El repositorio cuenta ahora con el cuaderno maestro **`PIML_E030.ipynb`** que contiene el código completo y ejecutable de inicio a fin. Este cuaderno incluye toda la fase exploratoria (EDA), mostrando explícitamente la matriz de correlación térmica, la depuración de datos, y los gráficos de resultados (SHAP, distancias ordinales y regresión), haciendo el proceso 100% reproducible.

### 2. Tratamiento de Redundancias (Colinealidad)
**Observación exacta del revisor:** 
> *"Hay redundancias que deben tratar antes de interpretar SHAP o PCA: la zona y el factor Z son la misma información, igual que el tipo de suelo y el factor S, y el número de pisos y la altura tienen r = 0.99."*

**Respuesta y Acción Implementada:**
Observación matemáticamente certera. La inclusión de variables colineales distorsiona la varianza en el PCA y fragmenta artificialmente la importancia de variables en el análisis SHAP.
* **Acción:** Se implementó una purga estricta en el Jupyter Notebook (`PIML_E030.ipynb`). Las variables de texto redundantes (`Zona`, `Suelo`) fueron excluidas a favor de sus valores numéricos (`Factor_Z`, `Factor_S`). Asimismo, la variable `N_Pisos` fue eliminada de la lista de características independientes, dejando únicamente la `Altura_Total_H_m`, ya que es la variable mecánicamente activa en las fórmulas de la E.030.

---

## PARTE II: PREGUNTAS PARA LA SUSTENTACIÓN

### Pregunta 1: Definición del Índice de Peligrosidad
**Pregunta exacta del revisor:** 
> *"¿Cómo se define exactamente Indice_Peligrosidad? Si es una regla determinista, ¿qué aporta un clasificador que la aprende con 80% de exactitud frente a aplicar la regla directamente?"*

**Respuesta Formal:**
El *Índice de Peligrosidad* es efectivamente una etiqueta determinista basada en el Ratio de Deriva inelástica y la penalización por resonancia (cercanía a $T_p$). 
**El aporte del clasificador es el Triage Estructural Conceptual:** Aplicar la regla determinista requiere construir el modelo, calcular masas, rigideces, ejecutar el análisis modal espectral, y extraer el periodo, cortantes y derivas. El modelo de Machine Learning (XGBoost) permite inferir esa misma categoría de vulnerabilidad utilizando **exclusivamente variables de pre-dimensionamiento** (Zona, Suelo, Altura, Uso) *sin ejecutar el cálculo dinámico computacional*. Esto reduce el análisis a latencias de milisegundos para fases tempranas de diseño urbano.

### Pregunta 2: Script Generador y Realismo de Datos
**Pregunta exacta del revisor:** 
> *"¿Dónde está el código que generó el dataset? ¿De qué distribuciones salen los periodos, los pesos y la densidad de muros? ¿Son realistas para edificios peruanos?"*

**Respuesta Formal:**
* **Acción:** El notebook generador se adjuntará al repositorio para cumplir con la reproducibilidad. 
Las distribuciones se definieron usando heurísticas de la práctica peruana:
- Las alturas se limitaron a rangos comerciales (2 a 20 pisos). 
- Los pesos se estimaron usando metrados típicos de la norma E.020 (aprox. 1 tonelada por metro cuadrado por piso). 
- El Periodo ($T$) **se re-calculó empíricamente** en esta iteración del proyecto para asegurar el realismo físico, utilizando la ecuación fundamental de la E.030 acoplada al índice de rigidez lateral del edificio: $T = H / (35 + 20 \times \text{Ratio})$, forzando así el cumplimiento estricto de los coeficientes $C_T$ (35 para pórticos, 45 dual, 60 muros).

### Pregunta 3: Circularidad de la Regresión Simbólica
**Pregunta exacta del revisor:** 
> *"Si la regresión simbólica 'redescubre' Sa = ZUCS/R, ¿es un hallazgo o simplemente están recuperando la ecuación que ustedes mismos usaron para generar los datos? ¿Cómo lo presentarían sin caer en un argumento circular?"*

**Respuesta Formal:**
No se presenta como un descubrimiento físico nuevo, sino como una **Prueba de Concepto (Proof of Concept) en IA Explicable (XAI)**.
Bajo el paradigma de *Veridical Data Science*, el hallazgo es validar que algoritmos como PySR (*Cranmer, 2023*) poseen la madurez matemática para reconstruir leyes físicas algebraicas a partir de pura estadística observacional ruidosa. Usar un dataset sintético donde la fórmula original es conocida sirve como "terreno de pruebas" irrefutable. Al demostrar que el método es exitoso aquí, se certifica su validez para usarlo a futuro sobre daños empíricos reales (o simulaciones FEM no lineales) donde la ecuación subyacente es desconocida.

### Pregunta 4: Discrepancia de Clases
**Pregunta exacta del revisor:** 
> *"¿Por qué el README y el informe reportan conteos de clases distintos? ¿Cuál es la versión válida del dataset?"*

**Respuesta Formal:**
Esta discrepancia ocurrió por un rezago en la documentación de una versión preliminar de los datos. 
* **Acción:** La versión oficial es el `dataset_e030_v2.csv` alojado actualmente en el repositorio, cuyos conteos son: Bajo (1108), Medio (575), Alto (676) y Crítico (141). Se ha auditado el `README.md` actual y el Jupyter Notebook para confirmar que ambas fuentes reportan estas cifras unificadas.

### Pregunta 5: Asimetría de Falsos Negativos (Riesgo Crítico)
**Pregunta exacta del revisor:** 
> *"¿Qué tan grave es para ustedes un falso negativo en la clase Crítico frente a un falso positivo? ¿Cómo se refleja eso en la métrica que eligieron?"*

**Respuesta Formal:**
Un Falso Negativo en la clase "Crítico" (clasificar como "Bajo" un edificio que en realidad está cerca del colapso) es un error catastrófico que implica riesgo de pérdida de vidas humanas. Un Falso Positivo (sobredimensionar el riesgo) solo genera sobrecostos de revisión estructural.
* **Acción:** Por ello, se abandonó la métrica de *Exactitud (Accuracy)* global. Se adoptó una **Clasificación Ordinal** (*Frank & Hall, 2001*) donde se mide la "Distancia de Error". El clasificador fue diseñado y evaluado para priorizar asimétricamente el **Recall de la clase 3 (Crítico)**, garantizando que el modelo sea adverso al riesgo y minimice a cero las fallas catastróficas.
