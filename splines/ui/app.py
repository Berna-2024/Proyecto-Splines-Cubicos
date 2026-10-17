"""Aplicación Tkinter: entrada, resultados, gráfica y evidencia matemática."""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

from ..ejemplos import EJEMPLOS
from ..entrada import leer_puntos, numero
from ..exportacion import grafica_svg
from ..matematica import ErrorSpline, calcular_spline
from ..presentacion import formato, informe, polinomio, procedimiento
from . import tema
from .grafica import GraficaSpline

MAX_PUNTOS = 80


def etiqueta(parent, texto, size=10, color=tema.TEXTO, negrita=False, fondo="white", **kwargs):
    return tk.Label(parent, text=texto, bg=fondo, fg=color,
                    font=("Segoe UI", size, "bold" if negrita else "normal"), **kwargs)


class AplicacionSpline(tk.Tk):
    def __init__(self, cargar_inicial=True):
        super().__init__()
        self.title("SplineLab · Splines cúbicos naturales")
        ancho = min(1380, self.winfo_screenwidth() - 70)
        alto = min(900, self.winfo_screenheight() - 85)
        self.geometry(f"{ancho}x{alto}")
        self.minsize(min(1100, ancho), min(710, alto))
        self.configure(bg=tema.FONDO)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        tema.configurar(self)
        self.spline = None
        self._cargando = False
        self.contexto = ""
        self._crear_interfaz()
        self.bind("<Control-Return>", lambda _e: self.calcular())
        if cargar_inicial:
            self.after(80, self.cargar_ejemplo)

    def _crear_interfaz(self):
        cabecera = tk.Frame(self, bg="white", padx=28, pady=18, highlightbackground=tema.BORDE,
                            highlightthickness=1)
        cabecera.grid(row=0, column=0, sticky="ew")
        etiqueta(cabecera, "S", 21, "white", True, tema.PRIMARIO, width=2).pack(side="left", padx=(0, 12))
        marca = tk.Frame(cabecera, bg="white")
        marca.pack(side="left")
        etiqueta(marca, "SplineLab", 18, negrita=True).pack(anchor="w")
        etiqueta(marca, "ÁLGEBRA LINEAL  /  INTERPOLACIÓN", 8, tema.SECUNDARIO).pack(anchor="w")
        etiqueta(cabecera, "SPLINE CÚBICO NATURAL", 9, tema.PRIMARIO, True, "#F1EEFA", padx=15, pady=9).pack(side="right")

        cuerpo = tk.Frame(self, bg=tema.FONDO)
        cuerpo.grid(row=1, column=0, sticky="nsew", padx=24, pady=(20, 10))
        cuerpo.columnconfigure(0, minsize=286)
        cuerpo.columnconfigure(1, weight=1)
        cuerpo.rowconfigure(0, weight=1)
        self._crear_entrada(cuerpo)
        principal = tk.Frame(cuerpo, bg=tema.FONDO)
        principal.grid(row=0, column=1, sticky="nsew", padx=(22, 0))
        titulo = tk.Frame(principal, bg=tema.FONDO)
        titulo.pack(fill="x", pady=(0, 16))
        textos = tk.Frame(titulo, bg=tema.FONDO)
        textos.pack(side="left", fill="x", expand=True)
        etiqueta(textos, "De puntos a curvas suaves.", 22, negrita=True, fondo=tema.FONDO).pack(anchor="w")
        etiqueta(textos, "Explora la curva y comprende cada paso del cálculo.", 10,
                 tema.SECUNDARIO, fondo=tema.FONDO).pack(anchor="w", pady=(5, 0))
        self.exportar_boton = ttk.Button(titulo, text="Exportar informe", command=self.exportar, state="disabled")
        self.exportar_boton.pack(side="right", padx=(8, 0))

        metricas = tk.Frame(principal, bg=tema.FONDO)
        metricas.pack(fill="x", pady=(0, 16))
        self.metricas = []
        for i, titulo_metrica in enumerate(("NODOS INGRESADOS", "TRAMOS CÚBICOS", "VALIDACIÓN")):
            metricas.columnconfigure(i, weight=1, uniform="metricas")
            tarjeta = tk.Frame(metricas, bg="white", padx=17, pady=12,
                               highlightbackground=tema.BORDE, highlightthickness=1)
            tarjeta.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 6, 0 if i == 2 else 6))
            etiqueta(tarjeta, titulo_metrica, 8, tema.SECUNDARIO, True).pack(anchor="w")
            valor = etiqueta(tarjeta, "—", 20, tema.PRIMARIO if i < 2 else tema.EXITO, True)
            valor.pack(anchor="w", pady=(3, 0))
            self.metricas.append(valor)

        self.pestanas = ttk.Notebook(principal)
        self.pestanas.pack(fill="both", expand=True)
        self._crear_grafica()
        self._crear_polinomios()
        self._crear_procedimiento()
        self._crear_validacion()
        pie = tk.Frame(self, bg=tema.FONDO, padx=26)
        pie.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        self.estado = etiqueta(pie, "Listo para calcular.", 9, tema.SECUNDARIO, fondo=tema.FONDO)
        self.estado.pack(side="left")
        etiqueta(pie, "SEGUNDA ENTREGA · MA331", 8, tema.SECUNDARIO, fondo=tema.FONDO).pack(side="right")

    def _crear_entrada(self, parent):
        panel = tk.Frame(parent, bg="white", padx=18, pady=20,
                         highlightbackground=tema.BORDE, highlightthickness=1, width=286)
        panel.grid(row=0, column=0, sticky="nsew")
        panel.grid_propagate(False)
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(5, weight=1)
        etiqueta(panel, "01  /  PUNTOS DE PARTIDA", 9, tema.PRIMARIO, True).grid(row=0, sticky="w")
        etiqueta(panel, "Tus datos, tu curva", 17, negrita=True).grid(row=1, sticky="w", pady=(8, 4))
        etiqueta(panel, "Carga un ejemplo o escribe tus puntos.", 9, tema.SECUNDARIO).grid(row=2, sticky="w")
        self.ejemplo = ttk.Combobox(panel, values=list(EJEMPLOS), state="readonly", width=25)
        self.ejemplo.current(0)
        self.ejemplo.grid(row=3, sticky="ew", pady=(18, 8))
        self.ejemplo.bind("<<ComboboxSelected>>", lambda _e: self.cargar_ejemplo())
        etiqueta(panel, "x ; y     ·     un punto por línea", 9, tema.SECUNDARIO, True).grid(row=4, sticky="w", pady=(8, 8))
        editor = tk.Frame(panel, bg="#F8FAFD", highlightbackground=tema.BORDE, highlightthickness=1)
        editor.grid(row=5, sticky="nsew")
        self.entrada = tk.Text(editor, width=24, height=8, wrap="none", bg="#F8FAFD", fg=tema.TEXTO,
                               insertbackground=tema.PRIMARIO, relief="flat", padx=12, pady=10,
                               font=("Consolas", 12), undo=True, highlightthickness=0)
        barra = ttk.Scrollbar(editor, orient="vertical", command=self.entrada.yview)
        barra.pack(side="right", fill="y")
        self.entrada.pack(side="left", fill="both", expand=True)
        self.entrada.configure(yscrollcommand=barra.set)
        self.entrada.bind("<<Modified>>", self._datos_modificados)
        etiqueta(panel, "Usa punto o coma decimal.\nx en orden creciente, sin repetir.", 9,
                 tema.SECUNDARIO, justify="left").grid(row=6, sticky="w", pady=(9, 12))
        acciones = tk.Frame(panel, bg="white")
        acciones.grid(row=7, sticky="ew")
        ttk.Button(acciones, text="Importar CSV", command=self.importar).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(acciones, text="Limpiar", command=self.limpiar).pack(side="left", expand=True, fill="x")
        ttk.Button(panel, text="Calcular spline  →", style="Primary.TButton",
                   command=self.calcular).grid(row=8, sticky="ew", pady=(12, 5))
        etiqueta(panel, "Ctrl + Enter para calcular · Hasta 80 puntos", 8,
                 tema.SECUNDARIO).grid(row=9, sticky="w")
        self.mensaje = etiqueta(panel, "", 9, tema.ERROR, wraplength=245, justify="left", anchor="w")
        self.mensaje.grid(row=10, sticky="ew", pady=(10, 0))
        etiqueta(panel, "FRONTERA NATURAL\nS''(x inicial) = S''(x final) = 0", 9, tema.SECUNDARIO,
                 fondo="#F5F3FB", justify="left", padx=10, pady=10).grid(row=11, sticky="ew", pady=(12, 0))

    def _nueva_pestana(self, titulo):
        frame = tk.Frame(self.pestanas, bg="white", padx=18, pady=16)
        self.pestanas.add(frame, text=titulo)
        return frame

    def _crear_grafica(self):
        frame = self._nueva_pestana("Gráfica")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(2, weight=1)
        top = tk.Frame(frame, bg="white")
        top.grid(row=0, column=0, sticky="ew")
        etiqueta(top, "Una curva continua, tramo a tramo", 12, negrita=True).pack(side="left")
        etiqueta(top, "● Nodos   ━ Spline", 9, tema.PRIMARIO).pack(side="right")
        self.contexto_label = etiqueta(frame, "", 9, tema.SECUNDARIO, anchor="w", justify="left", wraplength=720)
        self.contexto_label.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        self.grafica = GraficaSpline(frame, self._seleccionar_x)
        self.grafica.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
        etiqueta(frame, "Mueve el cursor para explorar. Haz clic para evaluar un punto.", 9,
                 tema.SECUNDARIO).grid(row=3, column=0, sticky="w", pady=(2, 15))
        consulta = tk.Frame(frame, bg="#F6F7FB", padx=14, pady=12)
        consulta.grid(row=4, column=0, sticky="ew")
        etiqueta(consulta, "Evaluar en x", 10, negrita=True, fondo="#F6F7FB").grid(row=0, column=0, sticky="w")
        self.consulta_x = ttk.Entry(consulta, width=12)
        self.consulta_x.grid(row=0, column=1, padx=10)
        self.consulta_x.bind("<Return>", lambda _e: self.evaluar())
        self.evaluar_boton = ttk.Button(consulta, text="Evaluar", command=self.evaluar, state="disabled")
        self.evaluar_boton.grid(row=0, column=2)
        consulta.columnconfigure(3, weight=1)
        self.guardar_grafica_boton = ttk.Button(consulta, text="Guardar gráfica", command=self.guardar_grafica, state="disabled")
        self.guardar_grafica_boton.grid(row=0, column=3, sticky="e", padx=(12, 0))
        self.resultado_consulta = etiqueta(consulta, "Elige un valor dentro del dominio.", 10,
                                          tema.SECUNDARIO, fondo="#F6F7FB", anchor="w")
        self.resultado_consulta.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(8, 0))

    def _tabla(self, parent, columnas, anchos):
        contenedor = tk.Frame(parent, bg="white")
        contenedor.pack(fill="both", expand=True, pady=(12, 0))
        contenedor.rowconfigure(0, weight=1)
        contenedor.columnconfigure(0, weight=1)
        tabla = ttk.Treeview(contenedor, columns=columnas, show="headings", selectmode="browse")
        for nombre, ancho in zip(columnas, anchos):
            tabla.heading(nombre, text=nombre)
            tabla.column(nombre, width=ancho, minwidth=60, anchor="w")
        vertical = ttk.Scrollbar(contenedor, orient="vertical", command=tabla.yview)
        horizontal = ttk.Scrollbar(contenedor, orient="horizontal", command=tabla.xview)
        tabla.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        tabla.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        tabla.tag_configure("par", background="#F8FAFD")
        return tabla

    def _crear_polinomios(self):
        frame = self._nueva_pestana("Polinomios")
        etiqueta(frame, "Un polinomio por intervalo", 13, negrita=True).pack(anchor="w")
        etiqueta(frame, "Sᵢ(x) = aᵢ(x − xᵢ)³ + bᵢ(x − xᵢ)² + cᵢ(x − xᵢ) + dᵢ", 11,
                 tema.SECUNDARIO).pack(anchor="w", pady=(5, 0))
        self.tabla_coef = self._tabla(frame, ("Tramo", "Intervalo", "a · cúbico", "b · cuadrático", "c · lineal", "d"),
                                     (70, 150, 130, 130, 130, 90))
        self.tabla_coef.bind("<<TreeviewSelect>>", self._ver_polinomio)
        self.expresion = tk.Text(frame, height=4, wrap="word", bg="#F5F3FB", fg=tema.PRIMARIO_OSCURO,
                                 relief="flat", padx=14, pady=12, font=("Consolas", 11), state="disabled")
        self.expresion.pack(fill="x", pady=(15, 0))
        etiqueta(frame, "Selecciona un tramo para ver su expresión. Los cálculos usan la precisión completa.",
                 9, tema.SECUNDARIO).pack(anchor="w", pady=(8, 0))

    def _crear_procedimiento(self):
        frame = self._nueva_pestana("Procedimiento")
        etiqueta(frame, "De los datos al sistema de ecuaciones", 13, negrita=True).pack(anchor="w")
        etiqueta(frame, "Distancias → sistema → Gauss → segundas derivadas → coeficientes", 10,
                 tema.SECUNDARIO).pack(anchor="w", pady=(4, 10))
        area = tk.Frame(frame, bg="white")
        area.pack(fill="both", expand=True)
        area.rowconfigure(0, weight=1)
        area.columnconfigure(0, weight=1)
        self.pasos = tk.Text(area, wrap="none", bg="#FAFBFE", fg=tema.TEXTO, relief="flat", padx=14,
                            pady=12, font=("Consolas", 10), state="disabled", highlightthickness=0)
        vertical = ttk.Scrollbar(area, orient="vertical", command=self.pasos.yview)
        horizontal = ttk.Scrollbar(area, orient="horizontal", command=self.pasos.xview)
        self.pasos.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        self.pasos.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")

    def _crear_validacion(self):
        frame = self._nueva_pestana("Validación")
        etiqueta(frame, "Resultados que se pueden comprobar", 13, negrita=True).pack(anchor="w")
        self.resumen_validacion = etiqueta(frame, "Calcula un spline para ver sus comprobaciones.", 10,
                                           tema.SECUNDARIO, justify="left", anchor="w", wraplength=760)
        self.resumen_validacion.pack(fill="x", pady=(6, 0))
        self.tabla_validacion = self._tabla(frame, ("Condición", "Error absoluto", "Límite", "Estado"), (400, 130, 130, 90))
        self.tabla_validacion.tag_configure("ok", foreground=tema.EXITO)
        self.tabla_validacion.tag_configure("error", foreground=tema.ERROR)
        etiqueta(frame, "Se verifica con valores sin redondear: error ≤ 10⁻⁸ × escala (escala ≥ 1).", 9,
                 tema.SECUNDARIO).pack(anchor="w", pady=(10, 0))

    @staticmethod
    def _texto(widget, contenido):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", contenido)
        widget.configure(state="disabled")

    def _invalidar(self):
        self.spline = None
        self.exportar_boton.configure(state="disabled")
        self.evaluar_boton.configure(state="disabled")
        self.guardar_grafica_boton.configure(state="disabled")
        for valor in self.metricas:
            valor.configure(text="—")
        for tabla in (self.tabla_coef, self.tabla_validacion):
            tabla.delete(*tabla.get_children())
        self._texto(self.expresion, "Selecciona un tramo después de calcular.")
        self._texto(self.pasos, "Calcula el spline para consultar el desarrollo matemático.")
        self.grafica.establecer(None)
        self.resultado_consulta.configure(text="Calcula el spline para evaluar un valor.", fg=tema.SECUNDARIO)
        self.resumen_validacion.configure(text="Calcula un spline para ver sus comprobaciones.", fg=tema.SECUNDARIO)

    def _datos_modificados(self, _event=None):
        if not self.entrada.edit_modified():
            return
        self.entrada.edit_modified(False)
        if self._cargando:
            return
        self.contexto = "Datos ingresados por el usuario."
        self.contexto_label.configure(text=self.contexto)
        self.mensaje.configure(text="")
        self._invalidar()
        self.estado.configure(text="Datos modificados · calcula para actualizar los resultados.")

    def _reemplazar_datos(self, texto):
        self._cargando = True
        self.entrada.delete("1.0", "end")
        self.entrada.insert("1.0", texto)
        self.entrada.edit_modified(False)
        self._cargando = False

    def cargar_ejemplo(self):
        texto, contexto = EJEMPLOS[self.ejemplo.get()]
        self._reemplazar_datos(texto)
        self.contexto = contexto
        self.calcular()

    def limpiar(self):
        self._reemplazar_datos("")
        self.contexto = "Datos ingresados por el usuario."
        self.contexto_label.configure(text=self.contexto)
        self._invalidar()
        self.mensaje.configure(text="")
        self.estado.configure(text="Escribe al menos dos puntos para comenzar.")
        self.entrada.focus_set()

    def calcular(self):
        self.mensaje.configure(text="")
        try:
            puntos = leer_puntos(self.entrada.get("1.0", "end"))
            if len(puntos) > MAX_PUNTOS:
                raise ErrorSpline(f"Esta interfaz admite hasta {MAX_PUNTOS} puntos por cálculo.")
            spline = calcular_spline(puntos)
            # Preparar también las muestras antes de publicar el resultado.
            spline.muestrear()
        except (ErrorSpline, OverflowError) as exc:
            self._invalidar()
            self.mensaje.configure(text=str(exc))
            self.estado.configure(text="Revisa los datos indicados para continuar.")
            return
        self.spline = spline
        self.metricas[0].configure(text=str(len(spline.x)))
        self.metricas[1].configure(text=str(len(spline.tramos)))
        self.metricas[2].configure(text="Verificado" if spline.valido else "Revisar",
                                  fg=tema.EXITO if spline.valido else tema.ERROR)
        self.contexto_label.configure(text=self.contexto or "Datos ingresados por el usuario.")
        self.grafica.establecer(spline)
        self.tabla_coef.delete(*self.tabla_coef.get_children())
        for i, t in enumerate(spline.tramos):
            self.tabla_coef.insert("", "end", iid=str(i), values=(f"S{i}", f"[{formato(t.inicio)}, {formato(t.fin)}]",
                                    formato(t.a), formato(t.b), formato(t.c), formato(t.d)), tags=("par",) if i % 2 == 0 else ())
        self.tabla_coef.selection_set("0")
        self._ver_polinomio()
        self._texto(self.pasos, procedimiento(spline))
        self.tabla_validacion.delete(*self.tabla_validacion.get_children())
        for i, c in enumerate(spline.comprobaciones):
            self.tabla_validacion.insert("", "end", values=(c.nombre, f"{c.error:.3e}", f"{c.limite:.3e}",
                                         "Cumple" if c.cumple else "Revisar"), tags=("ok" if c.cumple else "error",))
        cumplidas = sum(c.cumple for c in spline.comprobaciones)
        self.resumen_validacion.configure(
            text=f"{cumplidas} de {len(spline.comprobaciones)} condiciones cumplidas. "
                 f"Error absoluto máximo: {spline.error_maximo:.3e}.\n"
                 "Interpolación · continuidad de S, S' y S'' · fronteras naturales · sistema lineal.",
            fg=tema.EXITO if spline.valido else tema.ERROR)
        self.exportar_boton.configure(state="normal")
        self.evaluar_boton.configure(state="normal")
        self.guardar_grafica_boton.configure(state="normal")
        self.consulta_x.delete(0, "end")
        self.consulta_x.insert(0, formato(spline.x[0] + (spline.x[-1] - spline.x[0]) / 2, 12))
        self.resultado_consulta.configure(text=f"Dominio: [{formato(spline.x[0])}, {formato(spline.x[-1])}]. "
                                          "Ingresa x y pulsa Evaluar.", fg=tema.SECUNDARIO)
        self.estado.configure(text="Cálculo completado · todas las condiciones verificadas." if spline.valido
                              else "Cálculo completado · revisa la precisión en Validación.")

    def _ver_polinomio(self, _event=None):
        seleccion = self.tabla_coef.selection()
        if self.spline and seleccion:
            indice = int(seleccion[0])
            tramo = self.spline.tramos[indice]
            self._texto(self.expresion, polinomio(tramo, indice) +
                        f"\n\nx ∈ [{formato(tramo.inicio)}, {formato(tramo.fin)}]")

    def _seleccionar_x(self, x):
        self.consulta_x.delete(0, "end")
        self.consulta_x.insert(0, formato(x, 15))
        self.evaluar()

    def evaluar(self):
        if self.spline is None:
            return
        try:
            x = numero(self.consulta_x.get())
            indice = self.spline.indice_tramo(x)
            y = self.spline.evaluar(x)
            self.grafica.marcar(x)
            self.resultado_consulta.configure(text=f"S({formato(x)}) = {formato(y, 10)}   ·   Tramo S{indice}   ·   "
                                               f"S' = {formato(self.spline.evaluar(x, 1))}   ·   "
                                               f"S'' = {formato(self.spline.evaluar(x, 2))}", fg=tema.PRIMARIO_OSCURO)
        except ErrorSpline as exc:
            self.grafica.marcar(None)
            self.resultado_consulta.configure(text=str(exc), fg=tema.ERROR)

    def importar(self):
        ruta = filedialog.askopenfilename(title="Importar puntos x;y",
                                         filetypes=[("Puntos CSV o texto", "*.csv *.txt"), ("Todos los archivos", "*.*")])
        if not ruta:
            return
        try:
            texto = Path(ruta).read_text(encoding="utf-8-sig")
            puntos = leer_puntos(texto)
            if len(puntos) > MAX_PUNTOS:
                raise ErrorSpline(f"El archivo excede el máximo de {MAX_PUNTOS} puntos.")
        except (OSError, UnicodeError, ErrorSpline) as exc:
            self.mensaje.configure(text=f"No se pudo importar: {exc}")
            return
        self._reemplazar_datos("\n".join(f"{x:.17g}; {y:.17g}" for x, y in puntos))
        self.contexto = f"Datos importados: {Path(ruta).name}"
        self.calcular()

    def exportar(self):
        if self.spline is None:
            return
        ruta = filedialog.asksaveasfilename(title="Guardar informe de ejecución", defaultextension=".txt",
                                           initialfile="informe_spline.txt", filetypes=[("Informe de texto", "*.txt")])
        if not ruta:
            return
        try:
            Path(ruta).write_text(informe(self.spline), encoding="utf-8")
        except OSError as exc:
            self.mensaje.configure(text=f"No se pudo guardar el informe: {exc}")
            return
        self.estado.configure(text=f"Informe guardado en {ruta}")

    def guardar_grafica(self):
        if self.spline is None:
            return
        ruta = filedialog.asksaveasfilename(title="Guardar gráfica para el informe", defaultextension=".svg",
                                           initialfile="grafica_spline.svg", filetypes=[("Gráfica vectorial", "*.svg")])
        if not ruta:
            return
        try:
            Path(ruta).write_text(grafica_svg(self.spline), encoding="utf-8")
        except (OSError, ErrorSpline) as exc:
            self.mensaje.configure(text=f"No se pudo guardar la gráfica: {exc}")
            return
        self.estado.configure(text=f"Gráfica guardada en {ruta}")


def iniciar():
    app = AplicacionSpline()
    app.mainloop()
