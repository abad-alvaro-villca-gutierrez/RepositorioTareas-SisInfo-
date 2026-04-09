import tkinter as tk
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.conexion_bd import traer_tareas


def abrir_lista_tareas():
    ventana = tk.Toplevel()
    ventana.title("Lista de Tareas")
    ventana.geometry("500x400")

    tk.Label(ventana, text="Lista de Tareas Ordenadas", font=("Arial", 14)).pack(pady=10)

    tareas = traer_tareas()

    if not tareas:
        tk.Label(ventana, text="No hay tareas").pack()
        return

    tareas.sort(key=lambda x: x[3])

    for t in tareas:
        texto = f"{t[1]} - {t[3]} ({t[4]})"
        tk.Label(ventana, text=texto).pack(anchor="w")