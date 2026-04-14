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
        obtener_archivo_anterior,
        marcar_tarea_entregada,  # <-- NUEVA IMPORTACIÓN
    )
except ImportError as e:
    print(f"Error importando módulos: {e}")

ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx", ".zip", ".rar", ".png", ".jpg", ".jpeg"]
MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 5 MB
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

selected_files_paths = [] 

def seleccionar_archivos(label_archivo, btn_subir):
    global selected_files_paths
    
    files = filedialog.askopenfilenames(
        title="Seleccionar archivos para la entrega",
        filetypes=[
            ("Archivos permitidos", "*.pdf *.doc *.docx *.zip *.rar *.png *.jpg *.jpeg"),
            ("Todos los archivos", "*.*")
        ]
    )
    
    if files:
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
        if not selected_files_paths:
            label_archivo.config(text="Ningún archivo seleccionado", fg="red")
            btn_subir.config(state="disabled")

# ⚠️ Modificado: Ya no recibe 'entry', recibe directamente los IDs
def subir_entrega(id_tarea, id_alumno, label_archivo, btn_subir, ventana):
    global selected_files_paths

    if not selected_files_paths:
        messagebox.showwarning("Faltan datos", "Selecciona al menos un archivo.")
        return

    if verificar_entrega_existente(id_tarea, id_alumno):
        reemplazar = messagebox.askyesno("Confirmación", "Ya existen entregas previas. ¿Deseas agregar estos archivos?")
        if not reemplazar:
            return 

    exitos = 0
    for ruta_origen in selected_files_paths:
        try:
            nombre_base = os.path.basename(ruta_origen)
            nombre_final = f"T{id_tarea}_A{id_alumno}_{nombre_base}"
            destino = os.path.join(UPLOAD_FOLDER, nombre_final)

            shutil.copy2(ruta_origen, destino)
            peso_kb = round(os.path.getsize(destino) / 1024, 2)

            if guardar_entrega(id_tarea, id_alumno, destino, peso_kb):
                exitos += 1

        except Exception as e:
            print(f"Error al subir {nombre_base}: {e}")

    if exitos > 0:
        # ⚠️ AQUÍ CAMBIAMOS EL ESTADO DE LA TAREA
        marcar_tarea_entregada(id_tarea)
        
        messagebox.showinfo("Éxito", f"Se han procesado {exitos} archivos correctamente.\nLa tarea ha sido marcada como Entregada.")
        
        # Limpiamos variables y cerramos la ventana automáticamente
        selected_files_paths = []
        ventana.destroy() 
    else:
        messagebox.showerror("Error", "No se pudo subir ningún archivo.")

# ⚠️ Modificado: Ahora recibe los IDs como parámetros
def abrir_vista_entrega_estudiante(id_tarea, id_alumno):
    ventana = tk.Toplevel()
    ventana.title("Subir Entrega - Estudiante")
    ventana.geometry("450x450")
    ventana.configure(bg="#FFFBF0", padx=20, pady=20)
    ventana.grab_set()

    frame_header = tk.Frame(ventana, bg="#6D4145", padx=15, pady=15)
    frame_header.pack(fill="x", pady=(0, 20))
    tk.Label(frame_header, text="📥 Recepción de Entrega Digital", font=("Arial", 14, "bold"), 
             bg="#6D4145", fg="#FFEFAE").pack(anchor="w")

    frame_main = tk.Frame(ventana, bg="#FFFBF0")
    frame_main.pack(fill="both", expand=True)

    # ⚠️ En lugar de pedir los datos, se los mostramos al usuario de forma elegante
    info_frame = tk.Frame(frame_main, bg="#F5F1E8", padx=10, pady=10, relief="groove", bd=2)
    info_frame.pack(fill="x", pady=(0, 15))
    
    tk.Label(info_frame, text=f"📌 Entregando Tarea #{id_tarea}", bg="#F5F1E8", fg="#333", font=("Arial", 11, "bold")).pack(anchor="w")
    tk.Label(info_frame, text=f"👤 Estudiante ID: {id_alumno}", bg="#F5F1E8", fg="#666", font=("Arial", 10)).pack(anchor="w")

    label_archivo = tk.Label(frame_main, text="📄 Ningún archivo seleccionado", fg="#888", bg="#FFFBF0", 
                             font=("Arial", 9), wraplength=400)
    label_archivo.pack(fill="x", pady=10)

    btn_seleccionar = tk.Button(
        frame_main, text="📁 Seleccionar archivos", 
        command=lambda: seleccionar_archivos(label_archivo, btn_subir),
        bg="#96D1AA", fg="#2D4A3E", font=("Arial", 10, "bold"), pady=5
    )
    btn_seleccionar.pack(fill="x", pady=5)

    btn_subir = tk.Button(
        frame_main, text="✓ Subir Entrega", 
        command=lambda: subir_entrega(id_tarea, id_alumno, label_archivo, btn_subir, ventana),
        bg="#FFEFAE", fg="#555832", font=("Arial", 10, "bold"), pady=5, state="disabled"
    )
    btn_subir.pack(fill="x", pady=5)

    frame_info = tk.Frame(ventana, bg="#555832", padx=10, pady=5)
    frame_info.pack(fill="x", side="bottom")
    tk.Label(frame_info, text="Formatos: PDF, DOCX, ZIP, JPG | Máx: 5MB", 
             font=("Arial", 8), bg="#555832", fg="#FFEFAE").pack()