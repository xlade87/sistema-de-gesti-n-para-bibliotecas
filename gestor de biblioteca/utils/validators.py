import re
import os

class Validaciones:
    @staticmethod
    def solo_numeros(texto):
        """Solo permite números"""
        return texto.isdigit() or texto == ""

    @staticmethod
    def validar_email(email):
        """Valida formato de email"""
        return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

    @staticmethod
    def validar_imagen(ruta):
        """Valida imagen"""
        if not ruta:
            return False, "No hay imagen"
        extensiones = ['.jpg', '.jpeg', '.png', '.gif']
        ext = os.path.splitext(ruta)[1].lower()
        if ext not in extensiones:
            return False, f"Solo: {', '.join(extensiones)}"
        tamano = os.path.getsize(ruta) / (1024 * 1024)
        if tamano > 2:
            return False, "Máximo 2MB"
        return True, "OK"

    @staticmethod
    def validar_longitud_texto(texto, minimo=0, maximo=100):
        """Valida longitud de texto"""
        longitud = len(texto)
        if longitud < minimo:
            return False, f"Longitud mínima: {minimo} caracteres"
        if longitud > maximo:
            return False, f"Longitud máxima: {maximo} caracteres"
        return True, "OK"