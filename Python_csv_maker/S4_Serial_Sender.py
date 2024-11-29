import pandas as pd
import serial  # Biblioteca para comunicación serial

# Configuración del puerto serial
SERIAL_PORT = 'COM4'  # Cambia esto por el puerto donde está conectado tu Arduino
BAUD_RATE = 9600  # Velocidad en baudios del Arduino

# Mapa base de valores según el tipo de pila con los nuevos identificadores
type_to_serial = {
    "Alkaline (MnO2)": 2,
    "Carbon-Zinc (Zn-MnO2)": 1,
    "Nickel-Cadmium (Ni-Cd)": 3,
    "Nickel-Metal Hydride (Ni-MH)": 4
}

# Cargar el archivo CSV con las predicciones
file_path = 'predictions_output_with_ids.csv'
df = pd.read_csv(file_path)

# Abrir el puerto serial
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print("Conectado al puerto {}".format(SERIAL_PORT))

    for _, row in df.iterrows():
        pila_id = row['pila_id']  # Identificador de la pila (e.g., "Pila 1", "Pila 2", ...)
        battery_type = row['predicted_battery_type']  # Tipo de pila predicho

        # Obtener el número entero asociado al tipo de pila y ajustar según el número de la pila
        pila_numero = int(pila_id.split()[1])  # Extrae el número de la pila (1, 2, 3, ...)
        if battery_type in type_to_serial:
            value_to_send = pila_numero * 10 + type_to_serial[battery_type]
            # Enviar el valor por serial
            ser.write("{}\n".format(value_to_send).encode())
            print("Enviado por serial para {} ({}): {}".format(pila_id, battery_type, value_to_send))
        else:
            print("Tipo de pila desconocido para {}: {}".format(pila_id, battery_type))

except serial.SerialException as e:
    print("Error al conectar al puerto serial: {}".format(e))
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Puerto serial cerrado.")
