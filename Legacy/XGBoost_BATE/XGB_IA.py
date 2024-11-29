# Importar las librerías necesarias
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
from sklearn.metrics import classification_report, accuracy_score
import joblib  # Librería para guardar y cargar el modelo

# 1. Cargar el archivo CSV con los datos
file_path = 'Final_Extended_Battery_Dataset.csv'  # Cambia este path a donde tienes tu archivo CSV
df = pd.read_csv(file_path)

# Mostrar las primeras filas para ver la estructura de los datos
print("Primeras filas del dataset:")
print(df.head())

# 2. Preprocesar los datos
# Codificar la columna 'battery_type' a valores numéricos
label_encoder = LabelEncoder()
df['battery_type_encoded'] = label_encoder.fit_transform(df['battery_type'])

# Mostrar las primeras filas después de la codificación
print("\nDataset después de codificar 'battery_type':")
print(df.head())

# 3. Separar las características (X) y la variable objetivo (y)
X = df.drop(columns=['battery_type', 'battery_type_encoded'])  # Características
y = df['battery_type_encoded']  # Variable objetivo

# 4. Dividir los datos en conjunto de entrenamiento y conjunto de prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Verificar el tamaño de los conjuntos
print(f"\nTamaño del conjunto de entrenamiento: {X_train.shape[0]}")
print(f"Tamaño del conjunto de prueba: {X_test.shape[0]}")

# 5. Crear el modelo de XGBoost
xg_model = xgb.XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='mlogloss')

# Entrenar el modelo con el conjunto de entrenamiento
xg_model.fit(X_train, y_train)

# 6. Hacer predicciones con el conjunto de prueba
y_pred = xg_model.predict(X_test)

# 7. Evaluar el modelo
accuracy = accuracy_score(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

# Mostrar los resultados de la evaluación
print("\nPrecisión del modelo:", accuracy)
print("\nReporte de clasificación:")
print(class_report)

# 8. Guardar el modelo entrenado y el LabelEncoder
joblib.dump(xg_model, 'xgboost_model.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')  # Guardar el LabelEncoder
print("\nModelo guardado como 'xgboost_model.pkl'")
print("LabelEncoder guardado como 'label_encoder.pkl'")
