from config.database import db

class PrestamoModel:
    @staticmethod
    def obtener_todos():
        query = """SELECT p.id, l.titulo, u.nombre, p.fecha_prestamo, 
                   CASE WHEN p.devuelto THEN 'Sí' ELSE 'No' END
                   FROM prestamos p
                   JOIN libros l ON p.libro_id = l.id
                   JOIN usuarios u ON p.usuario_id = u.id
                   ORDER BY p.fecha_prestamo DESC"""
        success, result = db.execute_query(query)
        if success:
            return result
        else:
            print(f"Error obteniendo préstamos: {result}")
            return []

    @staticmethod
    def realizar(datos):
        query = "CALL sp_RealizarPrestamo(%s, %s)"
        success, result = db.execute_query(query, datos)
        if success:
            return result[0][0] if result else "Préstamo realizado (mensaje no devuelto por SP)"
        else:
            return f"Error al realizar préstamo: {result}"

    @staticmethod
    def devolver(id_prestamo):
        query = "CALL sp_DevolverLibro(%s)"
        success, result = db.execute_query(query, (id_prestamo,))
        if success:
            return result[0][0] if result else "Libro devuelto (mensaje no devuelto por SP)"
        else:
            return f"Error al devolver libro: {result}"