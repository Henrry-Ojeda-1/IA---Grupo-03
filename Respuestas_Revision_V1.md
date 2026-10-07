# Matriz de Resolución de Observaciones y Plan de Acción (Revisión V1)
**Proyecto:** PIML E030 (Machine Learning Físicamente Informado)

Este documento registra los comentarios de la primera auditoría técnica del proyecto y las acciones correctivas fundamentales que dieron origen a la actual arquitectura del código y al "Camino B".

---

## 1. Naturaleza Sintética de los Datos
> **Comentario:** *"El texto habla de 'una base de datos compuesta por información de edificios reales', pero el dataset es sintético. Hay que corregir la redacción."*

**Respuesta y Acción Tomada:**
Se procedió a actualizar inmediatamente toda la documentación (`README.md` y `PIML_E030.html`) para declarar de forma transparente que el dataset es **100% sintético paramétrico** (un *Surrogate Model* de la Norma E.030). Se argumentó que esto es una ventaja para probar algoritmos de IA Explicable en un entorno controlado antes de escalar a ensayos reales.

---

## 2. Fuga de Información (Data Leakage)
> **Comentario:** *"Las variables de demanda son fórmulas exactas. Si alguna de estas columnas entra como variable de entrada, el modelo simplemente aprende la norma... Ratio_Deriva_Limite, Deriva_Inelastica_Max_X no pueden ser entradas del clasificador, porque sería fuga de información."*

**Respuesta y Acción Tomada:**
Esta fue la observación más crítica. Se modificó el Jupyter Notebook estableciendo una lista estricta llamada `columnas_independientes`. Se **purgaron** del set de entrenamiento todas las variables dependientes o derivadas de las fórmulas (Derivas, Cortantes Basales, Pseudoaceleraciones). El modelo XGBoost y el análisis PCA pasaron a entrenarse única y exclusivamente con variables de diseño primarias (Zona, Suelo, Altura, Geometría, Uso).

---

## 3. Discrepancia de Clases
> **Comentario:** *"Inconsistencia en la distribución de clases. El README reporta Bajo 1214 / Crítico 189. El CSV del repositorio tiene Bajo 1108 / Crítico 141. ¿Cuál es la versión final?"*

**Respuesta y Acción Tomada:**
Se validó que el archivo `dataset_e030_v2.csv` alojado en el repositorio era la fuente de la verdad (1108, 575, 676, 141). Se actualizó el `README.md` borrando los valores antiguos de la iteración v1 y emparejándolos con los del archivo final.

---

## 4. Combinaciones Físicamente Irreales
> **Comentario:** *"Aparecen 7 edificios con estructura metálica en X y albañilería confinada en Y... Recomiendo restringir el muestreo a combinaciones que existen en la práctica."*

**Respuesta y Acción Tomada:**
Se implementó un filtro de **Depuración Física** en la Fase 1 del cuaderno de Jupyter. Usando `pandas`, se programaron máscaras booleanas que eliminan automáticamente del dataset cualquier combinación incompatible (ej. Acero combinado con Albañilería), asegurando la coherencia estructural de los datos procesados.

---

## 5. Recálculo Físico del Periodo Fundamental ($T$)
> **Comentario:** *"La relación T/H está coherente, pero la correlación entre periodo y porcentaje de muros es débil (-0.18), cuando físicamente debería ser más fuerte."*

**Respuesta y Acción Tomada:**
Para devolverle la coherencia dinámica a los datos, se implementó en código una **re-asignación matemática del Periodo**. En el cuaderno de Jupyter se forzó el cálculo $T = H / (35 + 20 \times \text{Ratio de Muros})$. Esto garantizó que edificios sin muros (pórticos) tuvieran un denominador de 35 (flexibles) y edificios con alta densidad de muros alcanzaran un denominador cercano a 60 (rígidos), cumpliendo estrictamente con los $C_T$ de la E.030.

---

## 6. Adopción del "Camino B" (IA Explicable y Regresión Simbólica)
> **Comentario:** *"Camino B: mantener el dataset, pero reformular la pregunta. Conviertan la limitación en el experimento: ¿puede el ML redescubrir la E.030 a partir de los datos? Usen regresión simbólica con PySR (Cranmer, 2023) y SHAP (Mangalathu et al, 2020)."*

**Respuesta y Acción Tomada:**
Se adoptó oficialmente este pivote metodológico. Se integró el ecosistema `shap` en el Jupyter Notebook para dibujar gráficos de interacción y probar que la IA dedujo la relación entre Factor Z y Rigidez sin decírselo. Además, se integró el motor matemático en Julia mediante `PySR` para ejecutar algoritmos evolutivos que logran derivar algebraicamente la fórmula del cortante $V = ZUCSP/R$.

---

## 7. Clasificador Ordinal y Foco en Riesgo Crítico
> **Comentario:** *"Tratar la clasificación como ordinal y reportar el desempeño en la clase Crítico."*

**Respuesta y Acción Tomada:**
El problema dejó de tratarse como clasificación nominal y se forzó un mapeo jerárquico (`Bajo=0 < Medio=1 < Alto=2 < Critico=3`). Se implementaron métricas de **Distancia de Error Ordinal**, garantizando la penalización asimétrica de los **Falsos Negativos** (predecir como seguro un edificio Crítico) y reportando el *Recall* y *F1-Score* específicos para esta clase catastrófica.
