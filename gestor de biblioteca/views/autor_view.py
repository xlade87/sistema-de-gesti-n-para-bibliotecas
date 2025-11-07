import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from models.autor_model import AutorModel

class AutorView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        frame_form_autor = ttk.LabelFrame(self, text="Gestión de Autores", padding=10)
        frame_form_autor.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_form_autor, text="ID:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.autor_id = ttk.Entry(frame_form_autor, width=10)
        self.autor_id.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame_form_autor, text="Nombre:*").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.autor_nombre = ttk.Entry(frame_form_autor, width=30)
        self.autor_nombre.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(frame_form_autor, text="Nacionalidad:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.autor_nacionalidad = ttk.Entry(frame_form_autor, width=30)
        self.autor_nacionalidad.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(frame_form_autor, text="Fecha Nacimiento:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.autor_fecha_nacimiento = DateEntry(frame_form_autor, width=12, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.autor_fecha_nacimiento.grid(row=3, column=1, padx=5, pady=2, sticky="w")

        frame_botones_autor = ttk.Frame(frame_form_autor)
        frame_botones_autor.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(frame_botones_autor, text="Guardar", command=self.controller.guardar_autor).pack(side="left", padx=5)
        ttk.Button(frame_botones_autor, text="Eliminar", command=self.controller.eliminar_autor).pack(side="left", padx=5)
        ttk.Button(frame_botones_autor, text="Limpiar", command=self.limpiar_campos_autor).pack(side="left", padx=5)

        frame_lista_autores = ttk.LabelFrame(self, text="Lista de Autores", padding=10)
        frame_lista_autores.pack(fill="both", expand=True, padx=10, pady=5)
        columns_autores = ("ID", "Nombre", "Nacionalidad", "Fecha Nacimiento")
        self.tree_autores = ttk.Treeview(frame_lista_autores, columns=columns_autores, show="headings", height=12)
        for col in columns_autores:
            self.tree_autores.heading(col, text=col)
        self.tree_autores.column("ID", width=50)
        self.tree_autores.column("Nombre", width=200)
        self.tree_autores.column("Nacionalidad", width=120)
        self.tree_autores.column("Fecha Nacimiento", width=100)
        self.tree_autores.pack(fill="both", expand=True)

    def limpiar_campos_autor(self):
        self.autor_id.delete(0, 'end')
        self.autor_nombre.delete(0, 'end')
        self.autor_nacionalidad.delete(0, 'end')
        # Opcional: Reiniciar la fecha

    def actualizar_lista_autores(self):
        for item in self.tree_autores.get_children():
            self.tree_autores.delete(item)
        autores = AutorModel.obtener_todos()
        for autor in autores:
            fecha_formateada = autor[3].strftime("%d/%m/%Y") if autor[3] else ""
            self.tree_autores.insert("", tk.END, values=(autor[0], autor[1], autor[2] or "", fecha_formateada))