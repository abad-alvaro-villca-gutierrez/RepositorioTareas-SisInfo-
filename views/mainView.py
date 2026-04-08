import tkinter as tk
# Importamos la función que abrirá tu formulario desde la carpeta views
from views.formularioTarea import abrir_formulario_tarea

def iniciar_app():
    # tk.Tk() se usa SOLO UNA VEZ en toda la aplicación para la ventana base
    ventana_principal = tk.Tk()
    ventana_principal.title("Dashboard - Repositorio de Tareas")
    ventana_principal.geometry("600x400")
    ventana_principal.configure(padx=20, pady=20)

    # Mensaje de bienvenida
    tk.Label(ventana_principal, text="Bienvenido al Sistema", font=("Arial", 18, "bold")).pack(pady=30)

    # Botón que llama a tu formulario
    btn_nueva_tarea = tk.Button(
        ventana_principal, 
        text="Crear Nueva Tarea", 
        bg="#0052cc", 
        fg="white", 
        font=("Arial", 12, "bold"),
        padx=20,
        pady=10,
        command=abrir_formulario_tarea # Llama a la función importada
    )
    btn_nueva_tarea.pack(pady=10)

    # Iniciar el ciclo de la ventana principal
    ventana_principal.mainloop()

if __name__ == "__main__":
    iniciar_app()