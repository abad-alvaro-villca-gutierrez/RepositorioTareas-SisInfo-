import tkinter as tk
from tkinter import messagebox
import sys
import os

# 1. Configuración de rutas para reconocer las otras carpetas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rounded_button import RoundedButton

# 2. Importamos las funciones necesarias
from config.conexion_bd import guardar_tarea
from controllers.tarea_controladores import validar_tarea

def procesar_formulario(ventana_instancia, estado_elegido="Publicada"):
    """Esta función se ejecuta al hacer clic en los botones de guardado"""
    # 1. Obtener datos de los campos globales
    titulo = entry_titulo.get().strip()
    descripcion = text_descripcion.get("1.0", tk.END).strip()
    puntaje = entry_puntaje.get().strip()
    fecha = entry_fecha.get().strip()

    # 2. VALIDACIÓN: Invocamos al controlador
    es_valido, mensaje = validar_tarea(titulo, fecha, puntaje)

    if not es_valido:
        messagebox.showwarning("Error de Validación", mensaje)
        return 

    # 3. PROCESAMIENTO Y PERSISTENCIA
    try:
        puntaje_int = int(puntaje)
        
        # Guardamos en la Base de Datos usando el estado elegido
        exito = guardar_tarea(titulo, descripcion, puntaje_int, fecha, estado=estado_elegido)

        # 4. Feedback al usuario y cierre
        if exito:
            messagebox.showinfo("Éxito", f"¡La tarea se guardó como {estado_elegido}!")
            # CERRAMOS LA VENTANA AUTOMÁTICAMENTE
            ventana_instancia.destroy() 
        else:
            messagebox.showerror("Error de BD", "Hubo un problema al persistir los datos.")
            
    except Exception as e:
        messagebox.showerror("Error Crítico", f"Ocurrió un error inesperado: {e}")

def abrir_formulario_tarea():
    """Función que dibuja y abre la ventana del formulario"""
    
    # Declaramos globales para que procesar_formulario pueda leer los Entry
    global entry_titulo, text_descripcion, entry_puntaje, entry_fecha

    ventana = tk.Toplevel()
    ventana.title("Crear Tarea - Sistema Educativo")
    ventana.geometry("420x600")
    ventana.configure(bg="#f8f9fa", padx=30, pady=25)
    
    # Hacer que la ventana sea modal (bloquea la de atrás hasta cerrar)
    ventana.grab_set()

    # --- DISEÑO ---
    tk.Label(ventana, text="Nueva Tarea", font=("Segoe UI", 18, "bold"), 
             bg="#f8f9fa", fg="#333").pack(pady=(0, 20))

    # Título
    tk.Label(ventana, text="Título de la tarea *", font=("Segoe UI", 10), bg="#f8f9fa").pack(anchor="w")
    entry_titulo = tk.Entry(ventana, font=("Segoe UI", 11), bd=1, relief="solid")
    entry_titulo.pack(fill="x", pady=(5, 15))

    # Descripción
    tk.Label(ventana, text="Descripción", font=("Segoe UI", 10), bg="#f8f9fa").pack(anchor="w")
    text_descripcion = tk.Text(ventana, font=("Segoe UI", 11), height=5, bd=1, relief="solid")
    text_descripcion.pack(fill="x", pady=(5, 15))

    # Puntaje
    tk.Label(ventana, text="Puntaje Máximo *", font=("Segoe UI", 10), bg="#f8f9fa").pack(anchor="w")
    entry_puntaje = tk.Entry(ventana, font=("Segoe UI", 11), bd=1, relief="solid")
    entry_puntaje.pack(fill="x", pady=(5, 15))

    # Fecha
    tk.Label(ventana, text="Fecha límite (YYYY-MM-DD) *", font=("Segoe UI", 10), bg="#f8f9fa").pack(anchor="w")
    entry_fecha = tk.Entry(ventana, font=("Segoe UI", 11), bd=1, relief="solid")
    entry_fecha.pack(fill="x", pady=(5, 25))

    # --- BOTONES ---
    # Botón Borrador (Pasa la referencia 'ventana' para poder cerrarla después)
    btn_borrador = RoundedButton(ventana, text="📁 Guardar Borrador", bg="#6c757d", fg="white", 
                                  font=("Segoe UI", 10, "bold"), 
                                  command=lambda: procesar_formulario(ventana, "Borrador"))
    btn_borrador.pack(fill="x", pady=5)

    # Botón Publicar
    btn_publicar = RoundedButton(ventana, text="🚀 Publicar Tarea", bg="#28a745", fg="white", 
                                  font=("Segoe UI", 10, "bold"), 
                                  command=lambda: procesar_formulario(ventana, "Publicada"))
    btn_publicar.pack(fill="x", pady=5)