import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from config.conexion_bd import traer_entregas, calificar_entrega, obtener_puntaje_maximo_tarea

# Paleta
COL_BG = "#ffefae"
COL_PANEL = "#6d4145"
COL_ACCENT = "#96d1aa"
COL_TEXT = "#555832"

class EvaluacionDocenteWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Evaluación de Entregas")
        self.configure(bg=COL_BG)
        self.geometry("900x500")
        if master:
            self.transient(master)

        self._build_ui(self)

    def _build_ui(self, root_container):
        # Header
        header = tk.Frame(root_container, bg=COL_PANEL, height=60)
        header.pack(fill="x", padx=12, pady=(12, 8))

        lbl_title = tk.Label(header, text="Ingresar Calificación y Retroalimentación",
                             bg=COL_PANEL, fg=COL_BG, font=("Arial", 14, "bold"))
        lbl_title.pack(padx=12, pady=12)

        main = tk.Frame(root_container, bg=COL_BG)
        main.pack(fill="both", expand=True, padx=12, pady=6)

        # Estilos de la tabla
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#ffffff", foreground=COL_PANEL, rowheight=25)
        style.configure("Treeview.Heading", background=COL_PANEL, foreground=COL_BG, font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', COL_ACCENT)], foreground=[('selected', COL_TEXT)])

        lbl_ent = tk.Label(main, text="Entregas recibidas pendientes:", bg=COL_BG, fg=COL_PANEL, font=("Arial", 10, "bold"))
        lbl_ent.grid(row=0, column=0, sticky="w", pady=(6, 2))

        cols = ("ID", "ID Tarea", "ID Alumno", "Archivo", "Fecha")
        
        self.tree_entregas = ttk.Treeview(main, columns=cols, show="headings", height=6)
        for c in cols:
            self.tree_entregas.heading(c, text=c)
            self.tree_entregas.column(c, width=120, anchor="center")
            
        self.tree_entregas.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(0, 6))
        self.tree_entregas.bind("<<TreeviewSelect>>", self._on_tree_select)

        btns_ent = tk.Frame(main, bg=COL_BG)
        btns_ent.grid(row=2, column=0, columnspan=2, sticky="w", pady=(6, 8))
        
        btn_recargar = tk.Button(btns_ent, text="🔄 Recargar entregas", bg=COL_TEXT, fg=COL_BG,
                                 command=self._cargar_entregas, font=("Arial", 9, "bold"))
        btn_recargar.pack(side="left", padx=(0, 8))

        self.lbl_selected = tk.Label(main, text="Ninguna entrega seleccionada", bg=COL_BG, fg=COL_PANEL, font=("Arial", 10, "italic"))
        self.lbl_selected.grid(row=3, column=0, columnspan=2, sticky="w", pady=(5,10))

        # Calificación
        lbl_cal = tk.Label(main, text="Calificación (0-100):", bg=COL_BG, fg=COL_TEXT, font=("Arial", 10, "bold"))
        lbl_cal.grid(row=4, column=0, sticky="w", pady=(8, 2))

        self.cal_var = tk.IntVar(value=0)
        sp_cal = tk.Spinbox(main, from_=0, to=100, textvariable=self.cal_var, width=10, font=("Arial", 10))
        sp_cal.grid(row=4, column=1, sticky="w", padx=(6, 0))

        # Retroalimentación
        lbl_fb = tk.Label(main, text="Retroalimentación:", bg=COL_BG, fg=COL_TEXT, font=("Arial", 10, "bold"))
        lbl_fb.grid(row=5, column=0, sticky="nw", pady=(8, 2))

        self.txt_fb = tk.Text(main, height=6, wrap="word", bg="white", fg=COL_PANEL, font=("Arial", 10))
        self.txt_fb.grid(row=5, column=1, sticky="nsew", padx=(6, 0))

        # Botones
        btn_frame = tk.Frame(main, bg=COL_BG)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=15)

        btn_submit = tk.Button(btn_frame, text="✅ Guardar Evaluación", bg=COL_ACCENT, fg=COL_TEXT,
                               font=("Arial", 10, "bold"), activebackground=COL_PANEL, command=self._on_submit)
        btn_submit.pack(side="left", ipadx=8, padx=(0, 8))

        btn_clear = tk.Button(btn_frame, text="Limpiar Formulario", bg=COL_PANEL, fg=COL_BG, 
                              font=("Arial", 10, "bold"), command=self._clear_form)
        btn_clear.pack(side="left", ipadx=8)

        main.columnconfigure(1, weight=1)
        main.rowconfigure(1, weight=1)

        self.selected_entrega = None
        self._cargar_entregas()

    def _on_submit(self):
        if not self.selected_entrega:
            messagebox.showwarning("Atención", "Seleccione una entrega de la lista antes de calificar.")
            return

        # 1. Validar que sea un número
        try:
            cal_val = self.cal_var.get()
        except tk.TclError:
            messagebox.showerror("Error", "La calificación debe ser un número entero.")
            return
            
        id_tarea = self.selected_entrega.get("id_tarea")
        
        # 2. Consultar el puntaje máximo permitido para esta tarea
        puntaje_maximo = obtener_puntaje_maximo_tarea(id_tarea)

        # 3. Validar rango dinámico (0 hasta puntaje_maximo)
        if not (0 <= cal_val <= puntaje_maximo):
            messagebox.showerror("Rango Inválido", f"La calificación para esta tarea debe estar entre 0 y {puntaje_maximo}.")
            return

        fb = self.txt_fb.get("1.0", "end").strip()

        if not fb:
            if not messagebox.askyesno("Confirmación", "La retroalimentación está vacía. ¿Desea guardar de todos modos?"):
                return

        id_entrega = self.selected_entrega.get("id_entrega")

        # 4. Guardar en Base de Datos
        exito = calificar_entrega(id_entrega, cal_val, fb)

        if exito:
            messagebox.showinfo("Éxito", f"La calificación ({cal_val}/{puntaje_maximo}) se ha guardado en la base de datos correctamente.")
            self._clear_form()
            self._cargar_entregas() # Recarga la tabla para ver los cambios
        else:
            messagebox.showerror("Error", "Ocurrió un problema de base de datos. Intente nuevamente.")
    def _clear_form(self):
        self.cal_var.set(0)
        self.txt_fb.delete("1.0", "end")
        self.selected_entrega = None
        self.lbl_selected.config(text="Ninguna entrega seleccionada")

    def _cargar_entregas(self):
        # Limpiar tabla actual
        for r in self.tree_entregas.get_children():
            self.tree_entregas.delete(r)

        # Cargar entregas limpiamente
        try:
            entregas = traer_entregas()
        except Exception as e:
            print(f"Error cargando entregas: {e}")
            entregas = []

        for e in entregas:
            id_entrega = e[0]
            id_tarea = e[1]
            id_alumno = e[2]
            ruta = os.path.basename(e[3]) if e[3] else "Sin archivo"
            fecha = str(e[4]) if e[4] else "Sin fecha"
            
            self.tree_entregas.insert("", "end", iid=str(id_entrega), 
                                      values=(id_entrega, id_tarea, id_alumno, ruta, fecha))

    def _on_tree_select(self, event):
        sel = self.tree_entregas.selection()
        if not sel:
            return
        iid = sel[0]
        vals = self.tree_entregas.item(iid, "values")
        
        self.selected_entrega = {
            "id_entrega": int(vals[0]),
            "id_tarea": vals[1],
            "id_alumno": vals[2]
        }
        self.lbl_selected.config(text=f"📌 Seleccionada -> Entrega #{vals[0]} | Tarea: {vals[1]} | Alumno: {vals[2]}")

def abrir_evaluacion_docente(parent=None):
    win = EvaluacionDocenteWindow(master=parent)
    return win

if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw() # Oculta la ventana principal vacía
    abrir_evaluacion_docente()
    app.mainloop()

