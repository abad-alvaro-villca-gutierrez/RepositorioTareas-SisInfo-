import tkinter as tk
import tkinter.font as tkfont


def _rounded_rect(canvas, x1, y1, x2, y2, radius=20, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


class RoundedButton(tk.Canvas):
    def __init__(
        self,
        master,
        text,
        command=None,
        radius=18,
        padx=18,
        pady=10,
        bg="#96D1AA",
        fg="#2D4A3E",
        activebackground=None,
        activeforeground=None,
        disabledbackground="#cfcfcf",
        disabledforeground="#888888",
        font=("Arial", 11, "bold"),
        cursor="hand2",
        state="normal",
        **kwargs,
    ):
        bg_parent = master.cget("bg") if "bg" in master.keys() else "#FFFFFF"
        
        # Calcular dimensiones iniciales basadas en el texto
        temp_font = tkfont.Font(font=font)
        text_width = temp_font.measure(text)
        text_height = temp_font.metrics("linespace")
        canvas_width = max(text_width + padx * 2, 120)
        canvas_height = text_height + pady * 2 + 4
        
        super().__init__(
            master, 
            width=canvas_width, 
            height=canvas_height, 
            highlightthickness=0, 
            bd=0, 
            bg=bg_parent, 
            cursor=cursor,
            **kwargs
        )
        
        self._text = text
        self._command = command
        self._radius = radius
        self._padx = padx
        self._pady = pady
        self._bg = bg
        self._fg = fg
        self._activebg = activebackground or bg
        self._activefg = activeforeground or fg
        self._disabledbg = disabledbackground
        self._disabledfg = disabledforeground
        self._font = tkfont.Font(font=font)
        self._state = state
        self._current_bg = self._bg
        self._current_fg = self._fg
        self._text_id = None
        self._shape_id = None

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Configure>", self._on_resize)

        self._draw()

    def _draw(self):
        self.delete("all")
        
        # Obtener dimensiones del widget de Tkinter (en píxeles)
        width = self.winfo_width()
        height = self.winfo_height()
        
        # Si el widget aún no está mapeado, usar las dimensiones por defecto
        if width < 2:
            # Recalcular basado en el texto
            text_width = self._font.measure(self._text)
            text_height = self._font.metrics("linespace")
            width = max(text_width + self._padx * 2, 120)
            height = text_height + self._pady * 2 + 4

        bg = self._disabledbg if self._state == "disabled" else self._current_bg
        fg = self._disabledfg if self._state == "disabled" else self._current_fg

        self._shape_id = _rounded_rect(self, 0, 0, width, height, radius=self._radius, fill=bg, outline="")
        self._text_id = self.create_text(width / 2, height / 2, text=self._text, font=self._font, fill=fg)

    def _on_click(self, event):
        if self._state == "disabled":
            return
        if self._command:
            self._command()

    def _on_enter(self, event):
        if self._state == "disabled":
            return
        self._current_bg = self._activebg
        self._current_fg = self._activefg
        self._draw()

    def _on_leave(self, event):
        if self._state == "disabled":
            return
        self._current_bg = self._bg
        self._current_fg = self._fg
        self._draw()

    def _on_resize(self, event):
        self._draw()

    def config(self, **kwargs):
        if "text" in kwargs:
            self._text = kwargs.pop("text")
        if "command" in kwargs:
            self._command = kwargs.pop("command")
        if "bg" in kwargs:
            self._bg = kwargs.pop("bg")
        if "fg" in kwargs:
            self._fg = kwargs.pop("fg")
        if "activebackground" in kwargs:
            self._activebg = kwargs.pop("activebackground")
        if "activeforeground" in kwargs:
            self._activefg = kwargs.pop("activeforeground")
        if "state" in kwargs:
            self._state = kwargs.pop("state")
        if kwargs:
            super().config(**kwargs)
        self._draw()

    def configure(self, **kwargs):
        self.config(**kwargs)

    def set_state(self, state):
        self._state = state
        self._draw()
