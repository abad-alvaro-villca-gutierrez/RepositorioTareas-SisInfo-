import tkinter as tk
from tkinter import ttk
from entregaEstudiante import abrir_vista_entrega_estudiante
from config.conexion_bd import traer_tareas

def abrir_panel_alumno():
    ventana = tk.Toplevel()
    ventana.title("Mi Repositorio - Estudiante")
    ventana.state('zoomed')
    ventana.configure(bg="#f4f6f9", padx=30, pady=30)

    tk.Label(ventana, text="Mis Tareas Pendientes", font=("Arial", 20, "bold"), bg="#f4f6f9").pack(pady=(0, 20))

    # Lista de tareas publicadas
    frame_lista = tk.Frame(ventana, bg="white", padx=10, pady=10)
    frame_lista.pack(fill="both", expand=True)

    tareas = traer_tareas()
    # Filtrar solo las que están 'Publicada'
    tareas_publicas = [t for t in tareas if t[4] == "Publicada"]

    if not tareas_publicas:
        tk.Label(frame_lista, text="No hay tareas publicadas por ahora.", bg="white").pack()
    else:
        for t in tareas_publicas:
            card = tk.Frame(frame_lista, bg="#ffffff", highlightbackground="#e0e0e0", highlightthickness=1)
            card.pack(fill="x", pady=5, ipady=10, padx=5)
            
            tk.Label(card, text=t[1], font=("Arial", 12, "bold"), bg="white").pack(side="left", padx=20)
            tk.Label(card, text=f"Vence: {t[3]}", bg="white", fg="#666").pack(side="left", padx=20)
            
            tk.Button(card, text="📤 Subir Entrega", bg="#28a745", fg="white", 
                      command=abrir_vista_entrega_estudiante).pack(side="right", padx=20)