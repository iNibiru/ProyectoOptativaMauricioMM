# app_gui.py
import tkinter as tk
from tkinter import ttk, messagebox

from feria import Feria

class FeriaAppTk(tk.Tk):
    def __init__(self, feria: Feria):
        super().__init__()
        self.feria = feria

        self.title("Feria - Tarjeta Prepago")
        self.geometry("850x500")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self._build_tab_tarjetas()
        self._build_tab_depositos()
        self._build_tab_compras()

