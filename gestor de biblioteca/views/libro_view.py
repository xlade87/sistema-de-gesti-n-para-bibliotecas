import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from utils.image_manager import ImagenManager
from utils.validators import Validaciones
from tkcalendar import DateEntry

class LibroView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.imagen_manager = ImagenManager()
        self.create_widgets()

    def create_widgets(self):
        frame_form_libro = ttk.LabelFrame(self, text="Gestión de Libros", padding=10)
        frame_form_libro.pack(fill="x", padx=10, pady=5)

        frame_izq = ttk.Frame(frame_form_libro)
        frame_izq.pack(side="left", fill="both", expand=True)

        ttk.Label(frame_izq, text="ID:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.libro_id = ttk.Entry(frame_izq, width=10)
        self.libro_id.grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(frame_izq, text="Buscar por ID", command=self.controller.buscar_libro_por_id).grid(row=0, column=2, padx=5)

        ttk.Label(frame_izq, text="Título:*").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.libro_titulo = ttk.Entry(frame_izq, width=30)
        self.libro_titulo.grid(row=1, column=1, padx=5, pady=2, columnspan=2)

        ttk.Label(frame_izq, text="Autor:*").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.libro_autor = ttk.Entry(frame_izq, width=30)
        self.libro_autor.grid(row=2, column=1, padx=5, pady=2, columnspan=2)

        ttk.Label(frame_izq, text="Género:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.libro_genero = ttk.Entry(frame_izq, width=30)
        self.libro_genero.grid(row=3, column=1, padx=5, pady=2, columnspan=2)

        ttk.Label(frame_izq, text="Año:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.libro_anio = ttk.Entry(frame_izq, width=10)
        self.libro_anio.grid(row=4, column=1, padx=5, pady=2, sticky="w")
        vcmd = (self.winfo_toplevel().register(Validaciones.solo_numeros), '%P')
        self.libro_anio.configure(validate="key", validatecommand=vcmd)

        ttk.Label(frame_izq, text="ISBN:").grid(row=4, column=2, padx=5, pady=2, sticky="w")
        self.libro_isbn = ttk.Entry(frame_izq, width=20)
        self.libro_isbn.grid(row=4, column=3, padx=5, pady=2)

        # Imagen
        frame_der = ttk.Frame(frame_form_libro)
        frame_der.pack(side="right", padx=20)

        ttk.Label(frame_der, text="Portada del Libro").pack()
        self.label_imagen_libro = tk.Label(frame_der, background="lightgray", width=20, height=10)
        self.label_imagen_libro.pack(pady=5)
        frame_botones_img = ttk.Frame(frame_der)
        frame_botones_img.pack()
        ttk.Button(frame_botones_img, text="Seleccionar Imagen",
                   command=self.seleccionar_imagen_libro).pack(side="left", padx=2)
        ttk.Button(frame_botones_img, text="Limpiar Imagen",
                   command=self.limpiar_imagen_libro).pack(side="left", padx=2)

        # Botones
        frame_botones = ttk.Frame(frame_izq)
        frame_botones.grid(row=5, column=0, columnspan=4, pady=10)
        ttk.Button(frame_botones, text="Guardar", command=self.controller.guardar_libro).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Eliminar", command=self.controller.eliminar_libro).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Limpiar", command=self.limpiar_campos_libro).pack(side="left", padx=5)

        # Lista
        frame_lista_libros = ttk.LabelFrame(self, text="Lista de Libros", padding=10)
        frame_lista_libros.pack(fill="both", expand=True, padx=10, pady=5)
        columns_libros = ("ID", "Título", "Autor", "Género", "Año")
        self.tree_libros = ttk.Treeview(frame_lista_libros, columns=columns_libros, show="headings", height=12)
        for col in columns_libros:
            self.tree_libros.heading(col, text=col)
        self.tree_libros.column("ID", width=50)
        self.tree_libros.column("Título", width=250)
        self.tree_libros.column("Autor", width=150)
        self.tree_libros.column("Género", width=100)
        self.tree_libros.column("Año", width=80)
        self.tree_libros.pack(fill="both", expand=True)

    def seleccionar_imagen_libro(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif")])
        if ruta:
            valido, mensaje = Validaciones.validar_imagen(ruta)
            if valido:
                imagen = self.imagen_manager.cargar_imagen_para_mostrar(ruta)
                if imagen:
                    self.label_imagen_libro.config(image=imagen)
                    self.label_imagen_libro.image = imagen
                    self.imagen_manager.ruta_actual = ruta
                    messagebox.showinfo("Éxito", "Imagen cargada correctamente")
            else:
                messagebox.showerror("Error", mensaje)

    def limpiar_imagen_libro(self):
        self.label_imagen_libro.config(image='')
        self.imagen_manager.ruta_actual = None

    def limpiar_campos_libro(self):
        self.libro_id.delete(0, 'end')
        self.libro_titulo.delete(0, 'end')
        self.libro_autor.delete(0, 'end')
        self.libro_genero.delete(0, 'end')
        self.libro_anio.delete(0, 'end')
        self.libro_isbn.delete(0, 'end')
        self.limpiar_imagen_libro()

    def actualizar_lista_libros(self):
        for item in self.tree_libros.get_children():
            self.tree_libros.delete(item)
        libros = LibroModel.obtener_todos()
        for libro in libros:
            self.tree_libros.insert("", tk.END, values=libro)