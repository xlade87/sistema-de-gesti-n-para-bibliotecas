import tkinter.messagebox as messagebox
from models.autor_model import AutorModel

class AutorController:
    def __init__(self, view):
        self.view = view

    def guardar_autor(self):
        nombre = self.view.autor_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre del autor es obligatorio")
            return

        params = (nombre, self.view.autor_nacionalidad.get().strip() or None,
                  self.view.autor_fecha_nacimiento.get_date())

        mensaje = AutorModel.insertar(params)
        messagebox.showinfo("Resultado", mensaje)
        self.view.limpiar_campos_autor()
        self.view.actualizar_lista_autores()

    def eliminar_autor(self):
        id_autor = self.view.autor_id.get().strip()
        if not id_autor or not id_autor.isdigit():
            messagebox.showerror("Error", "ID de autor inválido")
            return

        if not messagebox.askyesno("Confirmar", f"¿Eliminar el autor ID {id_autor}?"):
            return

        mensaje = AutorModel.eliminar(int(id_autor))
        messagebox.showinfo("Resultado", mensaje)
        self.view.limpiar_campos_autor()
        self.view.actualizar_lista_autores()