import tkinter as tk
from docenteView import abrir_panel_docente
from alumnoView import abrir_panel_alumno
from lista_tareas_sistema import abrir_lista_tareas

def iniciar_app():
    ventana_principal = tk.Tk()
    ventana_principal.title("Sistema de Gestión Académica - Selección de Rol")
    
    # Maximizar ventana
    ventana_principal.state('zoomed')
    ventana_principal.configure(bg="#FFFBF0")

    # Título superior con color de la paleta
    tk.Label(
        ventana_principal, 
        text="Repositorio de Tareas", 
        font=("Arial", 32, "bold"), 
        bg="#FFFBF0",
        fg="#6D4145"
    ).pack(pady=(60, 10))

    tk.Label(
        ventana_principal, 
        text="Seleccione su perfil para continuar", 
        font=("Arial", 14), 
        bg="#FFFBF0",
        fg="#555832"
    ).pack(pady=(0, 40))

    # Contenedor para las dos opciones (Docente y Estudiante)
    frame_opciones = tk.Frame(ventana_principal, bg="#FFFBF0")
    frame_opciones.pack(expand=True)
    
      

    # --- SECCIÓN DOCENTE ---
    frame_docente = tk.Frame(frame_opciones, bg="white", padx=40, pady=40, highlightbackground="#96D1AA", highlightthickness=3)
    frame_docente.grid(row=0, column=0, padx=20)

    tk.Label(frame_docente, text="👨‍🏫", font=("Arial", 50), bg="white").pack()
    tk.Label(frame_docente, text="Panel Docente", font=("Arial", 16, "bold"), bg="white", fg="#6D4145").pack(pady=10)
    tk.Label(frame_docente, text="Crear tareas, gestionar\nestados y revisar entregas.", 
             font=("Arial", 10), bg="white", fg="#555832").pack(pady=10)

    btn_docente = tk.Button(
        frame_docente, 
        text="Acceder como Docente", 
        bg="#555832", 
        fg="#FFEFAE", 
        font=("Arial", 11, "bold"),
        padx=20,
        pady=10,
        cursor="hand2",
        relief="flat",
        activebackground="#6D4145",
        activeforeground="#FFEFAE",
        command=abrir_panel_docente
    )
    btn_docente.pack(pady=10)

    # --- SECCIÓN ESTUDIANTE ---
    frame_estudiante = tk.Frame(frame_opciones, bg="white", padx=40, pady=40, highlightbackground="#96D1AA", highlightthickness=3)
    frame_estudiante.grid(row=0, column=1, padx=20)

    tk.Label(frame_estudiante, text="🎓", font=("Arial", 50), bg="white").pack()
    tk.Label(frame_estudiante, text="Panel Estudiante", font=("Arial", 16, "bold"), bg="white", fg="#6D4145").pack(pady=10)
    tk.Label(frame_estudiante, text="Ver tareas pendientes y\nsubir archivos de entrega.", 
             font=("Arial", 10), bg="white", fg="#555832").pack(pady=10)

    btn_estudiante = tk.Button(
        frame_estudiante, 
        text="Acceder como Estudiante", 
        bg="#96D1AA", 
        fg="#2D4A3E", 
        font=("Arial", 11, "bold"),
        padx=20,
        pady=10,
        cursor="hand2",
        relief="flat",
        activebackground="#79B8A0",
        activeforeground="#2D4A3E",
        command=abrir_panel_alumno
    )
    btn_estudiante.pack(pady=10)
    
    
    # BOTON VER TAREAS ORDENADAS
    btn_lista = tk.Button(
    ventana_principal,
    text="📋 VER TAREAS ",
    bg="#FFEFAE",
    fg="#555832",
    font=("Arial", 12, "bold"),
    command=abrir_lista_tareas,
    activebackground="#FFE589",
    activeforeground="#555832",
    relief="flat",
    cursor="hand2"
    )
    btn_lista.pack(pady=10)

    # Botón Salir en la parte inferior
    btn_salir = tk.Button(
        ventana_principal, 
        text="Cerrar Aplicación", 
        bg="#FFFBF0", 
        fg="#6D4145", 
        font=("Arial", 10, "underline"),
        bd=0,
        cursor="hand2",
        activebackground="#FFFBF0",
        activeforeground="#555832",
        command=ventana_principal.destroy
    )
    btn_salir.pack(side=tk.BOTTOM, pady=40)

    ventana_principal.mainloop()

if __name__ == "__main__":
    iniciar_app()