import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from entregaEstudiante import abrir_vista_entrega_estudiante
from config.conexion_bd import traer_tareas
from rounded_button import RoundedButton
from lista_tareas_sistema import abrir_lista_tareas
from datetime import date

def abrir_panel_alumno():
    ventana = tk.Toplevel()
    ventana.title("Mi Repositorio - Estudiante")
    ventana.state('zoomed')
    ventana.configure(bg="#FFFBF0", padx=30, pady=30)

    # Encabezado con color de la paleta
    frame_header = tk.Frame(ventana, bg="#6D4145", padx=20, pady=20)
    frame_header.pack(fill="x", pady=(0, 20))
    tk.Label(frame_header, text="Mis Tareas Pendientes", font=("Arial", 24, "bold"), 
             bg="#6D4145", fg="#FFEFAE").pack(anchor="w")
    tk.Label(frame_header, text="Selecciona una tarea para adjuntar tu archivo", font=("Arial", 11), 
             bg="#6D4145", fg="#F5F1E8").pack(anchor="w", pady=(5, 0))

    # Indicador de información importante
    frame_info = tk.Frame(ventana, bg="#96D1AA", padx=15, pady=12)
    frame_info.pack(fill="x", pady=(0, 20))
    tk.Label(frame_info, text="📋 Extensiones permitidas: PDF, DOC, DOCX, ZIP, RAR, PNG, JPG | Tamaño máximo: 5 MB", 
             font=("Arial", 10), bg="#96D1AA", fg="#2D4A3E").pack()

    # Botón de subida rápida (siempre disponible)
    RoundedButton(ventana, text="📤 Subir Entrega", bg="#555832", fg="#FFEFAE", 
                  command=abrir_vista_entrega_estudiante, font=("Arial", 12, "bold"),
                  activebackground="#6D4145", activeforeground="#FFEFAE", padx=20, pady=12,
                  cursor="hand2").pack(pady=(0, 20))
    RoundedButton(ventana, text="📋 VER TAREAS", bg="#FFEFAE", fg="#555832",
              command=abrir_lista_tareas, font=("Arial", 12, "bold"),
              activebackground="#FFE589", activeforeground="#555832", padx=20, pady=12,
              cursor="hand2").pack(pady=(0, 20))

    # Lista de tareas publicadas
    frame_lista = tk.Frame(ventana, bg="#F5F1E8")
    frame_lista.pack(fill="both", expand=True, padx=5, pady=5)

    tareas = traer_tareas()
    # Filtrar solo las que están 'Publicada'
    tareas_publicas = [t for t in tareas if t[4] == "Publicada"]

    if not tareas_publicas:
        tk.Label(frame_lista, text="No hay tareas publicadas por ahora.", bg="#F5F1E8", 
                 font=("Arial", 12), fg="#666").pack(pady=40)
    else:
        for t in tareas_publicas:
            card = tk.Frame(frame_lista, bg="#FFFFFF", highlightbackground="#96D1AA", highlightthickness=2)
            card.pack(fill="x", pady=8, ipady=15, padx=8)
            
            # Contenedor izquierdo con info de la tarea
            frame_info_tarea = tk.Frame(card, bg="#FFFFFF")
            frame_info_tarea.pack(side="left", padx=20, fill="both", expand=True)
            
            tk.Label(frame_info_tarea, text=t[1], font=("Arial", 13, "bold"), 
                     bg="#FFFFFF", fg="#6D4145").pack(anchor="w")
            tk.Label(frame_info_tarea, text=f"Descripción: {t[2] if len(t) > 2 and t[2] else 'Sin descripción'}", 
                     font=("Arial", 10), bg="#FFFFFF", fg="#555").pack(anchor="w", pady=(3, 0))
            tk.Label(frame_info_tarea, text=f"Vence: {t[3]}", font=("Arial", 10, "bold"), 
                     bg="#FFFFFF", fg="#555832").pack(anchor="w", pady=(3, 0))
            
            # Botón de subir
           # RoundedButton(card, text="📤 Subir Entrega", bg="#FFEFAE", fg="#555832", 
                        #  command=abrir_vista_entrega_estudiante, font=("Arial", 11, "bold"),
                        #  activebackground="#FFE589", activeforeground="#555832", padx=15, pady=10,
                       #   cursor="hand2").pack(side="right", padx=20)
            # Bloqueo condicional por fecha límite
            hoy = date.today()
            fecha_limite = t[3].date() if hasattr(t[3], 'date') else t[3]

            if fecha_limite < hoy:
                 RoundedButton(card, text="🔒 Plazo Vencido", bg="#cfcfcf", fg="#888888",
                  command=lambda: None, font=("Arial", 11, "bold"),
                  activebackground="#cfcfcf", activeforeground="#888888", padx=15, pady=10,
                  cursor="arrow").pack(side="right", padx=20)
            else:
                 RoundedButton(card, text="📤 Subir Entrega", bg="#FFEFAE", fg="#555832",
                  command=abrir_vista_entrega_estudiante, font=("Arial", 11, "bold"),
                  activebackground="#FFE589", activeforeground="#555832", padx=15, pady=10,
                  cursor="hand2").pack(side="right", padx=20)
            