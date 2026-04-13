import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Configuración de rutas para importaciones
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from config.conexion_bd import traer_notificaciones, marcar_notificacion_leida
from rounded_button import RoundedButton

def abrir_notificaciones_alumno(id_alumno):
    """Abre la ventana de notificaciones para un alumno específico (T5.4)."""
    ventana = tk.Toplevel()
    ventana.title("Mis Notificaciones")
    ventana.geometry("800x600")
    ventana.configure(bg="#FFFBF0", padx=20, pady=20)
    
    # --- ENCABEZADO ---
    frame_header = tk.Frame(ventana, bg="#6D4145", padx=25, pady=20)
    frame_header.pack(fill="x", pady=(0, 15))
    
    tk.Label(frame_header, text="🔔 Centro de Notificaciones", font=("Segoe UI", 22, "bold"), 
             bg="#6D4145", fg="#FFEFAE").pack(anchor="w")
    tk.Label(frame_header, text="Aquí recibirás actualizaciones sobre tus entregas y calificaciones", 
             font=("Segoe UI", 10), bg="#6D4145", fg="#F5F1E8").pack(anchor="w", pady=(5, 0))
    
    # --- BARRA DE BOTONES ---
    frame_botones = tk.Frame(ventana, bg="#FFFBF0")
    frame_botones.pack(fill="x", pady=(0, 10))
    
    def marcar_todas_como_leidas():
        """Marca todas las notificaciones no leídas como leídas."""
        notificaciones = traer_notificaciones(id_alumno)
        no_leidas = [n for n in notificaciones if n[4] == 0]  # n[4] es leida
        
        if not no_leidas:
            messagebox.showinfo("Info", "No hay notificaciones sin leer.")
            return
        
        for notif in no_leidas:
            marcar_notificacion_leida(notif[0])  # n[0] es id_notificacion
        
        messagebox.showinfo("Éxito", f"✅ {len(no_leidas)} notificación(es) marcada(s) como leída(s)")
        actualizar_notificaciones()
    
    def actualizar_notificaciones():
        """Recarga las notificaciones desde la BD."""
        # Limpiamos el frame anterior
        for widget in frame_lista.winfo_children():
            widget.destroy()
        
        notificaciones = traer_notificaciones(id_alumno)
        
        if not notificaciones:
            tk.Label(frame_lista, text="📭 No tienes notificaciones por el momento", 
                     bg="#F5F1E8", font=("Segoe UI", 12), fg="#6D4145").pack(pady=40)
        else:
            for notif in notificaciones:
                # notif: [id_notificacion, id_tarea, mensaje, fecha_creacion, leida]
                id_notificacion = notif[0]
                id_tarea = notif[1]
                mensaje = notif[2]
                fecha_creacion = notif[3]
                leida = notif[4]
                
                # Determinar estilo según si fue leída
                bg_notif = "#FFFFFF" if leida == 1 else "#FFFEF0"
                border_color = "#E0DBCF" if leida == 1 else "#FFEFAE"
                icono_leida = "✓" if leida == 1 else "●"
                color_icono = "#96D1AA" if leida == 1 else "#FF5252"
                
                # --- CARD DE NOTIFICACIÓN ---
                card = tk.Frame(frame_lista, bg=bg_notif, highlightbackground=border_color, 
                                highlightthickness=2, padx=15, pady=12)
                card.pack(fill="x", pady=8)
                
                # Header de la notificación
                header_notif = tk.Frame(card, bg=bg_notif)
                header_notif.pack(fill="x", pady=(0, 8))
                
                # Icono de lectura + ID de tarea
                tk.Label(header_notif, text=f"{icono_leida} Tarea #{id_tarea}", 
                        font=("Segoe UI", 10, "bold"), bg=bg_notif, fg=color_icono).pack(side="left")
                
                # Fecha
                fecha_str = fecha_creacion.strftime("%d/%m/%Y %H:%M") if hasattr(fecha_creacion, 'strftime') else str(fecha_creacion)
                tk.Label(header_notif, text=f"📅 {fecha_str}", 
                        font=("Segoe UI", 9), bg=bg_notif, fg="#666").pack(side="right")
                
                # Mensaje
                tk.Label(card, text=mensaje, font=("Segoe UI", 10), bg=bg_notif, 
                        fg="#333", wraplength=650, justify="left").pack(anchor="w", pady=(0, 8))
                
                # Botón para marcar como leída/no leída
                footer_notif = tk.Frame(card, bg=bg_notif)
                footer_notif.pack(fill="x")
                
                if leida == 0:
                    def marcar_leida_callback(nid=id_notificacion):
                        if marcar_notificacion_leida(nid):
                            messagebox.showinfo("Éxito", "✅ Notificación marcada como leída")
                            actualizar_notificaciones()
                        else:
                            messagebox.showerror("Error", "❌ No se pudo marcar la notificación")
                    
                    RoundedButton(footer_notif, text="✓ Marcar como leída", bg="#96D1AA", 
                                 fg="#2D4A3E", font=("Segoe UI", 9, "bold"),
                                 command=marcar_leida_callback, padx=10, pady=5).pack(side="left")
                else:
                    tk.Label(footer_notif, text="✅ Leída", font=("Segoe UI", 9, "bold"), 
                            bg=bg_notif, fg="#96D1AA").pack(side="left")
    
    RoundedButton(frame_botones, text="🔄 Actualizar", bg="#555832", fg="#FFEFAE",
                 command=actualizar_notificaciones, font=("Segoe UI", 10, "bold"),
                 padx=15, pady=8).pack(side="left", padx=5)
    
    RoundedButton(frame_botones, text="✓ Marcar todas como leídas", bg="#96D1AA", fg="#2D4A3E",
                 command=marcar_todas_como_leidas, font=("Segoe UI", 10, "bold"),
                 padx=15, pady=8).pack(side="left", padx=5)
    
    # --- ÁREA DE NOTIFICACIONES CON SCROLL ---
    container_canvas = tk.Frame(ventana, bg="#F5F1E8")
    container_canvas.pack(fill="both", expand=True)
    
    canvas = tk.Canvas(container_canvas, bg="#F5F1E8", highlightthickness=0)
    scrollbar = ttk.Scrollbar(container_canvas, orient="vertical", command=canvas.yview)
    frame_lista = tk.Frame(canvas, bg="#F5F1E8")
    
    def actualizar_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    window_id = canvas.create_window((0, 0), window=frame_lista, anchor="nw")
    
    def ajustar_ancho_frame(event):
        canvas.itemconfig(window_id, width=event.width)
    
    frame_lista.bind("<Configure>", actualizar_scrollregion)
    canvas.bind("<Configure>", ajustar_ancho_frame)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Cargar notificaciones iniciales
    actualizar_notificaciones()
    
    # Limpiar binding al cerrar
    ventana.protocol("WM_DELETE_WINDOW", lambda: [canvas.unbind_all("<MouseWheel>"), ventana.destroy()])
