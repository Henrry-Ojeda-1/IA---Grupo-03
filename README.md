# IA---Grupo-03
## COMENTARIO IMPORTANTE
Profesor, buenas noches. Queríamos comentarle que hemos decidido cambiar nuestro tema inicial sobre la selección del tipo de cimentación, debido a que la recopilación y el procesamiento de los datos resultan muy extensos para el tiempo limitado del curso. Por ello, hemos optado por desarrollar un modelo de Machine Learning para la estimación de la demanda sísmica y la clasificación del nivel de peligrosidad estructural de edificaciones. Consideramos que este nuevo enfoque es más viable para cumplir con los objetivos y entregables del curso. Agradeceríamos su opinión sobre este cambio. A continuación se detalla:
## Objetivo 
Desarrollar un modelo predictivo basado en algoritmos de Machine Learning para la estimación rápida de la demanda sísmica y la clasificación del nivel de peligrosidad estructural de edificaciones. El modelo empleará como variables de entrada (X) la parametrización de las normativas de diseño sismorresistente (amenaza, zona, sitio) y las características dinámicas intrínsecas de las estructuras, tales como el periodo fundamental y la rigidez aproximada.
## Descripción del problema de ingeniería estructural 
La evaluación de la respuesta sísmica de una edificación exige analizar la interacción entre la amenaza sísmica del emplazamiento y las propiedades dinámicas de la estructura. En el Perú, este procedimiento está regulado por la Norma Técnica E.030 de Diseño Sismorresistente del Reglamento Nacional de Edificaciones (RNE), la cual establece los parámetros de zona (Z), perfil de suelo (S), periodos característicos (Tp y Tl) y factores de amplificación.
Por otro lado, la demanda sísmica que experimentará la estructura (aceleraciones espectrales, fuerzas cortantes y desplazamientos) es altamente dependiente de sus características propias, fundamentalmente su rigidez lateral, distribución de masa y, en consecuencia, su periodo fundamental de vibración. El problema de ingeniería surge ante la necesidad de evaluar el nivel de vulnerabilidad de un portafolio extenso de edificios existentes, o durante la fase de anteproyecto, donde el cálculo detallado de la demanda sísmica para múltiples combinaciones de parámetros normativos y configuraciones geométricas resulta en un proceso iterativo de alto costo computacional y temporal. La falta de correlaciones instantáneas entre la parametrización del código sísmico y la vulnerabilidad del edificio dificulta la identificación temprana de las estructuras con mayor riesgo de daño o colapso.
## Problema específico que se pretende resolver 
El problema específico a abordar es la carencia de una herramienta analítica automatizada que permita identificar de manera inmediata qué edificaciones presentan un mayor nivel de peligrosidad ante un evento sísmico, considerando simultáneamente las condiciones del sitio y la rigidez de la estructura.
La propuesta consiste en implementar algoritmos de aprendizaje supervisado y no supervisado que procesen una base de datos compuesta por información de edificios reales sometidos a diversas condiciones de sitio. El modelo recibirá como parámetros de entrada las variables del código sísmico (zona, tipo de suelo, parámetros de sitio) y los datos geométricos-dinámicos de la estructura (tipo de sistema estructural, alturas, rigidez aproximada). A partir del análisis de estos patrones, la Inteligencia Artificial generará resultados de salida (Y) que indicarán los valores de demanda esperada y clasificarán las edificaciones según su índice de peligrosidad. Esto permitirá a los ingenieros focalizar los análisis detallados y las estrategias de mitigación en aquellos edificios identificados por el algoritmo como los más críticos o vulnerables.


Paso a Paso para Ejecutar el Proyecto.: flujo de trabajo en 4 etapas


Paso 1: Generación del Dataset Sintético Paramétrico 
Paso 2: Análisis Exploratorio y No Supervisado (EDA + PCA + Clustering)
Paso 3: Entrenamiento Supervisado de Modelos
Paso 4: Validación de Estabilidad (PCS) y Repositorio

Dataset Sintético Realizado.

Distribución de Clases de Peligrosidad**:
	Bajo**: 1,214 casos (48.56%)
	Medio**: 573 casos (22.92%)
	Alto**: 524 casos (20.96%)
	Critico**: 189 casos (7.56%)


###  Actualización del Dataset (`dataset_edificaciones_e030-v2.csv`)

#### 1. Amenaza y Sitio
* **`Zona_Sismica_Z`** / **`Factor_Z`**: Zonas 1 a 4 (\\(0.10g, 0.25g, 0.35g, 0.45g\\)).
* **`Tipo_Suelo_S`** / **`Factor_S`**: Perfiles \\(S_0, S_1, S_2, S_3\\) con sus respectivos factores de suelo.
* **`Periodo_Tp_s`** / **`Periodo_TL_s`**: Periodos definitorios de la plataforma espectral.

#### 2. Categoría y Uso
* **`Categoria_Uso`** / **`Factor_Uso_U`**: Edificaciones esenciales \\(A\\) (\\(U=1.5\\)), importantes \\(B\\) (\\(U=1.3\\)) y comunes \\(C\\) (\\(U=1.0\\)).

#### 3. Sistemas Estructurales y Reducción Sísmica por Dirección
* **Dirección X-X**: **`Sistema_Estructural_X`**, **`R0_X`** (Coeficiente básico: Pórticos \\(R_0=8\\), Dual \\(R_0=7\\), Muros \\(R_0=6\\), Albañilería \\(R_0=3\\)) y **`Factor_R_X`**.
* **Dirección Y-Y**: **`Sistema_Estructural_Y`**, **`R0_Y`** y **`Factor_R_Y`**.

#### 4. Factores de Irregularidad y Reducción Efectiva (\\(R\\))
* **`Irregularidad_Altura_Ia`**: Factores \\(I_a \in \{1.00, 0.90, 0.85, 0.75\}\\).
* **`Irregularidad_Planta_Ip`**: Factores \\(I_p \in \{1.00, 0.90, 0.85, 0.75\}\\).
* **Cálculo del Factor Efectivo**: \\(R_X = R_{0,X} \cdot I_a \cdot I_p\\) y \\(R_Y = R_{0,Y} \cdot I_a \cdot I_p\\).

#### 5. Aceleración de la Gravedad y Respuestas Espectrales
* **`Gravedad_g_m_s2`**: Constante \\(g = 9.81\text{ m/s}^2\\).
* **`Periodo_Tx_s`** / **`Periodo_Ty_s`**: Periodos fundamentales de vibración por dirección.
* **`Factor_Cx`** / **`Factor_Cy`**: Factor de amplificación sísmica (tramo constante \\(2.5\\), tramo \\(1/T\\) y tramo \\(1/T^2\\)).
* **`Sa_X_m_s2`** / **`Sa_Y_m_s2`**: Espectro de pseudoaceleración en \\(\text{m/s}^2\\).
* **`Cortante_Basal_Vx_Ton`** / **`Cortante_Basal_Vy_Ton`**: Cortantes basales de diseño.
* **`Deriva_Inelastica_Max_X`** / **`Limite_Deriva_E030`**: Deriva calculada vs. límite permisible (\\(0.007\\) concreto, \\(0.005\\) albañilería, etc.).
* **`Indice_Peligrosidad`**: Clasificación del riesgo (`Bajo`, `Medio`, `Alto`, `Critico`).
