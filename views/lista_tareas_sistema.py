import tkinter as tk
from tkinter import ttk
from datetime import datetime, date
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.conexion_bd import traer_alumnos, traer_tareas_pendientes
from rounded_button import RoundedButton


def abrir_lista_tareas():
    ventana = tk.Toplevel()
    ventana.title("Todas las Tareas pendientes")
    ventana.state('zoomed')
   # ventana.configure(bg="#FFFBF0", padx=20, pady=20)
    ventana.geometry("250x200")
    # ==========================================
    # ENCABEZADO
    # ==========================================
    frame_header = tk.Frame(ventana, bg="#555832", padx=25, pady=25)
    frame_header.pack(fill="x", pady=(0, 20))
    
    tk.Label(frame_header, text="Tareas Pendientes ", font=("Segoe UI", 26, "bold"), 
             bg="#555832", fg="#FFEFAE").pack(anchor="w")
    tk.Label(frame_header, text="Selecciona un alumno para ver sus tareas pendientes", font=("Segoe UI", 11), 
             bg="#555832", fg="#F5F1E8").pack(anchor="w", pady=(5, 0))

    # ==========================================
    # SECCIÓN: SELECCIÓN DE ALUMNO
    # ==========================================
    frame_seleccion = tk.Frame(ventana, bg="#96D1AA", padx=20, pady=15)
    frame_seleccion.pack(fill="x", pady=(0, 20))

    label_alumno = tk.Label(frame_seleccion, text="👤 Seleccionar Alumno:", font=("Segoe UI", 12, "bold"), 
                            bg="#96D1AA", fg="#2D4A3E")
    label_alumno.pack(anchor="w", pady=(0, 10))

    # Obtener lista de alumnos
    alumnos = traer_alumnos()
    lista_alumnos = [(str(alumno[0]), alumno[1]) for alumno in alumnos]

    # Variable para guardar el alumno seleccionado
    alumno_seleccionado = tk.StringVar()

    # Crear Combobox (desplegable)
    estilo_combo = ttk.Style()
    estilo_combo.theme_use('clam')
    estilo_combo.configure('TCombobox', font=("Segoe UI", 11), fieldbackground="#FFFBF0", background="#FFFBF0")
    
    combo_alumnos = ttk.Combobox(
        frame_seleccion,
        textvariable=alumno_seleccionado,
        values=[nombre for _, nombre in lista_alumnos],
        state="readonly",
        width=45,
        font=("Segoe UI", 11),
        style='TCombobox'
    )
    combo_alumnos.pack(fill="x", padx=0, pady=0)
    combo_alumnos.bind("<<ComboboxSelected>>", lambda event: on_alumno_seleccionado(event, lista_alumnos, frame_tareas, frame_contenido_tareas))

    # ==========================================
    # SECCIÓN: TAREAS PENDIENTES
    # ==========================================
    label_tareas = tk.Label(ventana, text="📋 Tareas Pendientes:", font=("Segoe UI", 14, "bold"), 
                            bg="#6d4145", fg="#FFFBF0")
    label_tareas.pack(anchor="w", padx=20, pady=(20, 10))

    # Frame con scroll para las tareas
    frame_tareas_container = tk.Frame(ventana, bg="#FFFBF0")
    frame_tareas_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    frame_tareas = tk.Canvas(frame_tareas_container, bg="#FFFBF0", highlightthickness=0)
    scrollbar = ttk.Scrollbar(frame_tareas_container, orient="vertical", command=frame_tareas.yview)
    frame_contenido_tareas = tk.Frame(frame_tareas, bg="#FFFBF0")

    frame_tareas.create_window((0, 0), window=frame_contenido_tareas, anchor="nw")
    frame_tareas.configure(yscrollcommand=scrollbar.set)

    def on_frame_configure(event):
        frame_tareas.configure(scrollregion=frame_tareas.bbox("all"))
    
    frame_contenido_tareas.bind("<Configure>", on_frame_configure)

    def _on_mousewheel(event):
        frame_tareas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    frame_tareas.bind_all("<MouseWheel>", _on_mousewheel)

    frame_tareas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Guardar referencias globales
    frame_tareas.frame_contenido_tareas = frame_contenido_tareas

    # Mensaje inicial
    tk.Label(frame_contenido_tareas, text="Selecciona un alumno para ver sus tareas pendientes", 
            bg="#F5F1E8", font=("Segoe UI", 12, "italic"), fg="#999").pack(pady=40)


def on_alumno_seleccionado(event, lista_alumnos, canvas, frame_contenido):
    """Callback cuando se selecciona un alumno"""
    combo = event.widget
    nombre_seleccionado = combo.get()
    
    # Encontrar el id_alumno correspondiente
    id_alumno = None
    for id_al, nombre in lista_alumnos:
        if nombre == nombre_seleccionado:
            id_alumno = id_al
            break
    
    if id_alumno is None:
        return
    
    # Limpiar el frame anterior
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    # Obtener tareas pendientes
    tareas_pendientes = traer_tareas_pendientes(int(id_alumno))
    
    if not tareas_pendientes:
        tk.Label(frame_contenido, text="✓ El alumno ha entregado todas las tareas", 
                font=("Segoe UI", 13, "bold"), bg="#F5F1E8", fg="#2D4A3E").pack(pady=40)
        return
    
    hoy = date.today()
    
    # Mostrar cada tarea en un card
    for tarea in tareas_pendientes:
        id_tarea, nombre, descripcion, puntaje, fecha_vencimiento, estado = tarea
        
        # Convertir fecha
        fecha_limite = fecha_vencimiento.date() if hasattr(fecha_vencimiento, 'date') else fecha_vencimiento
        
        # Verificar si está vencida
        if isinstance(fecha_limite, date):
            esta_vencida = fecha_limite < hoy
        else:
            esta_vencida = False
        
        color_acento = "#FF5252" if esta_vencida else "#96D1AA"
        
        # ===== CARD =====
        card = tk.Frame(frame_contenido, bg="#FFFFFF", highlightbackground="#E0DBCF", highlightthickness=1)
        card.pack(fill="x", pady=10, padx=10)
        
        # Barra lateral de color
        tk.Frame(card, bg=color_acento, width=8).pack(side="left", fill="y")
        
        # Contenedor de información
        info_container = tk.Frame(card, bg="#FFFFFF", padx=20, pady=15)
        info_container.pack(side="left", fill="both", expand=True)
        
        # Header del card
        header_card = tk.Frame(info_container, bg="#FFFFFF")
        header_card.pack(fill="x", pady=(0, 8))
        
        tk.Label(header_card, text=nombre, font=("Segoe UI", 15, "bold"), 
                bg="#FFFFFF", fg="#6D4145").pack(side="left")
        
        tk.Label(header_card, text=f"Puntos: {puntaje}", font=("Segoe UI", 10, "bold"), 
                bg="#FFEFAE", fg="#555832", padx=10, pady=3).pack(side="right")
        
        # Descripción
        if descripcion:
            tk.Label(info_container, text=descripcion, font=("Segoe UI", 10), 
                    bg="#FFFFFF", fg="#555555", wraplength=700, justify="left").pack(anchor="w", pady=(0, 8))
        
        # Footer con fecha
        footer = tk.Frame(info_container, bg="#FFFFFF")
        footer.pack(fill="x", pady=(8, 0))
        
        vence_color = "#C62828" if esta_vencida else "#555832"
        vence_icono = "⚠️" if esta_vencida else "📅"
        
        tk.Label(footer, text=f"{vence_icono} Vence: {fecha_limite}", 
                font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg=vence_color).pack(side="left")
