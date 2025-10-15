"""
SISTEMA DE GESTIÓN DE BIBLIOTECA
Sistema completo para gestión de biblioteca con 4 módulos
Implementando CRUD con MySQL y Tkinter usando POO
"""

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# CLASE PARA MANEJAR LA CONEXIÓN A LA BASE DE DATOS
class DatabaseConnection:
    # Esta clase se encarga de conectar con la base de datos MySQL
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        # Intenta conectar a la base de datos
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                database="biblioteca_personal",
                user="root",
                password="",
                autocommit=True
            )
            self.cursor = self.connection.cursor(buffered=True)
            return True
        except mysql.connector.Error as error:
            messagebox.showerror("Error de Conexión", f"Error conectando: {error}")
            return False

    def disconnect(self):
        # Cierra la conexión cuando termina el programa
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, parameters=None):
        # Ejecuta cualquier consulta SQL (INSERT, UPDATE, DELETE, SELECT)
        try:
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)

            # Si es SELECT, devuelve los resultados
            if query.strip().upper().startswith('SELECT'):
                return True, self.cursor.fetchall()
            else:
                # Si es INSERT/UPDATE/DELETE, confirma los cambios
                self.connection.commit()
                return True, "Operación exitosa"
        except mysql.connector.Error as error:
            return False, str(error)


# CLASE PADRE PARA TODAS LAS ENTIDADES (LIBROS, USUARIOS, ETC.)
class EntidadBase:
    # Clase base que comparten todos los objetos del sistema
    def __init__(self, id=None):
        self.id = id
        self.db = DatabaseConnection()


# CLASE PARA MANEJAR LIBROS - HEREDA DE ENTIDADBASE
class Libro(EntidadBase):
    # Representa un libro en el sistema
    def __init__(self, id=None, titulo="", autor="", genero="", año_publicacion=None, isbn=""):
        super().__init__(id)
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.año_publicacion = año_publicacion
        self.isbn = isbn

    def guardar(self):
        # Guarda el libro en la base de datos (CREATE)
        if not self.db.connection and not self.db.connect():
            return False

        # Valida que tenga título y autor
        if not self.titulo or not self.autor:
            messagebox.showerror("Error", "Título y autor son obligatorios")
            return False

        try:
            # Si tiene ID, actualiza; si no, inserta nuevo
            if self.id:
                query = """UPDATE libros SET titulo=%s, autor=%s, genero=%s, 
                          año_publicacion=%s, isbn=%s WHERE id=%s"""
                params = (self.titulo, self.autor, self.genero, self.año_publicacion, self.isbn, self.id)
            else:
                query = """INSERT INTO libros (titulo, autor, genero, año_publicacion, isbn) 
                          VALUES (%s, %s, %s, %s, %s)"""
                params = (self.titulo, self.autor, self.genero, self.año_publicacion, self.isbn)

            success, result = self.db.execute_query(query, params)

            if success:
                messagebox.showinfo("Éxito", f"Libro '{self.titulo}' guardado")
                return True
            else:
                messagebox.showerror("Error", f"Error al guardar: {result}")
                return False
        except ValueError:
            messagebox.showerror("Error", "El año debe ser un número válido")
            return False

    def eliminar(self):
        # Elimina el libro de la base de datos (DELETE)
        if not self.id:
            messagebox.showerror("Error", "ID de libro inválido")
            return False

        # Pide confirmación antes de eliminar
        if not messagebox.askyesno("Confirmar", f"¿Eliminar el libro '{self.titulo}'?"):
            return False

        query = "DELETE FROM libros WHERE id = %s"
        success, result = self.db.execute_query(query, (self.id,))

        if success:
            messagebox.showinfo("Éxito", "Libro eliminado correctamente")
            return True
        else:
            messagebox.showerror("Error", f"Error al eliminar: {result}")
            return False

    def buscar_por_id(self, id):
        # Busca un libro por su ID (READ)
        if not self.db.connection and not self.db.connect():
            return None

        query = "SELECT * FROM libros WHERE id = %s"
        success, result = self.db.execute_query(query, (id,))

        if success and result:
            libro_data = result[0]
            # Crea y devuelve un objeto Libro con los datos encontrados
            return Libro(
                id=libro_data[0],
                titulo=libro_data[1],
                autor=libro_data[2],
                genero=libro_data[3],
                año_publicacion=libro_data[4],
                isbn=libro_data[5]
            )
        return None

    @staticmethod
    def obtener_todos():
        # Obtiene todos los libros de la base de datos
        db = DatabaseConnection()
        if not db.connection and not db.connect():
            return []

        query = "SELECT id, titulo, autor, genero, año_publicacion, isbn FROM libros ORDER BY titulo"
        success, result = db.execute_query(query)

        libros = []
        if success:
            for libro_data in result:
                # Crea una lista de objetos Libro
                libros.append(Libro(
                    id=libro_data[0],
                    titulo=libro_data[1],
                    autor=libro_data[2],
                    genero=libro_data[3],
                    año_publicacion=libro_data[4],
                    isbn=libro_data[5]
                ))
        return libros


# CLASE PRINCIPAL DE LA APLICACIÓN
class BibliotecaApp:
    # Maneja toda la interfaz gráfica y coordina las operaciones
    def __init__(self, root):
        self.root = root
        self.db = DatabaseConnection()
        self.crear_interfaz()

    def crear_interfaz(self):
        # Crea la ventana principal con pestañas
        self.root.title("Sistema de Gestión de Biblioteca")
        self.root.geometry("1100x750")

        # Crea las pestañas para cada módulo
        self.notebook = ttk.Notebook(self.root)

        self.tab_libros = ttk.Frame(self.notebook)
        self.tab_usuarios = ttk.Frame(self.notebook)
        self.tab_prestamos = ttk.Frame(self.notebook)
        self.tab_autores = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_libros, text=" Libros")
        self.notebook.add(self.tab_usuarios, text=" Usuarios")
        self.notebook.add(self.tab_prestamos, text=" Préstamos")
        self.notebook.add(self.tab_autores, text=" Autores")

        self.notebook.pack(expand=True, fill="both")

        # Configura cada módulo
        self.configurar_modulo_libros()

    def configurar_modulo_libros(self):
        # Configura la interfaz del módulo de libros
        frame_form_libro = ttk.LabelFrame(self.tab_libros, text="Gestión de Libros", padding=10)
        frame_form_libro.pack(fill="x", padx=10, pady=5)

        # Campos para ingresar datos del libro
        ttk.Label(frame_form_libro, text="ID:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.libro_id = ttk.Entry(frame_form_libro, width=10)
        self.libro_id.grid(row=0, column=1, padx=5, pady=2)

        ttk.Button(frame_form_libro, text="Buscar por ID", command=self.buscar_libro_por_id).grid(row=0, column=2,
                                                                                                  padx=5)

        ttk.Label(frame_form_libro, text="Título:*").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.libro_titulo = ttk.Entry(frame_form_libro, width=40)
        self.libro_titulo.grid(row=1, column=1, padx=5, pady=2, columnspan=2)

        ttk.Label(frame_form_libro, text="Autor:*").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.libro_autor = ttk.Entry(frame_form_libro, width=40)
        self.libro_autor.grid(row=2, column=1, padx=5, pady=2, columnspan=2)

        ttk.Label(frame_form_libro, text="Género:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.libro_genero = ttk.Entry(frame_form_libro, width=40)
        self.libro_genero.grid(row=3, column=1, padx=5, pady=2, columnspan=2)

        ttk.Label(frame_form_libro, text="Año:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
        self.libro_anio = ttk.Entry(frame_form_libro, width=10)
        self.libro_anio.grid(row=4, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(frame_form_libro, text="ISBN:").grid(row=4, column=2, padx=5, pady=2, sticky="w")
        self.libro_isbn = ttk.Entry(frame_form_libro, width=20)
        self.libro_isbn.grid(row=4, column=3, padx=5, pady=2)

        # Botones para acciones
        frame_botones_libro = ttk.Frame(frame_form_libro)
        frame_botones_libro.grid(row=5, column=0, columnspan=4, pady=10)
        ttk.Button(frame_botones_libro, text=" Guardar", command=self.guardar_libro).pack(side="left", padx=5)
        ttk.Button(frame_botones_libro, text=" Eliminar", command=self.eliminar_libro).pack(side="left", padx=5)
        ttk.Button(frame_botones_libro, text=" Limpiar", command=self.limpiar_libro).pack(side="left", padx=5)

        # Tabla para mostrar la lista de libros
        frame_lista_libros = ttk.LabelFrame(self.tab_libros, text="Lista de Libros", padding=10)
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

    def limpiar_libro(self):
        # Limpia todos los campos del formulario
        self.libro_id.delete(0, tk.END)
        self.libro_titulo.delete(0, tk.END)
        self.libro_autor.delete(0, tk.END)
        self.libro_genero.delete(0, tk.END)
        self.libro_anio.delete(0, tk.END)
        self.libro_isbn.delete(0, tk.END)

    def guardar_libro(self):
        # Usa la clase Libro para guardar los datos
        libro = Libro(
            id=self.libro_id.get().strip() or None,
            titulo=self.libro_titulo.get().strip(),
            autor=self.libro_autor.get().strip(),
            genero=self.libro_genero.get().strip(),
            año_publicacion=int(self.libro_anio.get()) if self.libro_anio.get().strip() else None,
            isbn=self.libro_isbn.get().strip()
        )

        if libro.guardar():
            self.limpiar_libro()
            self.actualizar_lista_libros()

    def eliminar_libro(self):
        # Usa la clase Libro para eliminar
        id_libro = self.libro_id.get().strip()
        if not id_libro or not id_libro.isdigit():
            messagebox.showerror("Error", "ID de libro inválido")
            return

        libro = Libro(id=int(id_libro))
        if libro.eliminar():
            self.limpiar_libro()
            self.actualizar_lista_libros()

    def buscar_libro_por_id(self):
        # Busca un libro usando la clase Libro
        id_libro = self.libro_id.get().strip()
        if not id_libro or not id_libro.isdigit():
            messagebox.showerror("Error", "Ingrese un ID válido")
            return

        libro = Libro().buscar_por_id(int(id_libro))
        if libro:
            # Llena los campos con los datos del libro encontrado
            self.libro_titulo.delete(0, tk.END)
            self.libro_titulo.insert(0, libro.titulo)
            self.libro_autor.delete(0, tk.END)
            self.libro_autor.insert(0, libro.autor)
            self.libro_genero.delete(0, tk.END)
            self.libro_genero.insert(0, libro.genero or "")
            self.libro_anio.delete(0, tk.END)
            if libro.año_publicacion:
                self.libro_anio.insert(0, str(libro.año_publicacion))
            self.libro_isbn.delete(0, tk.END)
            self.libro_isbn.insert(0, libro.isbn or "")
        else:
            messagebox.showinfo("Búsqueda", "Libro no encontrado")

    def actualizar_lista_libros(self):
        # Actualiza la tabla con todos los libros
        for item in self.tree_libros.get_children():
            self.tree_libros.delete(item)

        libros = Libro.obtener_todos()
        for libro in libros:
            self.tree_libros.insert("", tk.END, values=(
                libro.id, libro.titulo, libro.autor, libro.genero or "",
                libro.año_publicacion or ""
            ))

    def cargar_datos_iniciales(self):
        # Carga los datos al iniciar la aplicación
        if self.db.connect():
            self.actualizar_lista_libros()
            messagebox.showinfo("Listo", "Conectado a la base de datos")
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")

    def on_closing(self):
        # Cierra la conexión al salir
        self.db.disconnect()
        self.root.destroy()


# INICIO DEL PROGRAMA
if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)

    # Configura qué hacer al cerrar la ventana
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    # Carga los datos después de 100ms
    root.after(100, app.cargar_datos_iniciales)
    # Inicia la aplicación
    root.mainloop()