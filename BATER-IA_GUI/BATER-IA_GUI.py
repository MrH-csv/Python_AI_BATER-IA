import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from itertools import cycle

# Variables globales
user_points = 0
total_recycled_batteries = 5000

# Pantalla de inicio
def show_home():
    for widget in root.winfo_children():
        widget.destroy()

    welcome_label = tk.Label(root, text="¡Bienvenido a BATER-IA!", font=("Arial", 28, "bold"), fg="white", bg="#4CAF50")
    welcome_label.pack(fill=tk.X, pady=10)

    button_frame = tk.Frame(root, bg="#E8F5E9")
    button_frame.pack(fill=tk.BOTH, expand=True, pady=20)

    # Botones distribuidos proporcionalmente
    start_btn = tk.Button(button_frame, text="Iniciar Proceso de Reciclaje", font=("Arial", 24, "bold"), bg="#8BC34A", fg="white", command=show_recycling_screen)
    start_btn.pack(pady=20, ipadx=20, ipady=20, fill=tk.BOTH, expand=True)

    stats_btn = tk.Button(button_frame, text="Consultar Estadísticas Ambientales", font=("Arial", 24, "bold"), bg="#03A9F4", fg="white", command=show_stats)
    stats_btn.pack(pady=20, ipadx=20, ipady=20, fill=tk.BOTH, expand=True)

    help_btn = tk.Button(button_frame, text="Ayuda y Más Información", font=("Arial", 24, "bold"), bg="#FF9800", fg="white", command=show_help)
    help_btn.pack(pady=20, ipadx=20, ipady=20, fill=tk.BOTH, expand=True)

    profile_btn = tk.Button(button_frame, text="Registrar Usuario", font=("Arial", 24, "bold"), bg="#FF5722", fg="white", command=show_registration)
    profile_btn.pack(pady=20, ipadx=20, ipady=20, fill=tk.BOTH, expand=True)

# Registro de usuario
def show_registration():
    for widget in root.winfo_children():
        widget.destroy()

    reg_label = tk.Label(root, text="Registra tu Perfil", font=("Arial", 28, "bold"), fg="white", bg="#FF5722")
    reg_label.pack(fill=tk.X, pady=10)

    tk.Label(root, text="Ingresa tu nombre:", font=("Arial", 18), bg="#E8F5E9").pack(pady=10)
    name_entry = tk.Entry(root, font=("Arial", 18), justify="center")
    name_entry.pack(pady=10)

    def save_profile():
        name = name_entry.get()
        if name.strip():
            messagebox.showinfo("Perfil Guardado", f"¡Bienvenido, {name}!")
            show_home()
        else:
            messagebox.showerror("Error", "Por favor ingresa un nombre válido.")

    tk.Button(root, text="Guardar", font=("Arial", 20, "bold"), bg="#4CAF50", fg="white", command=save_profile).pack(pady=20)
    tk.Button(root, text="Volver al Inicio", font=("Arial", 18), bg="#9E9E9E", fg="white", command=show_home).pack(pady=10)

# Pantalla del proceso de reciclaje
def show_recycling_screen():
    for widget in root.winfo_children():
        widget.destroy()

    recycling_label = tk.Label(root, text="Proceso de Reciclaje", font=("Arial", 28, "bold"), fg="white", bg="#2196F3")
    recycling_label.pack(fill=tk.X, pady=10)

    global monitor_text, start_button, confirm_button, animation_label, progress_bar
    monitor_text = scrolledtext.ScrolledText(root, font=("Arial", 16), wrap=tk.WORD, height=8)
    monitor_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    animation_label = tk.Label(root, text="", font=("Arial", 24, "bold"), fg="#4CAF50")
    animation_label.pack(pady=20)

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress_bar.pack(pady=20)

    button_frame = tk.Frame(root)
    button_frame.pack(fill=tk.BOTH, expand=True, pady=20)

    start_button = tk.Button(button_frame, text="Iniciar Análisis", font=("Arial", 20, "bold"), bg="#FFEB3B", fg="black", command=simulate_recycling)
    start_button.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=20, expand=True)

    confirm_button = tk.Button(button_frame, text="Confirmar Reciclaje", font=("Arial", 20, "bold"), bg="#F44336", fg="white", state=tk.DISABLED, command=confirm_recycling)
    confirm_button.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=20, expand=True)

    back_button = tk.Button(button_frame, text="Volver al Inicio", font=("Arial", 20, "bold"), bg="#9E9E9E", fg="white", command=show_home)
    back_button.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=20, expand=True)

# Estadísticas ambientales
def show_stats():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Estadísticas Ambientales", font=("Arial", 28, "bold"), fg="white", bg="#03A9F4").pack(fill=tk.X, pady=10)

    tk.Label(root, text=f"Pilas Recicladas Globalmente: {total_recycled_batteries}", font=("Arial", 20), bg="#E8F5E9").pack(pady=10)
    tk.Label(root, text=f"Tus Puntos Acumulados: {user_points}", font=("Arial", 20), bg="#E8F5E9").pack(pady=10)

    tk.Button(root, text="Volver al Inicio", font=("Arial", 20, "bold"), bg="#9E9E9E", fg="white", command=show_home).pack(pady=20)

# Ayuda e información
def show_help():
    messagebox.showinfo(
        "Ayuda y Más Información",
        "BATER-IA es un sistema diseñado para reciclar pilas AA de forma inteligente.\n"
        "Con cada reciclaje, ayudas a reducir el impacto ambiental.\n"
        "¡Reciclar nunca fue tan fácil!"
    )

# Simulación de reciclaje
def simulate_recycling():
    progress_bar["value"] = 0
    root.update()

    monitor_text.insert(tk.END, "Iniciando análisis de pilas...\n")
    for i in range(1, 101, 10):
        progress_bar["value"] = i
        root.update()
        root.after(300)

    monitor_text.insert(tk.END, "Análisis completado. Pilas clasificadas.\n")
    confirm_button.config(state=tk.NORMAL)

def confirm_recycling():
    global user_points
    user_points += 10  # Gamificación: Suma puntos
    messagebox.showinfo("Reciclaje Completado", "¡Gracias por reciclar! Has ganado 10 puntos.")
    show_home()

# Configuración de la interfaz principal
root = tk.Tk()
root.title("BATER-IA - Reciclaje Inteligente")
root.geometry("800x480")
root.config(bg="#E8F5E9")

# Pantalla inicial
show_home()

# Ejecutar la interfaz
root.mainloop()

