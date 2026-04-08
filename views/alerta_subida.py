import tkinter as tk
from tkinter import messagebox

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

boton = tk.Button(ventana, text="Subir archivo", command=subir_archivo)
boton.pack(pady=20)

ventana.mainloop()