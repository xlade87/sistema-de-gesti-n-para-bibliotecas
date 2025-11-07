from config.database import db

class AutorModel:
    @staticmethod
    def obtener_todos():
        query = "SELECT id, nombre, nacionalidad, fecha_nacimiento FROM autores ORDER BY nombre"
        success, result = db.execute_query(query)
        if success:
            return result
        else:
            print(f"Error obteniendo autores: {result}")
            return []

    @staticmethod
    def insertar(datos):
        query = "CALL sp_InsertarAutor(%s, %s, %s)"
        success, result = db.execute_query(query, datos)
        if success:
            return result[0][0] if result else "Autor insertado (mensaje no devuelto por SP)"
        else:
            return f"Error al insertar: {result}"

    @staticmethod
    def eliminar(id_autor):
        # Asegúrate de que 'sp_EliminarAutor' exista en tu archivo stored_procedures.sql
        query = "CALL sp_EliminarAutor(%s)"
        success, result = db.execute_query(query, (id_autor,))
        if success:
            return result[0][0] if result else "Autor eliminado (mensaje no devuelto por SP)"
        else:
            return f"Error al eliminar: {result}"