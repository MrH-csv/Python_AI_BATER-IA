import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import subprocess
import threading
import os
import time

# Lista de scripts en orden de ejecución y su tiempo estimado en segundos
script_sequence = [
    ("S0_Starter.py", 5),
    ("S1_CSV_Maker.py", 30),
    ("S2_Dataset_maker.py", 10),
    ("S4_XGBoost_IA_Analyzer.py", 10),
    ("S5_Serial_Sender.py", 5)
]

# Función para ejecutar scripts secuencialmente con barra de progreso
def ejecutar_todos_los_scripts():
    def run_all_scripts():
        total_scripts = len(script_sequence)
        progress_step = 100 / total_scripts  # Incremento de progreso por script
        progress_bar["value"] = 0  # Reiniciar la barra de progreso
        monitor_text.delete(1.0, tk.END)  # Limpiar el monitor de texto

        for script_name, est_time in script_sequence:
            try:
                # Verificar si el archivo del script existe
                if not os.path.exists(script_name):
                    monitor_text.insert(tk.END, "Error: El archivo {} no existe.\n".format(script_name))
                    monitor_text.see(tk.END)
                    messagebox.showerror("Error", "El archivo {} no existe.".format(script_name))
                    return

                # Mostrar mensaje inicial
                monitor_text.insert(tk.END, "Ejecutando {} (estimado {} segundos)...\n".format(script_name, est_time))
                monitor_text.see(tk.END)

                # Ejecutar el script y capturar salida en tiempo real
                process = subprocess.Popen(
                    ["python", script_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

                start_time = time.time()
                elapsed_time = 0
                while process.poll() is None:  # Mientras el proceso esté activo
                    output_line = process.stdout.readline()
                    if output_line:
                        monitor_text.insert(tk.END, output_line.decode("utf-8"))
                        monitor_text.see(tk.END)

                    elapsed_time = time.time() - start_time
                    progress_bar["value"] = min((elapsed_time / est_time) * progress_step, progress_step)
                    root.update_idletasks()
                    time.sleep(0.1)

                # Leer errores después de finalizar
                for line in process.stderr.readlines():
                    monitor_text.insert(tk.END, "Error: {}".format(line.decode("utf-8")))
                    monitor_text.see(tk.END)

                process.stdout.close()
                process.stderr.close()
                process.wait()

                # Verificar el estado final del proceso
                if process.returncode == 0:
                    monitor_text.insert(tk.END, "{} ejecutado correctamente.\n".format(script_name))
                    monitor_text.see(tk.END)
                else:
                    monitor_text.insert(tk.END, "Error: {} terminó con errores.\n".format(script_name))
                    monitor_text.see(tk.END)
                    messagebox.showerror("Error", "{} terminó con errores.".format(script_name))
                    return
            except Exception as e:
                # Reportar cualquier error inesperado
                monitor_text.insert(tk.END, "Error inesperado en {}: {}\n".format(script_name, e))
                monitor_text.see(tk.END)
                messagebox.showerror("Error", "Error inesperado en {}: {}".format(script_name, e))
                return

            # Actualizar la barra de progreso para el siguiente script
            progress_bar["value"] += progress_step
            root.update_idletasks()

        # Mensaje al completar todos los scripts
        progress_bar["value"] = 100  # Completar barra de progreso
        messagebox.showinfo("Éxito", "Todos los scripts se ejecutaron correctamente.")
        monitor_text.insert(tk.END, "Ejecución de todos los scripts completada.\n")
        monitor_text.see(tk.END)

    # Ejecutar en un hilo separado para no bloquear la interfaz
    thread = threading.Thread(target=run_all_scripts)
    thread.daemon = True
    thread.start()

# Pantalla del proceso de reciclaje con la funcionalidad de ejecutar scripts
def show_recycling_screen():
    for widget in root.winfo_children():
        widget.destroy()

    recycling_label = tk.Label(root, text="Proceso de Reciclaje", font=("Arial", 28, "bold"), fg="white", bg="#2196F3")
    recycling_label.pack(fill=tk.X, pady=10)

    global monitor_text, progress_bar
    monitor_text = scrolledtext.ScrolledText(root, font=("Arial", 16), wrap=tk.WORD, height=8)
    monitor_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
    progress_bar.pack(pady=20)

    button_frame = tk.Frame(root)
    button_frame.pack(fill=tk.BOTH, expand=True, pady=20)

    start_button = tk.Button(button_frame, text="Iniciar Proceso", font=("Arial", 20, "bold"), bg="#FFEB3B", fg="black", command=ejecutar_todos_los_scripts)
    start_button.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=20, expand=True)

    back_button = tk.Button(button_frame, text="Volver al Inicio", font=("Arial", 20, "bold"), bg="#9E9E9E", fg="white", command=show_home)
    back_button.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=20, expand=True)

# Pantalla de inicio
def show_home():
    for widget in root.winfo_children():
        widget.destroy()

    welcome_label = tk.Label(root, text="¡Bienvenido a BATER-IA!", font=("Arial", 28, "bold"), fg="white", bg="#4CAF50")
    welcome_label.pack(fill=tk.X, pady=10)

    button_frame = tk.Frame(root, bg="#E8F5E9")
    button_frame.pack(fill=tk.BOTH, expand=True, pady=20)

    start_btn = tk.Button(button_frame, text="Iniciar Proceso de Reciclaje", font=("Arial", 24, "bold"), bg="#8BC34A", fg="white", command=show_recycling_screen)
    start_btn.pack(pady=20, ipadx=20, ipady=20, fill=tk.BOTH, expand=True)

# Configuración de la interfaz principal
root = tk.Tk()
root.title("BATER-IA - Reciclaje Inteligente")
root.geometry("800x480")
root.config(bg="#E8F5E9")

# Mostrar pantalla de inicio
show_home()

# Ejecutar la interfaz gráfica
root.mainloop()
