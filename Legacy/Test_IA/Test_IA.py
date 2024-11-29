import pandas as pd
import joblib  # Para cargar el modelo y label encoder
import xgboost as xgb

# 1. Cargar el modelo y el label encoder guardado
xg_model_loaded = joblib.load('xgboost_model.pkl')  # Modelo XGBoost guardado
label_encoder = joblib.load('label_encoder.pkl')  # LabelEncoder guardado

# 2. Función para hacer la predicción con los datos de un DataFrame
def predict_battery_type(df):
    # Hacer la predicción para cada fila del DataFrame usando XGBoost
    predictions = xg_model_loaded.predict(df)
    
    # Decodificar las predicciones a las etiquetas originales
    predicted_battery_types = label_encoder.inverse_transform(predictions)
    
    return predicted_battery_types

# 3. Cargar los datos desde el archivo CSV
file_path = 'Battery_Dataset_example.csv'  # Asegúrate de que este archivo esté en la misma carpeta
df = pd.read_csv(file_path)

# Asegúrate de que solo las columnas necesarias estén presentes
columns_needed = ['initial_voltage', 'slope_initial', 'area_curve', 'time_to_1_4v', 'max_voltage']
df = df[columns_needed]

# 4. Hacer las predicciones para todo el conjunto de datos
predictions = predict_battery_type(df)

# 5. Añadir la columna de predicciones al DataFrame original
df['predicted_battery_type'] = predictions

# 6. Mostrar los resultados
print("\nResultados de las predicciones:")
print(df[['initial_voltage', 'slope_initial', 'area_curve', 'time_to_1_4v', 'max_voltage', 'predicted_battery_type']])

# Si deseas guardar los resultados con las predicciones en un nuevo archivo CSV:
df.to_csv('predictions_output.csv', index=False)
