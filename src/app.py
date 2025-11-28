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

 #----- tarjeta tab -----#
    def _build_tab_tarjetas(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Tarjetas")

        frm_form = ttk.LabelFrame(frame, text="Datos de tarjeta")
        frm_form.pack(side="top", fill="x", padx=10, pady=10)

        ttk.Label(frm_form, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_t_id = ttk.Entry(frm_form, width=10)
        self.entry_t_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frm_form, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_t_nombre = ttk.Entry(frm_form, width=30)
        self.entry_t_nombre.grid(row=1, column=1, padx=5, pady=5)

        btn_crear = ttk.Button(frm_form, text="Crear tarjeta", command=self.btn_crear_tarjeta)
        btn_crear.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        btn_actualizar = ttk.Button(frm_form, text="Actualizar nombre", command=self.btn_actualizar_tarjeta)
        btn_actualizar.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        btn_eliminar = ttk.Button(frm_form, text="Eliminar tarjeta", command=self.btn_eliminar_tarjeta)
        btn_eliminar.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        btn_refrescar = ttk.Button(frm_form, text="Refrescar lista", command=self.refrescar_tarjetas)
        btn_refrescar.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        frm_lista = ttk.LabelFrame(frame, text="Tarjetas registradas")
        frm_lista.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_tarjetas = ttk.Treeview(
            frm_lista, columns=("id", "nombre", "saldo"), show="headings"
        )
        self.tree_tarjetas.heading("id", text="ID")
        self.tree_tarjetas.heading("nombre", text="Nombre")
        self.tree_tarjetas.heading("saldo", text="Saldo")
        self.tree_tarjetas.column("id", width=60, anchor="center")
        self.tree_tarjetas.column("nombre", width=200)
        self.tree_tarjetas.column("saldo", width=80, anchor="e")
        self.tree_tarjetas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frm_lista, orient="vertical", command=self.tree_tarjetas.yview)
        self.tree_tarjetas.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.refrescar_tarjetas()

    def refrescar_tarjetas(self):
        for item in self.tree_tarjetas.get_children():
            self.tree_tarjetas.delete(item)
        for t in self.feria.listar_tarjetas():
            self.tree_tarjetas.insert("", tk.END, values=(t.id, t.nombre, f"{t.saldo:.2f}"))

    def btn_crear_tarjeta(self):
        nombre = self.entry_t_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio.")
            return
        try:
            t = self.feria.crear_tarjeta(nombre)
            messagebox.showinfo("OK", f"Tarjeta creada con ID {t.id}")
            self.entry_t_id.delete(0, tk.END)
            self.entry_t_id.insert(0, str(t.id))
            self.refrescar_tarjetas()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def btn_actualizar_tarjeta(self):
        try:
            tarjeta_id = int(self.entry_t_id.get())
        except ValueError:
            messagebox.showerror("Error", "ID inválido.")
            return
        nuevo_nombre = self.entry_t_nombre.get().strip()
        if not nuevo_nombre:
            messagebox.showerror("Error", "Nombre no puede estar vacío.")
            return
        try:
            t = self.feria.actualizar_nombre_tarjeta(tarjeta_id, nuevo_nombre)
            messagebox.showinfo("OK", f"Tarjeta {t.id} actualizada.")
            self.refrescar_tarjetas()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def btn_eliminar_tarjeta(self):
        try:
            tarjeta_id = int(self.entry_t_id.get())
        except ValueError:
            messagebox.showerror("Error", "ID inválido.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar tarjeta {tarjeta_id}?"):
            return
        try:
            self.feria.eliminar_tarjeta(tarjeta_id)
            messagebox.showinfo("OK", "Tarjeta eliminada.")
            self.entry_t_id.delete(0, tk.END)
            self.entry_t_nombre.delete(0, tk.END)
            self.refrescar_tarjetas()
        except Exception as e:
            messagebox.showerror("Error", str(e))

#---- tab depositos----#
    def _build_tab_depositos(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Depósitos")

        ttk.Label(frame, text="ID Tarjeta:").pack(pady=5)
        self.entry_dep_id = ttk.Entry(frame, width=10)
        self.entry_dep_id.pack(pady=5)

        ttk.Label(frame, text="Monto a depositar:").pack(pady=5)
        self.entry_dep_monto = ttk.Entry(frame, width=15)
        self.entry_dep_monto.pack(pady=5)

        btn_dep = ttk.Button(frame, text="Realizar depósito", command=self.btn_depositar)
        btn_dep.pack(pady=10)

    def btn_depositar(self):
        try:
            tarjeta_id = int(self.entry_dep_id.get())
            monto = float(self.entry_dep_monto.get())
        except ValueError:
            messagebox.showerror("Error", "Datos inválidos.")
            return

        try:
            t = self.feria.depositar(tarjeta_id, monto)
            messagebox.showinfo("OK", f"Depósito realizado. Nuevo saldo: {t.saldo:.2f}")
            self.refrescar_tarjetas()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---tab compras---- #
    def _build_tab_compras(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Compras")

        frm_top = ttk.LabelFrame(frame, text="Datos de compra")
        frm_top.pack(side="top", fill="x", padx=10, pady=10)

        ttk.Label(frm_top, text="ID Tarjeta:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_comp_id = ttk.Entry(frm_top, width=10)
        self.entry_comp_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frm_top, text="Tienda:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.combo_tiendas = ttk.Combobox(frm_top, state="readonly", width=25)
        self.combo_tiendas.grid(row=1, column=1, padx=5, pady=5)

        self.tiendas_cache = self.feria.listar_tiendas()
        self.combo_tiendas["values"] = [t.nombre for t in self.tiendas_cache]
        self.combo_tiendas.bind("<<ComboboxSelected>>", self.on_tienda_selected)

        frm_lista = ttk.LabelFrame(frame, text="Productos de la tienda")
        frm_lista.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_productos = ttk.Treeview(
            frm_lista, columns=("id", "nombre", "precio"), show="headings"
        )
        self.tree_productos.heading("id", text="ID")
        self.tree_productos.heading("nombre", text="Producto")
        self.tree_productos.heading("precio", text="Precio")
        self.tree_productos.column("id", width=60, anchor="center")
        self.tree_productos.column("nombre", width=250)
        self.tree_productos.column("precio", width=80, anchor="e")
        self.tree_productos.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frm_lista, orient="vertical", command=self.tree_productos.yview)
        self.tree_productos.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        frm_bottom = ttk.Frame(frame)
        frm_bottom.pack(fill="x", padx=10, pady=10)

        ttk.Label(frm_bottom, text="ID Producto a comprar:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_comp_prod_id = ttk.Entry(frm_bottom, width=10)
        self.entry_comp_prod_id.grid(row=0, column=1, padx=5, pady=5)

        btn_compra = ttk.Button(frm_bottom, text="Comprar", command=self.btn_comprar)
        btn_compra.grid(row=0, column=2, padx=10, pady=5)

    def on_tienda_selected(self, event=None):
        idx = self.combo_tiendas.current()
        if idx < 0:
            return
        tienda = self.tiendas_cache[idx]
        self._refrescar_productos(tienda.id)

    def _refrescar_productos(self, tienda_id: int):
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        productos = self.feria.listar_productos_por_tienda(tienda_id)
        for p in productos:
            self.tree_productos.insert("", tk.END, values=(p.id, p.nombre, f"{p.precio:.2f}"))

    def btn_comprar(self):
        try:
            tarjeta_id = int(self.entry_comp_id.get())
            producto_id = int(self.entry_comp_prod_id.get())
        except ValueError:
            messagebox.showerror("Error", "Datos inválidos.")
            return

        try:
            t, p = self.feria.comprar(tarjeta_id, producto_id)
            messagebox.showinfo(
                "OK",
                f"Compra realizada: {p.nombre} por {p.precio:.2f}\n"
                f"Saldo restante: {t.saldo:.2f}"
            )
            self.refrescar_tarjetas()
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    feria = Feria()
    app = FeriaAppTk(feria)
    app.mainloop()
