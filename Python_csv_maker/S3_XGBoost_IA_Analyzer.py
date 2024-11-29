import pandas as pd
import joblib  # Para cargar el modelo y el label encoder
import xgboost as xgb

# 1. Cargar el modelo y el label encoder guardado
# Nota: Asegúrate de que los archivos 'xgboost_model.pkl' y 'label_encoder.pkl' existan en la misma carpeta que este script
xg_model_loaded = joblib.load('xgboost_model.pkl')  # Modelo XGBoost guardado
label_encoder = joblib.load('label_encoder.pkl')  # LabelEncoder guardado

# 2. Función para hacer la predicción con los datos de un DataFrame
def predict_battery_type(df):
    # Hacer la predicción usando el modelo cargado
    predictions = xg_model_loaded.predict(df)
    
    # Decodificar las predicciones a las etiquetas originales usando el LabelEncoder cargado
    predicted_battery_types = label_encoder.inverse_transform(predictions.astype(int))
    
    return predicted_battery_types

# 3. Cargar los datos desde el dataset generado por el script anterior
file_path = 'dataset_analizado.csv'  # Este es el archivo generado previamente
df = pd.read_csv(file_path)

# Asegúrate de que solo las columnas necesarias estén presentes
columns_needed = ['initial_voltage', 'slope_initial', 'area_curve', 'time_to_1_4v', 'max_voltage']
df = df[columns_needed]

# 4. Agregar la identificación de las pilas (Pila 1, Pila 2, Pila 3, etc.)
df['pila_id'] = ['Pila {}'.format(i + 1) for i in range(len(df))]

# 5. Hacer las predicciones para todo el conjunto de datos
predictions = predict_battery_type(df[columns_needed])

# 6. Añadir la columna de predicciones al DataFrame original
df['predicted_battery_type'] = predictions

# 7. Mostrar los resultados
print("\nResultados de las predicciones:")
print(df[['pila_id', 'initial_voltage', 'slope_initial', 'area_curve', 'time_to_1_4v', 'max_voltage', 'predicted_battery_type']])

# 8. Guardar los resultados con las predicciones en un nuevo archivo CSV
output_file = 'predictions_output_with_ids.csv'
df.to_csv(output_file, index=False)
print(f"\nLos resultados se han guardado en '{output_file}'")
