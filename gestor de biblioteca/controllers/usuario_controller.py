import tkinter.messagebox as messagebox
from models.usuario_model import UsuarioModel
from utils.validators import Validaciones

class UsuarioController:
    def __init__(self, view):
        self.view = view

    def guardar_usuario(self):
        nombre = self.view.usuario_nombre.get().strip()
        email = self.view.usuario_email.get().strip()
        telefono = self.view.usuario_telefono.get().strip()

        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        if not email:
            messagebox.showerror("Error", "El email es obligatorio")
            return
        if not Validaciones.validar_email(email):
            messagebox.showerror("Error", "Formato de email inválido")
            return
        if telefono and not telefono.isdigit():
            messagebox.showerror("Error", "El teléfono debe contener solo números")
            return

        params = (nombre, email, telefono or None)
        mensaje = UsuarioModel.insertar(params)
        messagebox.showinfo("Resultado", mensaje)
        self.view.limpiar_campos_usuario()
        self.view.actualizar_lista_usuarios()