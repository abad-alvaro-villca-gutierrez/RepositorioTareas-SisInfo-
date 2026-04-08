import tkinter as tk
from tkinter import messagebox
import sys
import os

# 1. Le decimos a Python que suba un nivel (..) para reconocer las otras carpetas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Importamos la función apuntando a la carpeta correcta
from config.conexion_bd import guardar_tarea

def procesar_formulario():
    """Esta función se ejecuta al hacer clic en el botón Guardar"""
    # 1. Obtener los datos escritos por el usuario
    titulo = entry_titulo.get()
    descripcion = text_descripcion.get("1.0", tk.END).strip()
    puntaje = entry_puntaje.get()
    fecha = entry_fecha.get()

    # 2. Validaciones básicas (Reglas de negocio)
    if not titulo or not puntaje or not fecha:
        messagebox.showwarning("Campos vacíos", "Por favor, llena todos los campos obligatorios.")
        return
    
    if not puntaje.isdigit():
        messagebox.showerror("Error", "El puntaje debe ser un número entero (ej. 100).")
        return

    # 3. Guardar en la Base de Datos
    puntaje_int = int(puntaje)
    
    # Llamamos a tu función, usando 'Publicada' como estado por defecto
    exito = guardar_tarea(titulo, descripcion, puntaje_int, fecha, estado="Publicada")

    # 4. Dar retroalimentación al usuario
    if exito:
        messagebox.showinfo("Éxito", "¡La tarea se guardó correctamente en la base de datos!")
        limpiar_campos()
    else:
        messagebox.showerror("Error de BD", "Hubo un problema al guardar. Revisa la consola para más detalles.")

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
    
    # Declarar variables globales para que procesar_formulario pueda leerlas
    global entry_titulo, text_descripcion, entry_puntaje, entry_fecha

    # Crear la ventana secundaria (Hija de main.py)
    ventana = tk.Toplevel()
    ventana.title("Repositorio de Tareas - Panel Docente")
    ventana.geometry("400x500")
    ventana.configure(padx=20, pady=20)
    
    # Obliga a que esta ventana se mantenga por encima del Dashboard principal
    ventana.grab_set()

    # Título Principal
    tk.Label(ventana, text="Crear Nueva Tarea", font=("Arial", 16, "bold")).pack(pady=(0, 15))

    # Campo: Título de la Tarea
    tk.Label(ventana, text="Título de la tarea *:").pack(anchor="w")
    entry_titulo = tk.Entry(ventana, width=40)
    entry_titulo.pack(pady=(0, 10))

    # Campo: Descripción
    tk.Label(ventana, text="Descripción:").pack(anchor="w")
    text_descripcion = tk.Text(ventana, width=40, height=8)
    text_descripcion.pack(pady=(0, 10))

    # Campo: Puntaje
    tk.Label(ventana, text="Puntaje Máximo *:").pack(anchor="w")
    entry_puntaje = tk.Entry(ventana, width=40)
    entry_puntaje.pack(pady=(0, 10))

    # Campo: Fecha de Vencimiento
    tk.Label(ventana, text="Fecha límite (YYYY-MM-DD) *:").pack(anchor="w")
    entry_fecha = tk.Entry(ventana, width=40)
    entry_fecha.pack(pady=(0, 20))

    # Botón Guardar
    boton_guardar = tk.Button(ventana, text="Guardar Tarea", bg="green", fg="white", font=("Arial", 10, "bold"), command=procesar_formulario)
    boton_guardar.pack(fill="x", pady=10)