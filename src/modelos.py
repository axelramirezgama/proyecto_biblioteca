# ==========================================
# Módulo: modelos.py
# Propósito: Definición de clases principales del sistema
# ==========================================

class Libro:
    """Clase que representa un libro dentro del inventario de la biblioteca."""
    
    def __init__(self, id_libro: int, titulo: str, autor: str, categoria: str, disponible: bool = True):
        # Asignación de identificador único del libro
        self.id_libro = id_libro
        # Asignación del título principal del libro
        self.titulo = titulo
        # Asignación del autor de la obra
        self.autor = autor
        # Asignación de la categoría o género literario
        self.categoria = categoria
        # Estado de disponibilidad (True si está disponible, False si está prestado)
        self.disponible = disponible

    def a_diccionario(self) -> dict:
        """Convierte la instancia del libro a un diccionario para guardarlo en JSON."""
        # Retorna representación en diccionario estructurado
        return {
            "id": self.id_libro,
            "titulo": self.titulo,
            "autor": self.autor,
            "categoria": self.categoria,
            "disponible": self.disponible
        }


class Usuario:
    """Clase que representa al bibliotecario o usuario en sesión."""
    
    def __init__(self, nickname: str):
        # Almacena el apodo o nombre ingresado por el usuario
        self.nickname = nickname.strip()
    
    def obtener_mensaje_bienvenida(self) -> str:
        """Genera el mensaje de bienvenida usando operadores de string (Criterio 1)."""
        # Formateo del nombre en mayúsculas
        nombre_formateado = self.nickname.upper()
        # Concatenación directa usando operadores de string (+)
        mensaje = "=== BIENVENIDO/A AL SISTEMA DE BIBLIOTECA, " + nombre_formateado + " ==="
        # Retorno del mensaje concatenado
        return mensaje