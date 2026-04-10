import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from rounded_button import RoundedButton

def subir_archivo():
    ya_existe_entrega = True  # simula que ya existe una entrega

    if ya_existe_entrega:
        respuesta = messagebox.askyesno(
            "Confirmación",
            "Ya existe una entrega. ¿Deseas reemplazarla?"
        )

        if respuesta:
            print("Reemplazando archivo...")
        else:
            print("Operación cancelada")
    else:
        print("Subida normal")

ventana = tk.Tk()
ventana.title("Subida de tareas")

boton = RoundedButton(ventana, text="Subir archivo", command=subir_archivo, bg="#96D1AA", fg="#2D4A3E", font=("Arial", 11, "bold"))
boton.pack(pady=20)

ventana.mainloop()