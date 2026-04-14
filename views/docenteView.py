import tkinter as tk
from tkinter import ttk
import sys
import os
import threading
import time

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# ⚠️ Asegúrate de que las rutas a tus archivos sean las correctas
from controllers.alertas_docente import verificar_alertas_docente
from services.servicio_correo import enviar_reporte_docente
from config.conexion_bd import traer_tareas
from formularioTarea import abrir_formulario_tarea
from evaluacionDocente import abrir_evaluacion_docente
from rounded_button import RoundedButton

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
        fecha = t[4]
        estado = t[5]
        
        tabla.insert("", "end", values=(nombre, puntaje, fecha, estado))

    # --- UBICACIÓN CORRECTA DE LA ALERTA VISUAL ---
    # Esto ejecuta la función a los 600 milisegundos de abrirse la ventana
    ventana.after(600, verificar_alertas_docente)

    # ==========================================
    # BLOQUE DE ENVÍO DE CORREO AUTOMÁTICO EN SEGUNDO PLANO
    # ==========================================
    
    # ⚠️ IMPORTANTE: Aquí debes poner el correo real del docente.
    correo_del_docente = "correo_del_docente@gmail.com"

    def tarea_enviar_correo():
        """
        Función que corre de fondo. Usamos un 'while True' para que sea 
        constante, y 'time.sleep' para no colapsar la computadora.
        """
        while True:
            try:
                # Ejecutamos la función que se conecta a Gmail
                exito = enviar_reporte_docente(correo_del_docente)
                
                if exito:
                    print("✅ Notificación de fondo: Correo de reporte enviado al docente.")
                else:
                    print("ℹ️ Notificación de fondo: No se envió correo (no hay tareas nuevas o falló la conexión).")
                    
            except Exception as e:
                print(f"❌ Error inesperado en el hilo de correo: {e}")
            
            # Pausamos el hilo por 60 segundos antes de volver a revisar la BD
            # (Si quieres que revise cada hora, cambia el 60 por 3600)
            time.sleep(60)

    # Creamos el Hilo y lo iniciamos
    hilo_correo = threading.Thread(target=tarea_enviar_correo, daemon=True)
    hilo_correo.start()