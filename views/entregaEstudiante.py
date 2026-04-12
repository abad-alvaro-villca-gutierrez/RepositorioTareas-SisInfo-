import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil

# 1. AJUSTE DE RUTA
directorio_actual = os.path.dirname(__file__)
directorio_padre = os.path.abspath(os.path.join(directorio_actual, '..'))
if directorio_padre not in sys.path:
    sys.path.append(directorio_padre)

# 2. IMPORTACIONES
try:
    from config.conexion_bd import (
        guardar_entrega, 
        verificar_entrega_existente, 
        existe_entrega, 
        obtener_archivo_anterior
    )
except ImportError as e:
    print(f"Error importando módulos: {e}")

# Importación de tu clase personalizada
# from rounded_button import RoundedButton 

ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx", ".zip", ".rar", ".png", ".jpg", ".jpeg"]
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))

# Asegurar que la carpeta de destino existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# VARIABLE GLOBAL PARA ALMACENAR LAS RUTAS
selected_files_paths = [] 

def seleccionar_archivos(label_archivo, btn_subir):
    """
    Permite al usuario seleccionar uno o varios archivos y actualiza la interfaz.
    """
    global selected_files_paths
    
    files = filedialog.askopenfilenames(
        title="Seleccionar archivos para la entrega",
        filetypes=[
            ("Archivos permitidos", "*.pdf *.doc *.docx *.zip *.rar *.png *.jpg *.jpeg"),
            ("Todos los archivos", "*.*")
        ]
    )
    
    if files:
        # Validar tamaño de cada archivo antes de aceptarlos
        archivos_validos = []
        for f in files:
            if os.path.getsize(f) <= MAX_FILE_SIZE_BYTES:
                archivos_validos.append(f)
            else:
                messagebox.showwarning("Archivo muy pesado", f"El archivo {os.path.basename(f)} excede los 5MB y será omitido.")

        selected_files_paths = archivos_validos
        cantidad = len(selected_files_paths)
        
        if cantidad == 1:
            nombre_archivo = os.path.basename(selected_files_paths[0])
            label_archivo.config(text=f"Seleccionado: {nombre_archivo}", fg="green")
        elif cantidad > 1:
            label_archivo.config(text=f"✓ {cantidad} archivos listos para subir", fg="green")
        else:
            label_archivo.config(text="Ningún archivo válido seleccionado", fg="red")
            btn_subir.config(state="disabled")
            return

        btn_subir.config(state="normal")
    else:
        # Si el usuario cancela y no había nada antes
        if not selected_files_paths:
            label_archivo.config(text="Ningún archivo seleccionado", fg="red")
            btn_subir.config(state="disabled")

def subir_entrega(entry_id_tarea, entry_id_alumno, label_archivo, btn_subir):
    global selected_files_paths
    
    id_t = entry_id_tarea.get().strip()
    id_a = entry_id_alumno.get().strip()

    if not id_t or not id_a or not selected_files_paths:
        messagebox.showwarning("Faltan datos", "Ingresa IDs y selecciona al menos un archivo.")
        return

    # Verificar si ya existe alguna entrega para este alumno/tarea
    if verificar_entrega_existente(id_t, id_a):
        reemplazar = messagebox.askyesno("Confirmación", "Ya existen entregas previas. ¿Deseas agregar estos archivos?")
        if not reemplazar:
            return 

    exitos = 0
    for ruta_origen in selected_files_paths:
        try:
            nombre_base = os.path.basename(ruta_origen)
            # Creamos un nombre único para evitar colisiones entre alumnos
            nombre_final = f"T{id_t}_A{id_a}_{nombre_base}"
            destino = os.path.join(UPLOAD_FOLDER, nombre_final)

            # Copiar archivo
            shutil.copy2(ruta_origen, destino)
            
            # Peso en KB
            peso_kb = round(os.path.getsize(destino) / 1024, 2)

            # Guardar en BD
            if guardar_entrega(id_t, id_a, destino, peso_kb):
                exitos += 1

        except Exception as e:
            print(f"Error al subir {nombre_base}: {e}")

    if exitos > 0:
        messagebox.showinfo("Éxito", f"Se han procesado {exitos} archivos correctamente.")
        
        # Limpiar Interfaz
        label_archivo.config(text="📄 Ningún archivo seleccionado", fg="#888")
        selected_files_paths = []
        btn_subir.config(state="disabled")
        entry_id_tarea.delete(0, tk.END)
        entry_id_alumno.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "No se pudo subir ningún archivo.")

def abrir_vista_entrega_estudiante():
    ventana = tk.Toplevel()
    ventana.title("Subir Entrega - Estudiante")
    ventana.geometry("500x600")
    ventana.configure(bg="#FFFBF0", padx=20, pady=20)
    ventana.grab_set()

    # Encabezado
    frame_header = tk.Frame(ventana, bg="#6D4145", padx=15, pady=15)
    frame_header.pack(fill="x", pady=(0, 20))
    tk.Label(frame_header, text="📥 Recepción de Entrega Digital", font=("Arial", 14, "bold"), 
             bg="#6D4145", fg="#FFEFAE").pack(anchor="w")

    frame_main = tk.Frame(ventana, bg="#FFFBF0")
    frame_main.pack(fill="both", expand=True)

    # Entradas
    tk.Label(frame_main, text="ID Tarea *:", bg="#FFFBF0", fg="#555832", font=("Arial", 10, "bold")).pack(anchor="w")
    entry_id_tarea = tk.Entry(frame_main, highlightthickness=1, highlightbackground="#96D1AA")
    entry_id_tarea.pack(fill="x", pady=(0, 10))

    tk.Label(frame_main, text="ID Alumno *:", bg="#FFFBF0", fg="#555832", font=("Arial", 10, "bold")).pack(anchor="w")
    entry_id_alumno = tk.Entry(frame_main, highlightthickness=1, highlightbackground="#96D1AA")
    entry_id_alumno.pack(fill="x", pady=(0, 10))

    # Etiqueta de estado de archivo
    label_archivo = tk.Label(frame_main, text="📄 Ningún archivo seleccionado", fg="#888", bg="#F5F1E8", 
                             font=("Arial", 9), padx=10, pady=10, wraplength=400)
    label_archivo.pack(fill="x", pady=10)

    # Botones (Usando tk.Button por compatibilidad, cambia a RoundedButton si lo tienes activo)
    btn_seleccionar = tk.Button(
        frame_main, text="📁 Seleccionar archivos", 
        command=lambda: seleccionar_archivos(label_archivo, btn_subir),
        bg="#96D1AA", fg="#2D4A3E", font=("Arial", 10, "bold"), pady=5
    )
    btn_seleccionar.pack(fill="x", pady=5)

    btn_subir = tk.Button(
        frame_main, text="✓ Subir Entrega", 
        command=lambda: subir_entrega(entry_id_tarea, entry_id_alumno, label_archivo, btn_subir),
        bg="#FFEFAE", fg="#555832", font=("Arial", 10, "bold"), pady=5, state="disabled"
    )
    btn_subir.pack(fill="x", pady=5)

    # Footer Info
    frame_info = tk.Frame(ventana, bg="#555832", padx=10, pady=10)
    frame_info.pack(fill="x", side="bottom")
    tk.Label(frame_info, text="Formatos: PDF, DOCX, ZIP, JPG | Máx: 5MB", 
             font=("Arial", 8), bg="#555832", fg="#FFEFAE").pack()

