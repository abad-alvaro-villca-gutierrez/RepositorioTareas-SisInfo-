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
        label_archivo.config(text="📄 Ningún archivo seleccionado", fg="#888")
        boton_subir.config(state="disabled")
        return

    tamaño = os.path.getsize(archivo)
    if tamaño > MAX_FILE_SIZE_BYTES:
        messagebox.showerror("Archivo muy grande", "El archivo supera el límite de 5 MB. Elige uno más pequeño.")
        selected_file_path = None
        label_archivo.config(text="📄 Ningún archivo seleccionado", fg="#888")
        boton_subir.config(state="disabled")
        return

    selected_file_path = archivo
    nombre_archivo = os.path.basename(archivo)
    tamaño_kb = round(tamaño / 1024, 2)
    label_archivo.config(text=f"✓ {nombre_archivo} ({tamaño_kb} KB)", fg="#2D4A3E")
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
    ventana.geometry("500x550")
    ventana.configure(bg="#FFFBF0", padx=20, pady=20)
    ventana.grab_set()
    ventana.resizable(True, True)

    # Encabezado con color de la paleta
    frame_header = tk.Frame(ventana, bg="#6D4145", padx=15, pady=15)
    frame_header.pack(fill="x", pady=(0, 20))
    tk.Label(frame_header, text="📥 Recepción de Entrega Digital", font=("Arial", 16, "bold"), 
             bg="#6D4145", fg="#FFEFAE").pack(anchor="w")

    # Frame principal usando grid para mejor control
    frame_main = tk.Frame(ventana, bg="#FFFBF0")
    frame_main.pack(fill="both", expand=True)
    frame_main.columnconfigure(0, weight=1)

    # ID Tarea
    tk.Label(frame_main, text="ID Tarea *:", bg="#FFFBF0", fg="#555832", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=(5, 3))
    entry_id_tarea = tk.Entry(frame_main, bg="white", fg="#333333", bd=1, 
                              highlightthickness=2, highlightbackground="#96D1AA", highlightcolor="#555832")
    entry_id_tarea.grid(row=1, column=0, sticky="ew", pady=(0, 12), padx=2)

    # ID Alumno
    tk.Label(frame_main, text="ID Alumno *:", bg="#FFFBF0", fg="#555832", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=(5, 3))
    entry_id_alumno = tk.Entry(frame_main, bg="white", fg="#333333", bd=1, 
                               highlightthickness=2, highlightbackground="#96D1AA", highlightcolor="#555832")
    entry_id_alumno.grid(row=3, column=0, sticky="ew", pady=(0, 12), padx=2)

    # Archivo seleccionado
    tk.Label(frame_main, text="Archivo seleccionado:", bg="#FFFBF0", fg="#555832", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", pady=(10, 5))
    label_archivo = tk.Label(frame_main, text="📄 Ningún archivo seleccionado", fg="#888", bg="#F5F1E8", 
                             font=("Arial", 10), padx=10, pady=10, wraplength=400, justify="left")
    label_archivo.grid(row=5, column=0, sticky="ew", pady=(0, 12), padx=2)

    # Botón Seleccionar
    btn_seleccionar = tk.Button(
        frame_main,
        text="📁 Seleccionar archivo",
        command=lambda: seleccionar_archivo(label_archivo, btn_subir),
        bg="#96D1AA",
        fg="#2D4A3E",
        activebackground="#79B8A0",
        activeforeground="#2D4A3E",
        font=("Arial", 11, "bold"),
        padx=15,
        pady=10,
        cursor="hand2",
        bd=0,
        relief="flat"
    )
    btn_seleccionar.grid(row=6, column=0, sticky="ew", pady=(0, 10), padx=2)

    # Botón Subir
    btn_subir = tk.Button(
        frame_main,
        text="✓ Subir Entrega",
        command=lambda: subir_entrega(entry_id_tarea, entry_id_alumno, label_archivo, btn_subir),
        bg="#FFEFAE",
        fg="#555832",
        activebackground="#FFE589",
        activeforeground="#555832",
        font=("Arial", 11, "bold"),
        padx=15,
        pady=10,
        cursor="hand2",
        state="disabled",
        bd=0,
        relief="flat"
    )
    btn_subir.grid(row=7, column=0, sticky="ew", pady=(0, 15), padx=2)

    # Información sobre extensiones y límite
    frame_info = tk.Frame(ventana, bg="#555832", padx=12, pady=10)
    frame_info.pack(fill="x")
    tk.Label(frame_info, text="✓ PDF, DOC, DOCX, ZIP, RAR, PNG, JPG", 
             font=("Arial", 9), bg="#555832", fg="#FFEFAE", wraplength=450, justify="left").pack(anchor="w", pady=2)
    tk.Label(frame_info, text="✓ Tamaño máximo: 5 MB", 
             font=("Arial", 9), bg="#555832", fg="#FFEFAE", wraplength=450, justify="left").pack(anchor="w", pady=2) 
