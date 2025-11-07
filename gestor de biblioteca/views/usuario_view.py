import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from utils.image_manager import ImagenManager
from utils.validators import Validaciones

class UsuarioView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.imagen_manager = ImagenManager()
        self.create_widgets()

    def create_widgets(self):
        frame_form_usuario = ttk.LabelFrame(self, text="Gestión de Usuarios", padding=10)
        frame_form_usuario.pack(fill="x", padx=10, pady=5)

        frame_izq_user = ttk.Frame(frame_form_usuario)
        frame_izq_user.pack(side="left", fill="both", expand=True)

        ttk.Label(frame_izq_user, text="ID:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.usuario_id = ttk.Entry(frame_izq_user, width=10)
        self.usuario_id.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame_izq_user, text="Nombre:*").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.usuario_nombre = ttk.Entry(frame_izq_user, width=30)
        self.usuario_nombre.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(frame_izq_user, text="Email:*").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.usuario_email = ttk.Entry(frame_izq_user, width=30)
        self.usuario_email.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(frame_izq_user, text="Teléfono:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.usuario_telefono = ttk.Entry(frame_izq_user, width=20)
        self.usuario_telefono.grid(row=3, column=1, padx=5, pady=2, sticky="w")
        vcmd = (self.winfo_toplevel().register(Validaciones.solo_numeros), '%P')
        self.usuario_telefono.configure(validate="key", validatecommand=vcmd)

        # Imagen usuario
        frame_der_user = ttk.Frame(frame_form_usuario)
        frame_der_user.pack(side="right", padx=20)

        ttk.Label(frame_der_user, text="Foto de Usuario").pack()
        self.label_imagen_usuario = tk.Label(frame_der_user, background="lightgray", width=18, height=8)
        self.label_imagen_usuario.pack(pady=5)
        frame_botones_img_user = ttk.Frame(frame_der_user)
        frame_botones_img_user.pack()
        ttk.Button(frame_botones_img_user, text="Seleccionar Foto",
                   command=self.seleccionar_imagen_usuario).pack(side="left", padx=2)
        ttk.Button(frame_botones_img_user, text="Limpiar Foto",
                   command=self.limpiar_imagen_usuario).pack(side="left", padx=2)

        # Botones usuario
        frame_botones_user = ttk.Frame(frame_izq_user)
        frame_botones_user.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(frame_botones_user, text="Guardar", command=self.controller.guardar_usuario).pack(side="left", padx=5)
        ttk.Button(frame_botones_user, text="Limpiar", command=self.limpiar_campos_usuario).pack(side="left", padx=5)

        # Lista usuarios
        frame_lista_usuarios = ttk.LabelFrame(self, text="Lista de Usuarios", padding=10)
        frame_lista_usuarios.pack(fill="both", expand=True, padx=10, pady=5)
        columns_usuarios = ("ID", "Nombre", "Email", "Teléfono")
        self.tree_usuarios = ttk.Treeview(frame_lista_usuarios, columns=columns_usuarios, show="headings", height=12)
        for col in columns_usuarios:
            self.tree_usuarios.heading(col, text=col)
        self.tree_usuarios.column("ID", width=50)
        self.tree_usuarios.column("Nombre", width=200)
        self.tree_usuarios.column("Email", width=200)
        self.tree_usuarios.column("Teléfono", width=100)
        self.tree_usuarios.pack(fill="both", expand=True)

    def seleccionar_imagen_usuario(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif")])
        if ruta:
            valido, mensaje = Validaciones.validar_imagen(ruta)
            if valido:
                imagen = self.imagen_manager.cargar_imagen_para_mostrar(ruta, (120, 120))
                if imagen:
                    self.label_imagen_usuario.config(image=imagen)
                    self.label_imagen_usuario.image = imagen
                    self.imagen_manager.ruta_usuario = ruta
                    messagebox.showinfo("Éxito", "Foto cargada correctamente")
            else:
                messagebox.showerror("Error", mensaje)

    def limpiar_imagen_usuario(self):
        self.label_imagen_usuario.config(image='')
        self.imagen_manager.ruta_usuario = None

    def limpiar_campos_usuario(self):
        self.usuario_id.delete(0, 'end')
        self.usuario_nombre.delete(0, 'end')
        self.usuario_email.delete(0, 'end')
        self.usuario_telefono.delete(0, 'end')
        self.limpiar_imagen_usuario()

    def actualizar_lista_usuarios(self):
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        usuarios = UsuarioModel.obtener_todos()
        for usuario in usuarios:
            self.tree_usuarios.insert("", tk.END, values=usuario)