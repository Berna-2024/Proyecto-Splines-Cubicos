"""Paleta y estilos de la aplicación."""

from tkinter import ttk

FONDO = "#F4F6FA"
SUPERFICIE = "#FFFFFF"
TEXTO = "#172338"
SECUNDARIO = "#64748B"
BORDE = "#E2E8F0"
PRIMARIO = "#6554C0"
PRIMARIO_OSCURO = "#51419E"
ACENTO = "#087F8C"
EXITO = "#147D60"
ERROR = "#B42338"


def configurar(root):
    root.option_add("*Font", "{Segoe UI} 10")
    estilo = ttk.Style(root)
    estilo.theme_use("clam")
    estilo.configure("TFrame", background=FONDO)
    estilo.configure("Card.TFrame", background=SUPERFICIE)
    estilo.configure("TLabel", background=FONDO, foreground=TEXTO)
    estilo.configure("TButton", font=("Segoe UI", 10), padding=(12, 8), background=SUPERFICIE,
                     foreground=TEXTO, bordercolor=BORDE, focuscolor=PRIMARIO, relief="flat")
    estilo.map("TButton", background=[("active", "#EEF0F6")], foreground=[("disabled", "#94A3B8")])
    estilo.configure("Primary.TButton", background=PRIMARIO, foreground="white", bordercolor=PRIMARIO,
                     font=("Segoe UI", 11, "bold"), padding=(14, 12))
    estilo.map("Primary.TButton", background=[("active", PRIMARIO_OSCURO), ("disabled", "#A8A0CC")])
    estilo.configure("TEntry", padding=7, fieldbackground=SUPERFICIE, foreground=TEXTO,
                     bordercolor=BORDE, lightcolor=BORDE, darkcolor=BORDE)
    estilo.map("TEntry", bordercolor=[("focus", PRIMARIO)])
    estilo.configure("TCombobox", padding=6, fieldbackground=SUPERFICIE, foreground=TEXTO,
                     bordercolor=BORDE, arrowcolor=SECUNDARIO)
    estilo.map("TCombobox", fieldbackground=[("readonly", SUPERFICIE)],
               selectbackground=[("readonly", SUPERFICIE)], selectforeground=[("readonly", TEXTO)])
    estilo.configure("TNotebook", background=FONDO, borderwidth=0, tabmargins=(0, 0, 0, 10))
    estilo.configure("TNotebook.Tab", padding=(16, 10), font=("Segoe UI", 10),
                     background=FONDO, foreground=SECUNDARIO, borderwidth=0)
    estilo.map("TNotebook.Tab", background=[("selected", SUPERFICIE)],
               foreground=[("selected", PRIMARIO)])
    estilo.configure("Treeview", background=SUPERFICIE, fieldbackground=SUPERFICIE,
                     foreground=TEXTO, rowheight=30, borderwidth=0, font=("Segoe UI", 10))
    estilo.configure("Treeview.Heading", background="#EEF1F7", foreground=SECUNDARIO,
                     relief="flat", padding=8, font=("Segoe UI", 9, "bold"))
    estilo.map("Treeview", background=[("selected", "#EDE9FA")], foreground=[("selected", TEXTO)])
    estilo.configure("Vertical.TScrollbar", background="#CFD7E4", troughcolor=FONDO,
                     borderwidth=0, arrowsize=12)
