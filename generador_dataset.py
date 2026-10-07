import pandas as pd
import numpy as np

def generar_dataset(n_samples=2500, output_file='dataset_e030_v2.csv'):
    np.random.seed(42)
    
    # Parámetros Norma E.030
    zonas = [('Z1', 0.10), ('Z2', 0.25), ('Z3', 0.35), ('Z4', 0.45)]
    suelos = [('S0', 0.8), ('S1', 1.0), ('S2', 1.05), ('S3', 1.20)]
    usos = [('A (Esencial)', 1.5), ('B (Importante)', 1.3), ('C (Comun)', 1.0)]
    sistemas = [
        ('Porticos RC', 8), ('Dual RC', 7), ('Muros RC', 6), 
        ('Albañileria_Confinada', 3), ('Porticos_Especiales_Acero', 8)
    ]
    
    data = []
    
    for _ in range(n_samples):
        z_str, z_val = zonas[np.random.randint(0, len(zonas))]
        s_str, s_val = suelos[np.random.randint(0, len(suelos))]
        u_str, u_val = usos[np.random.randint(0, len(usos))]
        
        sysx_str, rx_val = sistemas[np.random.randint(0, len(sistemas))]
        sysy_str, ry_val = sistemas[np.random.randint(0, len(sistemas))]
        
        # Filtro físico básico (no acero con albañilería)
        while (sysx_str == 'Albañileria_Confinada' and sysy_str == 'Porticos_Especiales_Acero') or \
              (sysy_str == 'Albañileria_Confinada' and sysx_str == 'Porticos_Especiales_Acero'):
            sysy_str, ry_val = sistemas[np.random.randint(0, len(sistemas))]
            
        n_pisos = np.random.randint(2, 21)
        h = n_pisos * np.random.uniform(2.8, 3.2)
        area = np.random.uniform(150, 1500)
        peso = n_pisos * area * np.random.uniform(0.9, 1.1)  # Aprox 1 ton/m2/piso
        
        ratio_muros = np.random.uniform(0.5, 4.0)
        
        # Periodos empíricos
        c_t = 35 + 20 * ratio_muros
        t_x = h / c_t * np.random.uniform(0.9, 1.1)
        t_y = h / c_t * np.random.uniform(0.9, 1.1)
        
        tp, tl = 0.6, 2.0  # Simplificado para S2
        if s_str == 'S3': tp, tl = 1.0, 1.6
            
        # Simulación de respuesta dinámica (para etiqueta)
        cx = 2.5 * (tp / t_x) if t_x > tp else 2.5
        cx = min(cx, 2.5)
        
        sa_x = (z_val * u_val * cx * s_val) * 9.81
        vx = sa_x * peso / (rx_val * 9.81)
        
        # Deriva sintética proporcional a la aceleración espectral y flexibilidad
        deriva_x = (sa_x / 9.81) * (t_x**2) * 0.005 / rx_val
        limite_deriva = 0.007
        ratio_deriva = deriva_x / limite_deriva
        
        # Etiqueta de peligrosidad
        dif_tp = abs(t_x - tp) / tp * 100
        
        if ratio_deriva > 1.0 and dif_tp < 50:
            peligro = "Critico"
        elif ratio_deriva > 0.8:
            peligro = "Alto"
        elif ratio_deriva > 0.5:
            peligro = "Medio"
        else:
            peligro = "Bajo"
            
        data.append([
            z_str, z_val, s_str, s_val, tp, tl, u_str, u_val,
            sysx_str, rx_val, sysy_str, ry_val, 1.0, 1.0, rx_val, ry_val, 9.81,
            n_pisos, h, area, peso, ratio_muros, t_x, t_y, cx, cx, sa_x, sa_x,
            vx, vx, vx/peso, vx/peso, deriva_x, limite_deriva, ratio_deriva, dif_tp, peligro
        ])
        
    cols = [
        'Zona_Sismica_Z', 'Factor_Z', 'Tipo_Suelo_S', 'Factor_S', 'Periodo_Tp_s', 'Periodo_TL_s', 
        'Categoria_Uso', 'Factor_Uso_U', 'Sistema_Estructural_X', 'R0_X', 'Sistema_Estructural_Y', 'R0_Y', 
        'Irregularidad_Altura_Ia', 'Irregularidad_Planta_Ip', 'Factor_R_X', 'Factor_R_Y', 'Gravedad_g_m_s2', 
        'N_Pisos', 'Altura_Total_H_m', 'Area_Planta_m2', 'Peso_Total_P_Ton', 'Ratio_Area_Muros_pct', 
        'Periodo_Tx_s', 'Periodo_Ty_s', 'Factor_Cx', 'Factor_Cy', 'Sa_X_m_s2', 'Sa_Y_m_s2', 
        'Cortante_Basal_Vx_Ton', 'Cortante_Basal_Vy_Ton', 'Ratio_Vx_P', 'Ratio_Vy_P', 
        'Deriva_Inelastica_Max_X', 'Limite_Deriva_E030', 'Ratio_Deriva_Limite', 'Diferencia_Resonancia_Tp_pct', 'Indice_Peligrosidad'
    ]
    
    df = pd.DataFrame(data, columns=cols)
    print("Dataset Generado. Distribución de Peligrosidad:")
    print(df['Indice_Peligrosidad'].value_counts())
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    generar_dataset(2500, 'dataset_e030_v2.csv')
