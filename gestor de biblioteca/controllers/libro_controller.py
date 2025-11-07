import tkinter.messagebox as messagebox
from models.libro_model import LibroModel
from utils.validators import Validaciones

class LibroController:
    def __init__(self, view):
        self.view = view

    def guardar_libro(self):
        titulo = self.view.libro_titulo.get().strip()
        autor = self.view.libro_autor.get().strip()

        if not titulo or not autor:
            messagebox.showerror("Error", "El título y el autor son obligatorios")
            return

        año = self.view.libro_anio.get().strip()
        if año and not año.isdigit():
            messagebox.showerror("Error", "El año debe ser numérico")
            return

        params = (titulo, autor, self.view.libro_genero.get().strip(),
                  int(año) if año else None,
                  self.view.libro_isbn.get().strip())

        mensaje = LibroModel.insertar(params)
        messagebox.showinfo("Resultado", mensaje)
        self.view.limpiar_campos_libro()
        self.view.actualizar_lista_libros()

    def eliminar_libro(self):
        id_libro = self.view.libro_id.get().strip()
        if not id_libro or not id_libro.isdigit():
            messagebox.showerror("Error", "ID de libro inválido")
            return

        if not messagebox.askyesno("Confirmar", f"¿Eliminar el libro ID {id_libro}?"):
            return

        mensaje = LibroModel.eliminar(int(id_libro))
        messagebox.showinfo("Resultado", mensaje)
        self.view.limpiar_campos_libro()
        self.view.actualizar_lista_libros()

    def buscar_libro_por_id(self):
        id_libro = self.view.libro_id.get().strip()
        if not id_libro or not id_libro.isdigit():
            messagebox.showerror("Error", "Ingrese un ID válido")
            return

        libro = LibroModel.buscar_por_id(int(id_libro))
        if libro:
            self.view.libro_titulo.delete(0, 'end')
            self.view.libro_titulo.insert(0, libro[1])
            self.view.libro_autor.delete(0, 'end')
            self.view.libro_autor.insert(0, libro[2])
            self.view.libro_genero.delete(0, 'end')
            self.view.libro_genero.insert(0, libro[3] or "")
            self.view.libro_anio.delete(0, 'end')
            if libro[4]:
                self.view.libro_anio.insert(0, str(libro[4]))
            self.view.libro_isbn.delete(0, 'end')
            self.view.libro_isbn.insert(0, libro[5] or "")
        else:
            messagebox.showinfo("Búsqueda", "Libro no encontrado")