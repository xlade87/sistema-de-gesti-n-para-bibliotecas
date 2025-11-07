from config.database import db

class UsuarioModel:
    @staticmethod
    def obtener_todos():
        query = "SELECT id, nombre, email, telefono FROM usuarios ORDER BY nombre"
        success, result = db.execute_query(query)
        if success:
            return result
        else:
            print(f"Error obteniendo usuarios: {result}")
            return []

    @staticmethod
    def insertar(datos):
        query = "CALL sp_InsertarUsuario(%s, %s, %s)"
        success, result = db.execute_query(query, datos)
        if success:
            return result[0][0] if result else "Usuario insertado (mensaje no devuelto por SP)"
        else:
            return f"Error al insertar: {result}"
