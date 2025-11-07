import tkinter.messagebox as messagebox
from models.prestamo_model import PrestamoModel

class PrestamoController:
    def __init__(self, view):
        self.view = view

    def realizar_prestamo(self):
        libro_id_val = self.view.prestamo_libro_id.get().strip()
        usuario_id_val = self.view.prestamo_usuario_id.get().strip()

        if not libro_id_val or not libro_id_val.isdigit():
            messagebox.showerror("Error", "ID de libro inválido")
            return
        if not usuario_id_val or not usuario_id_val.isdigit():
            messagebox.showerror("Error", "ID de usuario inválido")
            return

        if not messagebox.askyesno("Confirmar", "¿Realizar el préstamo?"):
            return

        mensaje = PrestamoModel.realizar((int(libro_id_val), int(usuario_id_val)))
        messagebox.showinfo("Resultado", mensaje)
        self.view.prestamo_libro_id.delete(0, 'end')
        self.view.prestamo_usuario_id.delete(0, 'end')
        self.view.actualizar_lista_prestamos()
        # Opcional: Actualizar lista de libros si cambia disponibilidad
        # self.view.actualizar_listas_dependientes()

    def devolver_libro(self):
        prestamo_id = self.view.devolucion_id.get().strip()
        if not prestamo_id or not prestamo_id.isdigit():
            messagebox.showerror("Error", "ID de préstamo inválido")
            return

        if not messagebox.askyesno("Confirmar", "¿Realizar la devolución?"):
            return

        mensaje = PrestamoModel.devolver(int(prestamo_id))
        messagebox.showinfo("Resultado", mensaje)
        self.view.devolucion_id.delete(0, 'end')
        self.view.actualizar_lista_prestamos()
        # Opcional: Actualizar lista de libros si cambia disponibilidad
        # self.view.actualizar_listas_dependientes()