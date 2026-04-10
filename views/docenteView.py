import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from formularioTarea import abrir_formulario_tarea
from config.conexion_bd import traer_tareas
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

    # Tabla de Tareas (Treeview)
    tabla_frame = tk.Frame(ventana)
    tabla_frame.pack(fill="both", expand=True)

    columnas = ("ID", "Título", "Puntaje", "Vencimiento", "Estado")
    tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")
    
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)

    tabla.pack(fill="both", expand=True)

    # Cargar datos de la BD
    tareas = traer_tareas()
    for t in tareas:
        tabla.insert("", "end", values=t)