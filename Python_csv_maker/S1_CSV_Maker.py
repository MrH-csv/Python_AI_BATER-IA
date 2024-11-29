import serial
import csv
import re
import time  # Importa la biblioteca para manejar el tiempo

# Configuración del puerto serial
SERIAL_PORT = 'COM4'  # Cambia esto al puerto serial correcto
BAUD_RATE = 9600  # Ajusta según la configuración de tu dispositivo

# Archivo de salida
OUTPUT_FILE = 'datos_pilas.csv'

# Tiempo máximo de ejecución en segundos
TIEMPO_EJECUCION = 30

# Inicializa el puerto serial
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Conectado al puerto {SERIAL_PORT}")
except serial.SerialException as e:
    print(f"Error al conectar al puerto {SERIAL_PORT}: {e}")
    exit()

# Función para validar líneas que contienen solo números separados por comas
def es_linea_valida(linea):
    # Verifica si la línea es de la forma "número, número, número, número"
    patron = r'^(\d+(\.\d+)?(,\s*\d+(\.\d+)?)*$)'
    return re.match(patron, linea.strip()) is not None

# Escribe datos en el archivo CSV
try:
    with open(OUTPUT_FILE, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Escribe el encabezado
        csv_writer.writerow(['Tiempo (S)', 'Pila 1 (V)', 'Pila 2 (V)', 'Pila 3 (V)'])
        print("Esperando datos del puerto serial...")

        # Registra el tiempo inicial
        tiempo_inicial = time.time()

        while True:
            # Calcula el tiempo transcurrido
            tiempo_transcurrido = time.time() - tiempo_inicial

            if tiempo_transcurrido >= TIEMPO_EJECUCION:
                print(f"Tiempo de ejecución ({TIEMPO_EJECUCION} segundos) completado.")
                break

            try:
                # Lee una línea del puerto serial
                line = ser.readline().decode('utf-8').strip()
                if line:
                    print(f"Recibido: {line}")
                    if es_linea_valida(line):
                        datos = line.split(',')
                        csv_writer.writerow(datos)
                        print(f"Escrito en CSV: {datos}")
                    else:
                        print("Línea descartada: no contiene datos válidos.")
            except Exception as e:
                print(f"Error al procesar datos: {e}")
finally:
    ser.close()
    print("Puerto serial cerrado.")
    print(f"Archivo CSV guardado como '{OUTPUT_FILE}'.")
