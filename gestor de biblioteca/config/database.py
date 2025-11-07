import mysql.connector
from tkinter import messagebox

class DatabaseConnection:
    def __init__(self, host="localhost", database="biblioteca_personal", user="root", password=""):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                autocommit=True
            )
            self.cursor = self.connection.cursor(buffered=True)
            return True
        except mysql.connector.Error as error:
            messagebox.showerror("Error de Conexión", f"Error conectando a la base de datos: {error}")
            return False

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, parameters=None):
        try:
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)

            if query.strip().upper().startswith('SELECT'):
                return True, self.cursor.fetchall()
            else:
                self.connection.commit()
                # Capturar el mensaje de retorno del SP si es una llamada
                if query.strip().upper().startswith('CALL'):
                    result = self.cursor.fetchall()
                    self.cursor.nextset()
                    return True, result
                else:
                    return True, "Operación exitosa"
        except mysql.connector.Error as error:
            return False, str(error)

# Instancia global para usar en el proyecto
db = DatabaseConnection()