import pandas as pd
import numpy as np

# Configuración: Ruta de los archivos y parámetros ajustables
input_file = "datos_pilas.csv"  # Cambia este nombre si el archivo tiene otro nombre
output_file = "dataset_analizado.csv"
initial_time_window = 10  # Duración en segundos para calcular el slope inicial

# Cargar el archivo CSV
data = pd.read_csv(input_file)

# Procesar datos para generar el dataset
processed_data = []

# Asume que la primera columna es "Tiempo (S)" y las demás son los voltajes de las pilas
time_column = data.columns[0]
voltage_columns = data.columns[1:]

for pila_num, voltage_column in enumerate(voltage_columns, start=1):
    # Filtrar datos de la pila actual
    tiempo = data[time_column].to_numpy()
    voltajes = data[voltage_column].to_numpy()

    # 1. Voltaje inicial
    initial_voltage = voltajes[0]

    # 2. Slope inicial (pendiente)
    time_mask = tiempo <= initial_time_window
    if np.any(time_mask):
        slope_initial = np.polyfit(tiempo[time_mask], voltajes[time_mask], 1)[0]  # Pendiente de la recta
    else:
        slope_initial = np.nan

    # 3. Área bajo la curva usando una aproximación trapezoidal sin `scipy`
    area_curve = sum(
        (voltajes[i] + voltajes[i + 1]) / 2 * (tiempo[i + 1] - tiempo[i])
        for i in range(len(tiempo) - 1)
    )

    # 4. Tiempo hasta alcanzar 1.4V
    try:
        time_to_1_4v = tiempo[np.argmax(voltajes >= 1.4)]
    except ValueError:
        time_to_1_4v = np.nan  # Si nunca alcanza 1.4V

    # 5. Voltaje máximo alcanzado
    max_voltage = np.max(voltajes)

    # Añadir al dataset
    processed_data.append([pila_num, initial_voltage, slope_initial, area_curve, time_to_1_4v, max_voltage])

# Crear DataFrame final
columns = ["numero_de_pila", "initial_voltage", "slope_initial", "area_curve", "time_to_1_4v", "max_voltage"]
dataset = pd.DataFrame(processed_data, columns=columns)

# Guardar el dataset en un archivo CSV
dataset.to_csv(output_file, index=False)

print(f"El dataset ha sido generado y guardado como '{output_file}'")
