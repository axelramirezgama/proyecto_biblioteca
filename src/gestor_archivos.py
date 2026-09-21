# ==========================================
# Módulo: gestor_archivos.py
# Propósito: Lógica de lectura, escritura, creación de archivos y manejo de excepciones
# ==========================================

import json
from pathlib import Path
from typing import Dict, List
from utilidades import tupla_a_texto_archivos


# Definición de rutas principales
DIR_DATA = Path("data")
DIR_ENTREGABLES = Path("entregables")


def cargar_inventario_json() -> List[dict]:
    """Carga la lista de libros desde el archivo JSON de la base de datos local."""
    # Define la ruta al archivo json de inventario
    ruta_json = DIR_DATA / "inventario.json"
    
    try:
        # Abre el archivo en modo lectura con codificación UTF-8
        with open(ruta_json, "r", encoding="utf-8") as archivo:
            # Lee y convierte el contenido JSON a una lista de diccionarios
            datos = json.load(archivo)
            # Retorna la lista con la información de los libros
            return datos
            
    except FileNotFoundError:
        # Captura error si el archivo json no existe aún
        print("[!] Advertencia: No se encontró inventario.json. Se iniciará vacío.")
        # Retorna lista vacía como respaldo de seguridad
        return []
        
    except json.JSONDecodeError:
        # Captura error si el archivo JSON tiene formato inválido
        print("[!] Error: El archivo inventario.json está corrupto.")
        # Retorna lista vacía para evitar caídas del sistema
        return []


def guardar_inventario_json(libros_dict: List[dict]) -> None:
    """Guarda la lista actualizada de libros en el archivo JSON."""
    # Define la ruta del archivo de inventario
    ruta_json = DIR_DATA / "inventario.json"
    
    try:
        # Abre el archivo en modo escritura
        with open(ruta_json, "w", encoding="utf-8") as archivo:
            # Convierte la estructura de datos a JSON formateado con sangría
            json.dump(libros_dict, archivo, indent=2, ensure_ascii=False)
            
    except PermissionError:
        # Lanza excepción si el sistema operativo no otorga permisos de escritura
        raise PermissionError("No tienes permisos suficientes para escribir en la carpeta 'data/'.")


def obtener_archivos_preexistentes() -> Dict[int, Path]:
    """
    Retorna un diccionario con los archivos preexistentes disponibles para lectura.
    Cumple con el Criterio 4: Lista o diccionario de archivos preexistentes.
    """
    # Mapeo de opciones numeradas a rutas de archivos en la carpeta /data
    archivos = {
        1: DIR_DATA / "proveedor_a.txt",
        2: DIR_DATA / "proveedor_b.txt",
        3: DIR_DATA / "politicas_prestamo.txt",
        4: DIR_DATA / "lista_categorias.txt"
    }
    # Retorna el diccionario con la lista de opciones
    return archivos


def leer_archivo_texto(ruta_archivo: Path) -> str:
    """
    Lee y retorna el contenido de un archivo de texto.
    Cumple con el Criterio 4 (Lectura) y Criterio 5 (Excepciones).
    """
    try:
        # Abre y lee el archivo de texto especificado
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            # Lee todo el texto y lo almacena en una variable
            contenido = archivo.read()
            # Retorna la cadena leída
            return contenido
            
    except FileNotFoundError:
        # Captura explícita de error cuando el archivo especificado no existe
        raise FileNotFoundError(f"El archivo '{ruta_archivo.name}' no existe en la carpeta especificada.")
        
    except UnicodeDecodeError:
        # Captura error si el archivo tiene una codificación incompatible
        raise ValueError(f"No se pudo leer el archivo '{ruta_archivo.name}' debido a un error de codificación.")


def escribir_bitacora(fecha_tupla: tuple, registro: str) -> Path:
    """
    Escribe un evento en la bitácora diaria (.txt).
    Cumple con el Criterio 4 (Escribir) y usa la tupla de fecha (Criterio 3).
    """
    # Convierte la tupla (día, mes, año) a texto con formato dd_mm_aaaa
    fecha_str = tupla_a_texto_archivos(fecha_tupla)
    # Define la ruta del archivo de bitácora diaria dentro de /entregables
    ruta_bitacora = DIR_ENTREGABLES / f"bitacora_{fecha_str}.txt"
    
    try:
        # Abre el archivo en modo 'a' (append) para añadir líneas sin borrar lo anterior
        with open(ruta_bitacora, "a", encoding="utf-8") as archivo:
            # Escribe la entrada del registro con un salto de línea
            archivo.write(f"[{fecha_str}] - {registro}\n")
            
        # Retorna la ruta del archivo de bitácora modificado
        return ruta_bitacora
        
    except Exception as e:
        # Captura general de errores al intentar escribir el archivo
        raise IOError(f"No se pudo actualizar la bitácora diaria: {str(e)}")


def crear_ticket_prestamo(fecha_tupla: tuple, nickname: str, titulo_libro: str) -> Path:
    """
    Crea un nuevo archivo .txt con el comprobante/ticket de préstamo.
    Cumple con el Criterio 4 (Crear archivo) y usa la tupla de fecha (Criterio 3).
    """
    # Formatea la tupla de fecha a cadena de texto
    fecha_str = tupla_a_texto_archivos(fecha_tupla)
    # Limpia el nombre de usuario para evitar caracteres inválidos en rutas
    nick_limpio = nickname.replace(" ", "_").lower()
    # Define la ruta única del ticket generado dentro de /entregables
    ruta_ticket = DIR_ENTREGABLES / f"ticket_{nick_limpio}_{fecha_str}.txt"
    
    # Construcción del texto estilizado para el ticket de préstamo
    contenido_ticket = (
        "=========================================\n"
        "       BIBLIOTECA CENTRAL ATENEO         \n"
        "       COMPROBANTE DE PRÉSTAMO           \n"
        "=========================================\n"
        f"Fecha del Préstamo: {fecha_str}\n"
        f"Usuario Responsable: {nickname}\n"
        f"Libro Prestado:      {titulo_libro}\n"
        "-----------------------------------------\n"
        "Nota: Favor de devolver en un plazo máximo\n"
        "de 7 días hábiles.\n"
        "=========================================\n"
    )
    
    try:
        # Abre el archivo en modo escritura ('w') creando un archivo totalmente nuevo
        with open(ruta_ticket, "w", encoding="utf-8") as archivo:
            # Escribe el bloque de texto en el archivo recién creado
            archivo.write(contenido_ticket)
            
        # Retorna la ruta del ticket generado
        return ruta_ticket
        
    except PermissionError:
        # Captura error de permisos al intentar crear el archivo
        raise PermissionError("No hay permisos suficientes para crear tickets en 'entregables/'.")