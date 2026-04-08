import tkinter as tk
# Si dejaste este archivo en la raíz, usas: from views.formularioTarea import abrir_formulario_tarea
# Si lo dejaste dentro de la carpeta views, usas: from formularioTarea import abrir_formulario_tarea
from formularioTarea import abrir_formulario_tarea 

def iniciar_app():
    ventana_principal = tk.Tk()
    ventana_principal.title("Dashboard - Repositorio de Tareas")
    
    # Hacer que la ventana se inicie MAXIMIZADA en Windows
    ventana_principal.state('zoomed')
    
    # Configuramos un color de fondo un poco más profesional
    ventana_principal.configure(bg="#f4f6f9", padx=20, pady=20)

    # Contenedor central para organizar los elementos
    frame_central = tk.Frame(ventana_principal, bg="#f4f6f9")
    frame_central.pack(expand=True) # expand=True hace que se centre en la pantalla gigante

    # Mensaje de bienvenida
    tk.Label(
        frame_central, 
        text="Bienvenido al Sistema de Tareas", 
        font=("Arial", 24, "bold"), 
        bg="#f4f6f9"
    ).pack(pady=30)

    # Botón que llama a tu formulario
    btn_nueva_tarea = tk.Button(
        frame_central, 
        text="Crear Nueva Tarea", 
        bg="#0052cc", 
        fg="white", 
        font=("Arial", 14, "bold"),
        padx=30,
        pady=15,
        cursor="hand2", # Cambia el cursor a una manito al pasar por encima
        command=abrir_formulario_tarea
    )
    btn_nueva_tarea.pack(pady=10)

    # Botón para salir del sistema
    btn_salir = tk.Button(
        frame_central, 
        text="Salir del Sistema", 
        bg="#dc3545", 
        fg="white", 
        font=("Arial", 12, "bold"),
        padx=20,
        pady=10,
        cursor="hand2",
        command=ventana_principal.destroy # Cierra la aplicación
    )
    btn_salir.pack(pady=30)

    # Iniciar el ciclo de la ventana principal
    ventana_principal.mainloop()

if __name__ == "__main__":
    iniciar_app()