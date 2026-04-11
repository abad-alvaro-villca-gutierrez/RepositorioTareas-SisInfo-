
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime



# Paleta
COL_BG = "#ffefae"
COL_PANEL = "#6d4145"
COL_ACCENT = "#96d1aa"
COL_TEXT = "#555832"


class EvaluacionDocenteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Evaluación docente")
        self.configure(bg=COL_BG)
        self.geometry("540x420")

        self._build_ui(self)


class EvaluacionDocenteWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Evaluación docente")
        self.configure(bg=COL_BG)
        self.geometry("540x420")
        self.transient(master)

        self._build_ui(self)

    def _build_ui(self, root_container):
        header = tk.Frame(root_container, bg=COL_PANEL, height=60)
        header.pack(fill="x", padx=12, pady=(12, 8))

        lbl_title = tk.Label(header, text="Ingresar calificación y retroalimentación",
                             bg=COL_PANEL, fg="white", font=(None, 14, "bold"))
        lbl_title.pack(padx=12, pady=12)

        main = tk.Frame(root_container, bg=COL_BG)
        main.pack(fill="both", expand=True, padx=12, pady=6)

        # Selector de alumno / tarea (ejemplo simple)
        # Lista de entregas
        lbl_ent = tk.Label(main, text="Entregas recibidas:", bg=COL_BG, fg=COL_TEXT)
        lbl_ent.grid(row=0, column=0, sticky="w", pady=(6, 2))

        cols = ("ID", "Tarea", "Alumno", "Archivo", "Fecha", "A tiempo")
        self.tree_entregas = ttk.Treeview(main, columns=cols, show="headings", height=6)
        for c in cols:
            self.tree_entregas.heading(c, text=c)
            self.tree_entregas.column(c, width=120)
        self.tree_entregas.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(0, 6))
        self.tree_entregas.bind("<<TreeviewSelect>>", self._on_tree_select)

        btns_ent = tk.Frame(main, bg=COL_BG)
        btns_ent.grid(row=2, column=0, columnspan=2, sticky="w", pady=(6, 8))
        tk.Button(btns_ent, text="Recargar entregas", command=self._cargar_entregas).pack(side="left", padx=(0, 8))

        # Etiqueta con la entrega seleccionada
        self.lbl_selected = tk.Label(main, text="Ninguna entrega seleccionada", bg=COL_BG, fg=COL_TEXT)
        self.lbl_selected.grid(row=3, column=0, columnspan=2, sticky="w")

        # Calificación
        lbl_cal = tk.Label(main, text="Calificación (0-100):", bg=COL_BG, fg=COL_TEXT)
        lbl_cal.grid(row=4, column=0, sticky="w", pady=(8, 2))

        self.cal_var = tk.IntVar(value=80)
        sp_cal = tk.Spinbox(main, from_=0, to=100, textvariable=self.cal_var, width=6)
        sp_cal.grid(row=4, column=1, sticky="w", padx=(6, 0))

        # Retroalimentación
        lbl_fb = tk.Label(main, text="Retroalimentación:", bg=COL_BG, fg=COL_TEXT)
        lbl_fb.grid(row=5, column=0, sticky="nw", pady=(8, 2))

        self.txt_fb = tk.Text(main, height=8, wrap="word", bg="white", fg=COL_TEXT)
        self.txt_fb.grid(row=5, column=1, sticky="nsew", padx=(6, 0))

        # Botones
        btn_frame = tk.Frame(main, bg=COL_BG)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=12)

        btn_submit = tk.Button(btn_frame, text="Guardar evaluación", bg=COL_ACCENT, fg="white",
                               activebackground=COL_PANEL, command=self._on_submit)
        btn_submit.pack(side="left", ipadx=8, padx=(0, 8))

        btn_clear = tk.Button(btn_frame, text="Limpiar", bg=COL_PANEL, fg="white", command=self._clear_form)
        btn_clear.pack(side="left", ipadx=8)

        # Grid weights
        main.columnconfigure(1, weight=1)
        main.rowconfigure(1, weight=1)

        # Estado interno
        self.selected_entrega = None
        self._cargar_entregas()

        # Grid weights
        main.columnconfigure(1, weight=1)
        main.rowconfigure(2, weight=1)

    def _on_submit(self):
        if not self.selected_entrega:
            messagebox.showwarning("Validación", "Seleccione primero una entrega de la lista.")
            return

        cal = self.cal_var.get()
        fb = self.txt_fb.get("1.0", "end").strip()

        try:
            cal_val = int(cal)
            if not (0 <= cal_val <= 100):
                raise ValueError()
        except Exception:
            messagebox.showwarning("Validación", "Ingrese una calificación válida entre 0 y 100.")
            return

        if not fb:
            if not messagebox.askyesno("Confirmar", "La retroalimentación está vacía. ¿Desea guardar igual?"):
                return

        data = {
            "id_entrega": self.selected_entrega.get("id_entrega"),
            "id_tarea": self.selected_entrega.get("id_tarea"),
            "id_alumno": self.selected_entrega.get("id_alumno"),
            "calificacion": cal_val,
            "retroalimentacion": fb,
            "fecha": datetime.now().isoformat()
        }

        try:
            self._save_evaluacion(data)
            messagebox.showinfo("Guardado", "Evaluación guardada correctamente.")
            self._clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la evaluación:\n{e}")

    def _save_evaluacion(self, data):
        uploads_dir = os.path.join(os.path.dirname(__file__), "..", "uploads")
        uploads_dir = os.path.abspath(uploads_dir)
        os.makedirs(uploads_dir, exist_ok=True)
        file_path = os.path.join(uploads_dir, "evaluaciones.json")

        existing = []
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    existing = json.load(f)
                except Exception:
                    existing = []

        existing.append(data)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)

    def _clear_form(self):
        self.cal_var.set(80)
        self.txt_fb.delete("1.0", "end")
        self.selected_entrega = None
        self.lbl_selected.config(text="Ninguna entrega seleccionada")

    def _cargar_entregas(self):
      for r in self.tree_entregas.get_children():
        self.tree_entregas.delete(r)

      try:
        from config.conexion_bd import traer_entregas, alumnos_entregaron_a_tiempo
        entregas = traer_entregas()
      except Exception:
        entregas = []

      for e in entregas:
        id_entrega = e[0]
        id_tarea = e[1]
        id_alumno = e[2]
        ruta = os.path.basename(e[3]) if e[3] else ""
        fecha = str(e[4]) if e[4] else ""
        entregaron = [x[0] for x in alumnos_entregaron_a_tiempo(int(id_tarea))]
        a_tiempo = "✅ Sí" if int(id_alumno) in entregaron else "❌ No"
        self.tree_entregas.insert("", "end", iid=str(id_entrega), values=(id_entrega, id_tarea, id_alumno, ruta, fecha, a_tiempo))
        
        
        
    def _on_tree_select(self, event):
        sel = self.tree_entregas.selection()
        if not sel:
            return
        iid = sel[0]
        vals = self.tree_entregas.item(iid, "values")
        # map values back
        self.selected_entrega = {
            "id_entrega": int(vals[0]),
            "id_tarea": vals[1],
            "id_alumno": vals[2],
            "archivo": vals[3],
            "fecha": vals[4]
        }
        self.lbl_selected.config(text=f"Seleccionada: Alumno {self.selected_entrega['id_alumno']} - Tarea {self.selected_entrega['id_tarea']} (Entrega {self.selected_entrega['id_entrega']})")


def abrir_evaluacion_docente(parent=None):
    win = EvaluacionDocenteWindow(master=parent)
    return win


def main():
    app = EvaluacionDocenteApp()
    app.mainloop()


if __name__ == "__main__":
    main()
