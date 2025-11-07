from PIL import Image, ImageTk

class ImagenManager:
    def __init__(self):
        self.ruta_actual = None
        self.ruta_usuario = None

    def cargar_imagen_para_mostrar(self, ruta, tamaño=(150, 150)):
        """Carga imagen solo para mostrar en pantalla"""
        try:
            imagen = Image.open(ruta)
            imagen = imagen.resize(tamaño, Image.LANCZOS)
            return ImageTk.PhotoImage(imagen)
        except Exception as e:
            print(f"Error al cargar imagen: {e}")
            return None

    def procesar_imagen_para_guardar(self, ruta, tamaño=(400, 600)):
        """Procesa imagen para guardar (redimensionar, convertir, aplicar filtros)"""
        try:
            imagen = Image.open(ruta)
            imagen = imagen.resize(tamaño, Image.LANCZOS)
            # Aquí puedes aplicar más filtros si quieres
            # imagen = imagen.filter(ImageFilter.BLUR)
            return imagen
        except Exception as e:
            print(f"Error al procesar imagen para guardar: {e}")
            return None