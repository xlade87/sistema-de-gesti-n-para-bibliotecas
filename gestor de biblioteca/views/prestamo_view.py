import tkinter as tk
from tkinter import ttk, messagebox
from utils.validators import Validaciones

class PrestamoView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        frame_prestamo = ttk.LabelFrame(self, text="Realizar Préstamo", padding=10)
        frame_prestamo.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_prestamo, text="ID Libro:*").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.prestamo_libro_id = ttk.Entry(frame_prestamo, width=10)
        self.prestamo_libro_id.grid(row=0, column=1, padx=5, pady=2)
        vcmd = (self.winfo_toplevel().register(Validaciones.solo_numeros), '%P')
        self.prestamo_libro_id.configure(validate="key", validatecommand=vcmd)

        ttk.Label(frame_prestamo, text="ID Usuario:*").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.prestamo_usuario_id = ttk.Entry(frame_prestamo, width=10)
        self.prestamo_usuario_id.grid(row=0, column=3, padx=5, pady=2)
        self.prestamo_usuario_id.configure(validate="key", validatecommand=vcmd)

        ttk.Button(frame_prestamo, text="Realizar Préstamo", command=self.controller.realizar_prestamo).grid(row=0, column=4, padx=10)

        frame_devolucion = ttk.LabelFrame(self, text="Devolver Libro", padding=10)
        frame_devolucion.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_devolucion, text="ID Préstamo:*").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.devolucion_id = ttk.Entry(frame_devolucion, width=10)
        self.devolucion_id.grid(row=0, column=1, padx=5, pady=2)
        self.devolucion_id.configure(validate="key", validatecommand=vcmd)

        ttk.Button(frame_devolucion, text="Devolver Libro", command=self.controller.devolver_libro).grid(row=0, column=2, padx=10)

        frame_lista_prestamos = ttk.LabelFrame(self, text="Préstamos Activos", padding=10)
        frame_lista_prestamos.pack(fill="both", expand=True, padx=10, pady=5)
        columns_prestamos = ("ID", "Libro", "Usuario", "Fecha Préstamo", "Devuelto")
        self.tree_prestamos = ttk.Treeview(frame_lista_prestamos, columns=columns_prestamos, show="headings", height=12)
        for col in columns_prestamos:
            self.tree_prestamos.heading(col, text=col)
        self.tree_prestamos.column("ID", width=50)
        self.tree_prestamos.column("Libro", width=200)
        self.tree_prestamos.column("Usuario", width=150)
        self.tree_prestamos.column("Fecha Préstamo", width=100)
        self.tree_prestamos.column("Devuelto", width=80)
        self.tree_prestamos.pack(fill="both", expand=True)

    def actualizar_lista_prestamos(self):
        for item in self.tree_prestamos.get_children():
            self.tree_prestamos.delete(item)
        prestamos = PrestamoModel.obtener_todos()
        for prestamo in prestamos:
            self.tree_prestamos.insert("", tk.END, values=prestamo)

    
    def actualizar_listas_dependientes(self):
        pass