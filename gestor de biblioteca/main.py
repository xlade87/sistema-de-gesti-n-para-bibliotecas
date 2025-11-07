import tkinter as tk
from tkinter import ttk, messagebox
from views.libro_view import LibroView
from views.usuario_view import UsuarioView
from views.prestamo_view import PrestamoView
from views.autor_view import AutorView
from controllers.libro_controller import LibroController
from controllers.usuario_controller import UsuarioController
from controllers.prestamo_controller import PrestamoController
from controllers.autor_controller import AutorController
from config.database import db

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Biblioteca")
        self.root.geometry("1200x800")
        self.root.configure(bg='white')

        try:
            self.root.iconbitmap("favicon.ico")
        except:
            pass

        # Crear vistas
        self.libro_view = LibroView(None, None)
        self.usuario_view = UsuarioView(None, None)
        self.prestamo_view = PrestamoView(None, None)
        self.autor_view = AutorView(None, None)

        # Crear controllers y enlazar con vistas
        self.libro_controller = LibroController(self.libro_view)
        self.usuario_controller = UsuarioController(self.usuario_view)
        self.prestamo_controller = PrestamoController(self.prestamo_view)
        self.autor_controller = AutorController(self.autor_view)

        # Asignar controllers a las vistas (necesario para que las vistas llamen al controlador)
        self.libro_view.controller = self.libro_controller
        self.usuario_view.controller = self.usuario_controller
        self.prestamo_view.controller = self.prestamo_controller
        self.autor_view.controller = self.autor_controller

        # Crear pestañas
        self.notebook = ttk.Notebook(root)

        self.tab_libros = self.libro_view
        self.tab_libros.parent = self.notebook
        self.notebook.add(self.tab_libros, text="Libros")

        self.tab_usuarios = self.usuario_view
        self.tab_usuarios.parent = self.notebook
        self.notebook.add(self.tab_usuarios, text="Usuarios")

        self.tab_prestamos = self.prestamo_view
        self.tab_prestamos.parent = self.notebook
        self.notebook.add(self.tab_prestamos, text="Préstamos")

        self.tab_autores = self.autor_view
        self.tab_autores.parent = self.notebook
        self.notebook.add(self.tab_autores, text="Autores")

        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        # Cargar datos iniciales
        self.cargar_datos_iniciales()

    def cargar_datos_iniciales(self):
        if db.connect():
            self.libro_view.actualizar_lista_libros()
            self.usuario_view.actualizar_lista_usuarios()
            self.prestamo_view.actualizar_lista_prestamos()
            self.autor_view.actualizar_lista_autores()
            messagebox.showinfo("Listo", "Sistema cargado correctamente")
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")

    def on_closing(self):
        db.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()