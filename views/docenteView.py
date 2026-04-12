import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from formularioTarea import abrir_formulario_tarea
from config.conexion_bd import traer_tareas
from evaluacionDocente import abrir_evaluacion_docente
from rounded_button import RoundedButton
from controllers.alertas_docente import verificar_alertas_docente

def abrir_panel_docente():
    ventana = tk.Toplevel()
    ventana.title("Panel de Control - Docente")
    ventana.state('zoomed')
    # Fondo principal
    ventana.configure(bg="#ffefae", padx=30, pady=30) 
    
    # Header
    header = tk.Frame(ventana, bg="#ffefae")
    header.pack(fill="x", pady=(0, 20))

    tk.Label(header, text="Gestión de Tareas", font=("Arial", 20, "bold"), bg="#ffefae", fg="#6d4145").pack(side="left")
    
    # Botón Crear Tarea (Relacionado a US-1)
    RoundedButton(header, text="➕ Crear Nueva Tarea", bg="#96d1aa", fg="#555832", 
                  font=("Arial", 10, "bold"), padx=15, pady=8, command=abrir_formulario_tarea).pack(side="right")

    # Botón Calificar Entrega (Relacionado a US-5)
    RoundedButton(header, text="Calificar Entrega", bg="#555832", fg="#ffefae",
                  font=("Arial", 10, "bold"), padx=12, pady=8,
                  command=lambda: abrir_evaluacion_docente(ventana)).pack(side="right", padx=(0, 8))

    # Estilos de la tabla (Treeview)
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", 
                    background="#ffffff",
                    foreground="#6d4145",
                    rowheight=25,
                    fieldbackground="#ffffff")
    
    style.configure("Treeview.Heading", 
                    background="#6d4145", 
                    foreground="#ffefae", 
                    font=('Arial', 10, 'bold'))
    
    style.map('Treeview', background=[('selected', '#96d1aa')], foreground=[('selected', '#555832')])

    # Tabla de Tareas
    tabla_frame = tk.Frame(ventana, bg="#ffefae")
    tabla_frame.pack(fill="both", expand=True)

    columnas = ("Título", "Puntaje", "Vencimiento", "Estado")
    tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", style="Treeview")
    
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150, anchor="center")

    tabla.pack(fill="both", expand=True)

    # Cargar datos de la BD (Relacionado a US-1 / Ver tareas creadas)
    tareas = traer_tareas()
    for t in tareas:
        nombre = t[1]
        puntaje = t[3]
        fecha = t[5]
        estado = t[4]
        
        tabla.insert("", "end", values=(nombre, puntaje, fecha, estado))

    # --- UBICACIÓN CORRECTA DE LA ALERTA ---
    ventana.after(600, verificar_alertas_docente)