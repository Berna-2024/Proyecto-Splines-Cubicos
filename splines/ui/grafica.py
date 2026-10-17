"""Gráfica en Canvas. Las muestras se obtienen del polinomio propio."""

import tkinter as tk

from . import tema


class GraficaSpline(tk.Canvas):
    def __init__(self, parent, al_seleccionar=None):
        super().__init__(parent, background="white", highlightthickness=0, height=320)
        self.spline = None
        self.muestra = []
        self.seleccion = None
        self.al_seleccionar = al_seleccionar
        self.zona = None
        self._pendiente = None
        self.bind("<Configure>", self._redimensionar)
        self.bind("<Motion>", self._mover)
        self.bind("<Leave>", lambda _e: self.delete("cursor"))
        self.bind("<Button-1>", self._clic)

    def _redimensionar(self, _event):
        if self._pendiente:
            self.after_cancel(self._pendiente)
        self._pendiente = self.after(60, self.dibujar)

    def establecer(self, spline):
        self.spline = spline
        self.muestra = spline.muestrear() if spline else []
        self.seleccion = None
        self.dibujar()

    def marcar(self, x):
        self.seleccion = x
        self.dibujar()

    def _pantalla(self, x, y):
        izquierda, arriba, derecha, abajo, xmin, xmax, ymin, ymax = self.zona
        return (izquierda + (x - xmin) * (derecha - izquierda) / (xmax - xmin),
                abajo - (y - ymin) * (abajo - arriba) / (ymax - ymin))

    def dibujar(self):
        self._pendiente = None
        self.delete("all")
        ancho, alto = self.winfo_width(), self.winfo_height()
        self.zona = None
        if not self.spline or ancho < 150 or alto < 120:
            self.create_text(ancho / 2, alto / 2, text="Ingresa tus puntos y calcula el spline.",
                             fill=tema.SECUNDARIO, font=("Segoe UI", 12))
            return
        xmin, xmax = self.spline.x[0], self.spline.x[-1]
        ys = [p[1] for p in self.muestra] + list(self.spline.y)
        ymin, ymax = min(ys), max(ys)
        margen = (ymax - ymin) * .12 if ymax != ymin else max(1, abs(ymin) * .12)
        ymin, ymax = ymin - margen, ymax + margen
        self.zona = (76, 24, ancho - 25, alto - 46, xmin, xmax, ymin, ymax)
        izquierda, arriba, derecha, abajo = self.zona[:4]
        for j in range(6):
            y = ymin + (ymax - ymin) * j / 5
            _, py = self._pantalla(xmin, y)
            self.create_line(izquierda, py, derecha, py, fill="#EBEEF5")
            self.create_text(izquierda - 12, py, text=f"{y:.4g}", anchor="e",
                             fill=tema.SECUNDARIO, font=("Segoe UI", 9))
            x = xmin + (xmax - xmin) * j / 5
            px, _ = self._pantalla(x, ymin)
            self.create_line(px, arriba, px, abajo, fill="#F1F3F8")
            self.create_text(px, abajo + 19, text=f"{x:.4g}", fill=tema.SECUNDARIO,
                             font=("Segoe UI", 9))
        self.create_line(izquierda, arriba, izquierda, abajo, derecha, abajo, fill="#C9D2E2")
        self.create_text(izquierda - 13, arriba - 12, text="y", fill=tema.SECUNDARIO)
        self.create_text(derecha + 9, abajo + 1, text="x", fill=tema.SECUNDARIO)
        if ymin < 0 < ymax:
            _, py = self._pantalla(xmin, 0)
            self.create_line(izquierda, py, derecha, py, fill="#B9C5D6", dash=(4, 5))
        coords = [self._pantalla(x, y) for x, y in self.muestra]
        plana = [v for punto in coords for v in punto]
        self.create_polygon(izquierda, abajo, *plana, derecha, abajo, fill="#F4F1FC", outline="")
        self.create_line(*plana, fill=tema.PRIMARIO, width=3, capstyle="round", joinstyle="round")
        for x, y in zip(self.spline.x, self.spline.y):
            px, py = self._pantalla(x, y)
            self.create_oval(px - 5, py - 5, px + 5, py + 5, fill=tema.ACENTO, outline="white", width=2)
        if self.seleccion is not None:
            self._indicador(self.seleccion, "seleccion", "#C47A16")

    def _indicador(self, x, etiqueta, color):
        y = self.spline.evaluar(x)
        px, py = self._pantalla(x, y)
        izquierda, arriba, derecha, abajo = self.zona[:4]
        self.create_line(px, arriba, px, abajo, fill=color, dash=(3, 4), tags=etiqueta)
        self.create_oval(px - 6, py - 6, px + 6, py + 6, fill="white", outline=color, width=2, tags=etiqueta)
        label_x = max(izquierda + 92, min(px, derecha - 92))
        self.create_rectangle(label_x - 90, arriba + 2, label_x + 90, arriba + 28,
                              fill="white", outline=tema.BORDE, tags=etiqueta)
        self.create_text(label_x, arriba + 15, text=f"x = {x:.5g}    S(x) = {y:.6g}",
                         fill=tema.TEXTO, font=("Segoe UI", 9), tags=etiqueta)

    def _x_evento(self, evento):
        if not self.zona:
            return None
        izquierda, arriba, derecha, abajo, xmin, xmax, _, _ = self.zona
        if izquierda <= evento.x <= derecha and arriba <= evento.y <= abajo:
            return xmin + (evento.x - izquierda) * (xmax - xmin) / (derecha - izquierda)
        return None

    def _mover(self, evento):
        self.delete("cursor")
        x = self._x_evento(evento)
        if x is not None:
            self._indicador(x, "cursor", tema.SECUNDARIO)

    def _clic(self, evento):
        x = self._x_evento(evento)
        if x is not None and self.al_seleccionar:
            self.al_seleccionar(x)
