import tkinter as tk
from tkinter import messagebox
import sys
import os

# 1. Le decimos a Python que suba un nivel (..) para reconocer las otras carpetas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rounded_button import RoundedButton

# 2. Importamos las funciones necesarias
from config.conexion_bd import guardar_tarea
from controllers.tarea_controladores import validar_tarea

def procesar_formulario(estado_elegido="Publicada"):
    """Esta función se ejecuta al hacer clic en los botones de guardado"""
    # 1. Obtener datos
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
        # Aquí se cumple la "Persistencia de datos con su estado correspondiente"
        exito = guardar_tarea(titulo, descripcion, puntaje_int, fecha, estado=estado_elegido)

        # 4. Feedback al usuario
        if exito:
            messagebox.showinfo("Éxito", f"¡La tarea se guardó como {estado_elegido}!")
            limpiar_campos() 
        else:
            messagebox.showerror("Error de BD", "Hubo un problema al persistir los datos.")
            
    except Exception as e:
        messagebox.showerror("Error Crítico", f"Ocurrió un error inesperado: {e}")
        
def limpiar_campos():
    """Limpia el formulario después de guardar"""
    entry_titulo.delete(0, tk.END)
    text_descripcion.delete("1.0", tk.END)
    entry_puntaje.delete(0, tk.END)
    entry_fecha.delete(0, tk.END)

# ==========================================
# DISEÑO DE LA INTERFAZ GRÁFICA (SUB-VENTANA)
# ==========================================

def abrir_formulario_tarea():
    """Función que dibuja y abre la ventana del formulario"""
    
    global entry_titulo, text_descripcion, entry_puntaje, entry_fecha

    ventana = tk.Toplevel()
    ventana.title("Repositorio de Tareas - Panel Docente")
    ventana.geometry("400x550") # Un poco más alta para los botones
    ventana.configure(padx=20, pady=20)
    ventana.grab_set()

    # Título Principal
    tk.Label(ventana, text="Crear Nueva Tarea", font=("Arial", 16, "bold")).pack(pady=(0, 15))

    # Inputs
    tk.Label(ventana, text="Título de la tarea *:").pack(anchor="w")
    entry_titulo = tk.Entry(ventana, width=40)
    entry_titulo.pack(pady=(0, 10))

    tk.Label(ventana, text="Descripción:").pack(anchor="w")
    text_descripcion = tk.Text(ventana, width=40, height=6)
    text_descripcion.pack(pady=(0, 10))

    tk.Label(ventana, text="Puntaje Máximo *:").pack(anchor="w")
    entry_puntaje = tk.Entry(ventana, width=40)
    entry_puntaje.pack(pady=(0, 10))

    tk.Label(ventana, text="Fecha límite (YYYY-MM-DD) *:").pack(anchor="w")
    entry_fecha = tk.Entry(ventana, width=40)
    entry_fecha.pack(pady=(0, 20))

    # --- BOTONES DE ACCIÓN (Implementación de Persistencia con Estado) ---
    
    # Botón 1: Guardar como Borrador
    btn_borrador = RoundedButton(ventana, text="Guardar como Borrador", bg="#6c757d", fg="white", 
                                 font=("Arial", 10, "bold"), 
                                 command=lambda: procesar_formulario("Borrador"))
    btn_borrador.pack(fill="x", pady=5)

    # Botón 2: Publicar
    btn_publicar = RoundedButton(ventana, text="Publicar Tarea", bg="#28a745", fg="white", 
                                 font=("Arial", 10, "bold"), 
                                 command=lambda: procesar_formulario("Publicada"))
    btn_publicar.pack(fill="x", pady=5)