import serial  # Biblioteca para comunicación serial
import time    # Biblioteca para manejar tiempos de espera

# Configuración del puerto serial
SERIAL_PORT = 'COM4'  # Cambia esto por el puerto donde está conectado tu Arduino
BAUD_RATE = 9600      # Velocidad en baudios del Arduino

# Valor que se enviará por serial
START_SIGNAL = 99

try:
    # Abrir el puerto serial
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print("Conectado al puerto {}".format(SERIAL_PORT))
    time.sleep(2)  # Esperar a que el Arduino esté listo

    # Enviar el número entero
    ser.write("{}\n".format(START_SIGNAL).encode())
    print("Enviado por serial: {}".format(START_SIGNAL))

except serial.SerialException as e:
    print("Error al conectar al puerto serial: {}".format(e))
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Puerto serial cerrado.")
