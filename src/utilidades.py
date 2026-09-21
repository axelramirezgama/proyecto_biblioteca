# ==========================================
# Módulo: utilidades.py
# Propósito: Funciones de soporte para fechas, validaciones y tiempos
# ==========================================

from typing import Tuple
from datetime import datetime

# Tiempo límite de inactividad para pruebas (en segundos)
# NOTA: Ajustar a 600 segundos (10 minutos) para la entrega final del proyecto
TIEMPO_LIMITE_INACTIVIDAD = 10 


def capturar_fecha_tupla(cadena_fecha: str) -> Tuple[int, int, int]:
    """
    Recibe una fecha en formato dd/mm/aaaa, la valida y la almacena en una tupla.
    Cumple con el Criterio 3: Fecha = día, mes, año
    """
    # Intenta dividir la cadena ingresada usando la barra diagonal como separador
    partes = cadena_fecha.strip().split('/')
    
    # Valida que la fecha contenga exactamente 3 partes (día, mes, año)
    if len(partes) != 3:
        # Lanza excepción de valor si la estructura no es dd/mm/aaaa
        raise ValueError("El formato debe ser dd/mm/aaaa (ejemplo: 12/06/2023)")
    
    try:
        # Convierte el primer elemento a número entero para el día
        dia = int(partes[0])
        # Convierte el segundo elemento a número entero para el mes
        mes = int(partes[1])
        # Convierte el tercer elemento a número entero para el año
        anio = int(partes[2])
        
        # Válida que la fecha sea una fecha real usando la librería datetime
        datetime(year=anio, month=mes, day=dia)
        
        # Crea la tupla requerida por la rúbrica: Fecha = día, mes, año
        fecha_tupla = (dia, mes, anio)
        # Retorna la tupla de fecha procesada
        return fecha_tupla

    except ValueError:
        # Excepción en caso de números fuera de rango (ej. mes 13 o día 32)
        raise ValueError("La fecha ingresada no corresponde a un día o mes válido.")


def tupla_a_texto_archivos(fecha_tupla: Tuple[int, int, int]) -> str:
    """
    Convierte la tupla (día, mes, año) en formato de texto con guiones 
    para nombrar o estampar archivos (ej: '12_06_2023').
    """
    # Desempaqueta la tupla de fecha en variables individuales
    dia, mes, anio = fecha_tupla
    # Retorna la cadena formateada con ceros a la izquierda para días y meses de un dígito
    return f"{dia:02d}_{mes:02d}_{anio}"