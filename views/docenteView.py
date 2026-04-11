import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from formularioTarea import abrir_formulario_tarea
from config.conexion_bd import traer_tareas
from evaluacionDocente import abrir_evaluacion_docente
from rounded_button import RoundedButton
def abrir_panel_docente():
    ventana = tk.Toplevel()
    ventana.title("Panel de Control - Docente")
    ventana.state('zoomed')
    ventana.configure(bg="#f4f6f9", padx=30, pady=30)

    # Header
    header = tk.Frame(ventana, bg="#f4f6f9")
    header.pack(fill="x", pady=(0, 20))

    tk.Label(header, text="Gestión de Tareas", font=("Arial", 20, "bold"), bg="#f4f6f9").pack(side="left")
    
    RoundedButton(header, text="➕ Crear Nueva Tarea", bg="#0052cc", fg="white", 
                  font=("Arial", 10, "bold"), padx=15, pady=8, command=abrir_formulario_tarea).pack(side="right")

    tk.Button(header, text="Calificar Tareas", bg="#28a745", fg="white",
              font=("Arial", 10, "bold"), padx=12, pady=8,
              command=lambda: abrir_evaluacion_docente(ventana)).pack(side="right", padx=(0, 8))

    # Tabla de Tareas (Treeview)
    tabla_frame = tk.Frame(ventana)
    tabla_frame.pack(fill="both", expand=True)

    # 1. Quitamos "ID" de las columnas
    columnas = ("Título", "Puntaje", "Vencimiento", "Estado")
    tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")
    
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150, anchor="center") # Centramos para que se vea mejor

    tabla.pack(fill="both", expand=True)

    # 2. Cargar datos de la BD filtrando el ID
    tareas = traer_tareas()
    for t in tareas:
        # t[1:] significa: "toma desde el segundo elemento hasta el final"
        # Esto ignora el t[0] que es el ID de la base de datos
        tabla.insert("", "end", values=t[1:])