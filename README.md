# IA---Grupo-03
## Objetivo 
Este repositorio implementa un marco de Aprendizaje Automático diseñado para predecir demandas sísmicas dinámicas y clasificar la vulnerabilidad estructural en edificaciones de concreto armado, albañilería y estructuras de acero en el Perú. Desarrollado estrictamente bajo la Norma Técnica E.030 de Diseño Sismorresistente del Reglamento Nacional de Edificaciones (RNE), el proyecto une la mecánica computacional con el aprendizaje estadístico.
Mediante una arquitectura supervisada de dos etapas combinada con descubrimiento no supervisado de dimensionalidad (PCA y K-Means), este modelo evita la alta latencia computacional de los análisis dinámicos no lineales (tiempo-historia o pushover). 

## Paso a Paso para Ejecutar el Proyecto.: flujo de trabajo en 4 etapas
Paso 1: Generación del Dataset Sintético Paramétrico 
Paso 2: Análisis Exploratorio y No Supervisado (EDA + PCA + Clustering)
Paso 3: Entrenamiento Supervisado de Modelos
Paso 4: Validación de Estabilidad (PCS) y Repositorio

Dataset Sintético Realizado.

Distribución de Clases de Peligrosidad**:
	Bajo**: 1,108 casos (44.32%)
	Medio**: 575 casos (23.00%)
	Alto**: 676 casos (27.04%)
	Critico**: 141 casos (5.64%)


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
