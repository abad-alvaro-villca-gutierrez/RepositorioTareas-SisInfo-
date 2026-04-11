import tkinter as tk
import sys
import os

# Configuración de rutas para asegurar importaciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.conexion_bd import traer_tareas_vencidas

def verificar_alertas_docente():
    """
    Identifica tareas vencidas y lanza un popup modal con un diseño moderno.
    """
    tareas_vencidas = traer_tareas_vencidas()
    
    if tareas_vencidas:
        # 1. Crear ventana emergente (Toplevel)
        alerta = tk.Toplevel()
        alerta.title("Aviso del Sistema")
        alerta.configure(bg="#FFFFFF")
        
        # 2. Dimensiones y Centrado en pantalla
        ancho = 500
        alto = 380
        x = (alerta.winfo_screenwidth() // 2) - (ancho // 2)
        y = (alerta.winfo_screenheight() // 2) - (alto // 2)
        alerta.geometry(f"{ancho}x{alto}+{x}+{y}")
        alerta.resizable(False, False)
        
        # 3. Comportamiento Modal (Bloquea la ventana de atrás hasta que se cierre esta)
        alerta.transient()
        alerta.grab_set()

        # --- DISEÑO DEL COMPONENTE ---
        
        # Cabecera roja/salmón
        header = tk.Frame(alerta, bg="#FF5252", pady=20)
        header.pack(fill="x")
        
        tk.Label(header, text="⚠️ Tareas Vencidas Detectadas", 
                 font=("Segoe UI", 16, "bold"), bg="#FF5252", fg="#FFFFFF").pack()

        # Cuerpo
        cuerpo = tk.Frame(alerta, bg="#FFFFFF", padx=30, pady=20)
        cuerpo.pack(fill="both", expand=True)

        tk.Label(cuerpo, text="Las siguientes tareas han pasado su fecha límite y continúan con estado 'Publicada':", 
                 font=("Segoe UI", 11), bg="#FFFFFF", fg="#555555", 
                 wraplength=440, justify="center").pack(pady=(0, 15))

        # Contenedor para la lista de tareas (Text widget para permitir scroll visual y estilos)
        frame_lista = tk.Frame(cuerpo, bg="#F5F1E8", highlightbackground="#E0DBCF", highlightthickness=1)
        frame_lista.pack(fill="both", expand=True, pady=5)
        
        texto_tareas = tk.Text(frame_lista, bg="#F5F1E8", fg="#6D4145", font=("Segoe UI", 11, "bold"), 
                               bd=0, height=6, padx=15, pady=15)
        texto_tareas.pack(side="left", fill="both", expand=True)
        
        # Insertar los datos
        for t in tareas_vencidas:
            nombre = t[0]
            fecha_vence = t[1].date() if hasattr(t[1], 'date') else t[1]
            texto_tareas.insert("end", f"• {nombre}\n  (Venció: {fecha_vence})\n\n")
        
        # Deshabilitar escritura para que el usuario no pueda borrar el texto
        texto_tareas.config(state="disabled") 

        # Pie con botón
        pie = tk.Frame(alerta, bg="#FFFFFF", pady=15)
        pie.pack(fill="x", side="bottom")

        # Botón de estilo plano moderno
        btn_cerrar = tk.Button(pie, text="Entendido", bg="#6D4145", fg="#FFEFAE", 
                               font=("Segoe UI", 11, "bold"), relief="flat", 
                               padx=30, pady=20, cursor="hand2",
                               activebackground="#553336", activeforeground="white",
                               command=alerta.destroy)
        btn_cerrar.pack()