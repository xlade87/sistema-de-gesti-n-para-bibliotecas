from config.database import db

class LibroModel:
    @staticmethod
    def obtener_todos():
        query = "SELECT id, titulo, autor, genero, año_publicacion FROM libros ORDER BY titulo"
        success, result = db.execute_query(query)
        if success:
            return result
        else:
            print(f"Error obteniendo libros: {result}")
            return []

    @staticmethod
    def insertar(datos):
        query = "CALL sp_InsertarLibro(%s, %s, %s, %s, %s)"
        success, result = db.execute_query(query, datos)
        if success:
            return result[0][0] if result else "Libro insertado (mensaje no devuelto por SP)"
        else:
            return f"Error al insertar: {result}"

    @staticmethod
    def eliminar(id_libro):
        query = "CALL sp_EliminarLibro(%s)"
        success, result = db.execute_query(query, (id_libro,))
        if success:
            return result[0][0] if result else "Libro eliminado (mensaje no devuelto por SP)"
        else:
            return f"Error al eliminar: {result}"

    @staticmethod
    def buscar_por_id(id_libro):
        query = "SELECT * FROM libros WHERE id = %s"
        success, result = db.execute_query(query, (id_libro,))
        if success and result:
            return result[0]
        return None