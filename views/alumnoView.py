import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sys
import os
from datetime import date

# Configuración de rutas para importaciones
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from entregaEstudiante import abrir_vista_entrega_estudiante
from notificacionesAlumno import abrir_notificaciones_alumno
from config.conexion_bd import traer_tareas
from rounded_button import RoundedButton
from lista_tareas_sistema import abrir_lista_tareas

def abrir_notificaciones_con_id(ventana_padre):
    """Solicita el ID del alumno y abre la ventana de notificaciones (T5.4)."""
    id_alumno = simpledialog.askstring("Mis Notificaciones", 
                                       "Ingresa tu ID de alumno:",
                                       parent=ventana_padre)
    if id_alumno and id_alumno.strip():
        try:
            int(id_alumno.strip())  # Validar que sea número
            abrir_notificaciones_alumno(int(id_alumno.strip()))
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número válido")

def abrir_panel_alumno():
    ventana = tk.Toplevel()
    ventana.title("Mi Repositorio - Estudiante")
    ventana.state('zoomed')
    ventana.configure(bg="#FFFBF0", padx=30, pady=30)

    # --- ENCABEZADO ---
    frame_header = tk.Frame(ventana, bg="#6D4145", padx=25, pady=25)
    frame_header.pack(fill="x", pady=(0, 20))
    
    tk.Label(frame_header, text="Mis Tareas Pendientes", font=("Segoe UI", 26, "bold"), 
             bg="#6D4145", fg="#FFEFAE").pack(anchor="w")
    tk.Label(frame_header, text="Selecciona una tarea para adjuntar tu archivo", font=("Segoe UI", 11), 
             bg="#6D4145", fg="#F5F1E8").pack(anchor="w", pady=(5, 0))

    # --- INDICADOR DE INFORMACIÓN ---
    frame_info = tk.Frame(ventana, bg="#96D1AA", padx=15, pady=12)
    frame_info.pack(fill="x", pady=(0, 20))
    tk.Label(frame_info, text="📋 Extensiones permitidas: PDF, DOCX, ZIP, JPG | Tamaño máximo: 5 MB", 
             font=("Segoe UI", 10, "bold"), bg="#96D1AA", fg="#2D4A3E").pack()

    # --- BOTONES DE ACCIÓN SUPERIOR ---
    frame_acciones = tk.Frame(ventana, bg="#FFFBF0")
    frame_acciones.pack(fill="x", pady=(0, 10))

    RoundedButton(frame_acciones, text="📤 Subir Entrega Rápida", bg="#555832", fg="#FFEFAE", 
                  command=abrir_vista_entrega_estudiante, font=("Segoe UI", 11, "bold"),
                  padx=20, pady=10).pack(side="left", padx=5)

    RoundedButton(frame_acciones, text="📋 VER TODAS LAS TAREAS", bg="#FFEFAE", fg="#555832",
                  command=abrir_lista_tareas, font=("Segoe UI", 11, "bold"),
                  padx=20, pady=10).pack(side="left", padx=5)

    RoundedButton(frame_acciones, text="🔔 MIS NOTIFICACIONES", bg="#96D1AA", fg="#2D4A3E",
                  command=lambda: abrir_notificaciones_con_id(ventana), font=("Segoe UI", 11, "bold"),
                  padx=20, pady=10).pack(side="left", padx=5)

    # --- LISTA DE TAREAS CON SCROLL ---
    container_canvas = tk.Frame(ventana, bg="#F5F1E8")
    container_canvas.pack(fill="both", expand=True)

    canvas = tk.Canvas(container_canvas, bg="#F5F1E8", highlightthickness=0)
    scrollbar = ttk.Scrollbar(container_canvas, orient="vertical", command=canvas.yview)
    frame_lista = tk.Frame(canvas, bg="#F5F1E8")

    def actualizar_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    window_id = canvas.create_window((0, 0), window=frame_lista, anchor="nw")

    def ajustar_ancho_frame(event):
        canvas.itemconfig(window_id, width=event.width)

    frame_lista.bind("<Configure>", actualizar_scrollregion)
    canvas.bind("<Configure>", ajustar_ancho_frame)
    canvas.configure(yscrollcommand=scrollbar.set)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # --- CARGA DE DATOS ---
    tareas = traer_tareas()
    
    # Filtramos solo las tareas con estado "Publicada" (el estado está en t[5])
    tareas_publicas = [t for t in tareas if len(t) > 5 and t[5] == "Publicada"]

    if not tareas_publicas:
        tk.Label(frame_lista, text="No hay tareas publicadas por ahora. ✨", bg="#F5F1E8", 
                 font=("Segoe UI", 14), fg="#6D4145").pack(pady=60)
    else:
        for t in tareas_publicas:
            # MAPEO CORRECTO EN BASE A LA CONSULTA SQL ACTUAL
            # [0: id_tarea, 1: nombre_tarea, 2: descripcion, 3: puntaje, 4: estado, 5: fecha_vencimiento]
            nombre_tarea = t[1]
            descripcion  = t[2]
            puntaje      = t[3]
            fecha_bd     = t[4]
            
            hoy = date.today()
            
            # Nos aseguramos de que lo que venga de BD se trate como fecha pura
            fecha_limite = fecha_bd.date() if hasattr(fecha_bd, 'date') else fecha_bd
            
            # Verificación de seguridad por si alguna fecha en BD es Nula
            if isinstance(fecha_limite, date):
                esta_vencida = fecha_limite < hoy
            else:
                esta_vencida = False
                
            color_acento = "#FF5252" if esta_vencida else "#96D1AA"

            # --- CARD ---
            card = tk.Frame(frame_lista, bg="#FFFFFF", highlightbackground="#E0DBCF", highlightthickness=1)
            card.pack(fill="x", pady=10, padx=20)

            tk.Frame(card, bg=color_acento, width=8).pack(side="left", fill="y")

            info_container = tk.Frame(card, bg="#FFFFFF", padx=20, pady=15)
            info_container.pack(side="left", fill="both", expand=True)

            header_card = tk.Frame(info_container, bg="#FFFFFF")
            header_card.pack(fill="x")

            tk.Label(header_card, text=nombre_tarea, font=("Segoe UI", 15, "bold"), 
                     bg="#FFFFFF", fg="#6D4145").pack(side="left")
            
            tk.Label(header_card, text=f"Puntos: {puntaje}", font=("Segoe UI", 10, "bold"), 
                     bg="#FFEFAE", fg="#555832", padx=10).pack(side="right")
            
            tk.Label(info_container, text=descripcion, font=("Segoe UI", 10), 
                     bg="#FFFFFF", fg="#555", wraplength=700, justify="left").pack(anchor="w", pady=(5, 5))

            footer = tk.Frame(info_container, bg="#FFFFFF")
            footer.pack(fill="x", pady=(5, 0))

            vence_color = "#C62828" if esta_vencida else "#555832"
            vence_icono = "⚠️" if esta_vencida else "📅"

            tk.Label(footer, text=f"{vence_icono} Vence: {fecha_limite}", 
                     font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg=vence_color).pack(side="left")

            if esta_vencida:
                RoundedButton(card, text="🔒 Plazo Vencido", bg="#EEEEEE", fg="#9E9E9E",
                              command=lambda: None, font=("Segoe UI", 10, "bold"),
                              padx=15, pady=8).pack(side="right", padx=20)
            else:
                RoundedButton(card, text="📤 Subir Entrega", bg="#FFEFAE", fg="#555832",
                              command=abrir_vista_entrega_estudiante, font=("Segoe UI", 10, "bold"),
                              activebackground="#FFE589", activeforeground="#555832",
                              padx=15, pady=8, cursor="hand2").pack(side="right", padx=20)

    ventana.protocol("WM_DELETE_WINDOW", lambda: [canvas.unbind_all("<MouseWheel>"), ventana.destroy()])