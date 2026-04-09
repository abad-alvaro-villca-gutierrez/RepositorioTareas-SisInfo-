import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os
import shutil

# Ajustar ruta para poder importar desde config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.conexion_bd import guardar_entrega, existe_entrega

ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx", ".zip", ".rar", ".png", ".jpg", ".jpeg"]
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))

selected_file_path = None


def seleccionar_archivo(label_archivo, boton_subir):
    global selected_file_path

    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de entrega",
        filetypes=[
            ("Documentos y archivos", "*.pdf *.doc *.docx *.zip *.rar *.png *.jpg *.jpeg"),
            ("Todos los archivos", "*.*")
        ]
    )

    if not archivo:
        return

    extension = os.path.splitext(archivo)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        messagebox.showerror("Extensión inválida", "Solo se permiten archivos PDF, DOC/DOCX, ZIP, RAR, PNG y JPG.")
        selected_file_path = None
        label_archivo.config(text="Ningún archivo seleccionado")
        boton_subir.config(state="disabled")
        return

    tamaño = os.path.getsize(archivo)
    if tamaño > MAX_FILE_SIZE_BYTES:
        messagebox.showerror("Archivo muy grande", "El archivo supera el límite de 5 MB. Elige uno más pequeño.")
        selected_file_path = None
        label_archivo.config(text="Ningún archivo seleccionado")
        boton_subir.config(state="disabled")
        return

    selected_file_path = archivo
    label_archivo.config(text=os.path.basename(archivo))
    boton_subir.config(state="normal")


def subir_entrega(entry_id_tarea, entry_id_alumno, label_archivo, boton_subir):
    global selected_file_path

    id_tarea = entry_id_tarea.get().strip()
    id_alumno = entry_id_alumno.get().strip()

    if not id_tarea or not id_alumno:
        messagebox.showwarning("Campos obligatorios", "Completa el ID de tarea y el ID de alumno.")
        return

    if not selected_file_path:
        messagebox.showwarning("Archivo no seleccionado", "Selecciona un archivo antes de subir la entrega.")
        return

    if existe_entrega(id_tarea, id_alumno):
        reemplazar = messagebox.askyesno(
            "Entrega existente",
            "Ya existe una entrega para esta tarea. ¿Deseas reemplazarla con el nuevo archivo?"
        )
        if not reemplazar:
            return

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    nombre_archivo = os.path.basename(selected_file_path)
    destino = os.path.join(UPLOAD_FOLDER, f"tarea_{id_tarea}_alumno_{id_alumno}_{nombre_archivo}")

    try:
        shutil.copy2(selected_file_path, destino)
        peso_kb = round(os.path.getsize(destino) / 1024, 2)

        exito = guardar_entrega(id_tarea, id_alumno, destino, peso_kb)
        if exito:
            messagebox.showinfo("Éxito", "El archivo se subió correctamente y la entrega quedó registrada.")
            entry_id_tarea.delete(0, tk.END)
            entry_id_alumno.delete(0, tk.END)
            label_archivo.config(text="Ningún archivo seleccionado")
            selected_file_path = None
            boton_subir.config(state="disabled")
        else:
            messagebox.showerror("Error", "Ocurrió un problema al guardar la entrega en la base de datos.")
    except Exception as e:
        messagebox.showerror("Error de archivo", f"No se pudo copiar el archivo: {e}")


def abrir_vista_entrega_estudiante():
    global selected_file_path
    selected_file_path = None

    ventana = tk.Toplevel()
    ventana.title("Subir Entrega - Estudiante")
    ventana.geometry("450x420")
    ventana.configure(bg="#eef2f7", padx=20, pady=20)
    ventana.grab_set()

    tk.Label(ventana, text="Recepción de Entrega Digital", font=("Arial", 16, "bold"), bg="#eef2f7", fg="#1f3a93").pack(pady=(0, 15))

    tk.Label(ventana, text="ID Tarea *:", bg="#eef2f7", fg="#333333").pack(anchor="w")
    entry_id_tarea = tk.Entry(ventana, width=45, bg="white", fg="#333333", bd=1, highlightthickness=1, highlightcolor="#8fa5c4")
    entry_id_tarea.pack(pady=(0, 10))

    tk.Label(ventana, text="ID Alumno *:", bg="#eef2f7", fg="#333333").pack(anchor="w")
    entry_id_alumno = tk.Entry(ventana, width=45, bg="white", fg="#333333", bd=1, highlightthickness=1, highlightcolor="#8fa5c4")
    entry_id_alumno.pack(pady=(0, 10))

    tk.Label(ventana, text="Archivo seleccionado:", bg="#eef2f7", fg="#333333").pack(anchor="w", pady=(10, 0))
    label_archivo = tk.Label(ventana, text="Ningún archivo seleccionado", fg="#555", bg="#eef2f7")
    label_archivo.pack(anchor="w", pady=(0, 10))

    btn_seleccionar = tk.Button(
        ventana,
        text="Seleccionar archivo",
        command=lambda: seleccionar_archivo(label_archivo, btn_subir),
        bg="#4a90e2",
        fg="white",
        activebackground="#3f7ecb",
        activeforeground="white",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=8,
        cursor="hand2",
        bd=0
    )
    btn_seleccionar.pack(fill="x", pady=(0, 10))

    btn_subir = tk.Button(
        ventana,
        text="Subir Entrega",
        command=lambda: subir_entrega(entry_id_tarea, entry_id_alumno, label_archivo, btn_subir),
        bg="#ff7a59",
        fg="white",
        activebackground="#e06642",
        activeforeground="white",
        font=("Arial", 10, "bold"),
        padx=10,
        pady=8,
        cursor="hand2",
        state="disabled",
        bd=0
    )
    btn_subir.pack(fill="x", pady=(0, 15))

    tk.Label(ventana, text="Extensiones permitidas: PDF, DOC, DOCX, ZIP, RAR, PNG, JPG", fg="#4d4d4d", bg="#eef2f7").pack(anchor="w")
    #tk.Label(ventana, text="Tamaño máximo: 5 MB", fg="#333").pack(anchor="w", pady=(0, 5)) 
