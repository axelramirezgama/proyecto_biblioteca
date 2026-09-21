# ==========================================
# Módulo: main.py
# Propósito: Punto de entrada principal y orquestador del flujo del sistema
# ==========================================

import time
import sys
from pathlib import Path

# Importación de los módulos locales del proyecto
from modelos import Usuario, Libro
from utilidades import capturar_fecha_tupla, TIEMPO_LIMITE_INACTIVIDAD
import gestor_archivos as gestor
import ui


def solicitar_nickname() -> Usuario:
    """Solicita el nombre al usuario y genera la instancia de Usuario (Criterio 1)."""
    while True:
        # Pide el nombre de usuario mediante la consola de Rich
        nick = ui.console.input("[bold cyan]Ingresa tu nombre o nickname: [/bold cyan]")
        
        # Valida que el nombre introducido no esté vacío
        if nick.strip():
            # Retorna una nueva instancia de la clase Usuario
            return Usuario(nick)
        
        # Muestra mensaje de error si el campo se dejó en blanco
        ui.mostrar_mensaje_error("El nombre no puede estar vacío. Intenta de nuevo.")


def solicitar_fecha_sistema() -> tuple:
    """Solicita la fecha al usuario y la guarda en una tupla (Criterio 3)."""
    while True:
        try:
            # Solicita la fecha en formato numérico dd/mm/aaaa
            entrada_fecha = ui.console.input("[bold yellow]Ingresa la fecha de hoy (dd/mm/aaaa): [/bold yellow]")
            
            # Procesa y valida la fecha retornando la tupla (día, mes, año)
            fecha_tupla = capturar_fecha_tupla(entrada_fecha)
            
            # Muestra confirmación de la tupla capturada
            ui.mostrar_mensaje_exito(f"Fecha registrada en tupla correctamente: {fecha_tupla}")
            
            # Retorna la tupla guardada
            return fecha_tupla
            
        except ValueError as e:
            # Captura errores de formato o fechas inválidas sin cerrar el programa (Criterio 5)
            ui.mostrar_mensaje_error(str(e))


def main():
    """Función principal que controla el bucle de ejecución de la aplicación."""
    
    # Muestra la animación de pantalla de carga inicial <= 5 segundos (Criterio 1)
    ui.mostrar_pantalla_carga()
    
    # 1. Captura de usuario e interacción inicial
    usuario_actual = solicitar_nickname()
    
    # Obtiene el mensaje formateado con operadores de string (+)
    mensaje_bienvenida = usuario_actual.obtener_mensaje_bienvenida()
    
    # Despliega el banner estilizado de bienvenida
    ui.mostrar_banner_bienvenida(mensaje_bienvenida)
    
    # 2. Captura de la tupla de fecha
    fecha_actual_tupla = solicitar_fecha_sistema()
    
    # 3. Ciclo Principal del Menú (Criterio 2)
    mantenimiento_activo = True
    
    while mantenimiento_activo:
        # Despliega el menú en formato de tabla de 2 columnas
        ui.mostrar_menu_principal()
        
        # Registra la estampa de tiempo justo antes de pedir la entrada
        tiempo_inicio = time.time()
        
        # Solicita la opción seleccionada por el usuario
        opcion = ui.console.input("\n[bold yellow]Selecciona una opción (0-5): [/bold yellow]").strip()
        
        # Registra la estampa de tiempo inmediatamente después de recibir la entrada
        tiempo_fin = time.time()
        
        # Calcula la diferencia de segundos transcurridos durante la selección
        segundos_transcurridos = int(tiempo_fin - tiempo_inicio)
        
        # Variable bandera para detectar inactividad
        inactividad_detectada = False
        
        # Ciclo FOR obligatorio para evaluar si se superó el tiempo límite (Criterio 2)
        for segundo in range(segundos_transcurridos):
            # Compara si los segundos transcurridos exceden el tiempo máximo configurado
            if segundo >= TIEMPO_LIMITE_INACTIVIDAD:
                inactividad_detectada = True
                break # Rompe el ciclo for al confirmar la inactividad
        
        # Si se detecta inactividad de 10 minutos (o del tiempo de prueba), pregunta si desea continuar
        if inactividad_detectada:
            ui.mostrar_mensaje_error(f"¡Atención! Tardaste {segundos_transcurridos} segundos en responder.")
            respuesta = ui.console.input("[bold magenta]¿Deseas continuar en el menú? (si/no): [/bold magenta]").strip().lower()
            
            # Si el usuario responde 'no', el sistema vuelve a la pantalla inicial de login
            if respuesta != "si":
                ui.mostrar_mensaje_exito("Reiniciando sesión por inactividad...")
                usuario_actual = solicitar_nickname()
                mensaje_bienvenida = usuario_actual.obtener_mensaje_bienvenida()
                ui.mostrar_banner_bienvenida(mensaje_bienvenida)
                continue # Regresa al inicio del ciclo while
        
        # Manejo de excepciones global para proteger la navegación de la opción elegida
        try:
            # OPCIÓN 1: Leer archivo preexistente (Criterio 4)
            if opcion == "1":
                # Obtiene el diccionario con los 4 archivos preexistentes
                archivos = gestor.obtener_archivos_preexistentes()
                # Muestra los archivos disponibles en una tabla
                ui.mostrar_tabla_archivos(archivos)
                
                # Solicita al usuario el ID del archivo a leer
                seleccion = ui.console.input("[bold cyan]Ingresa el número del archivo que deseas abrir: [/bold cyan]")
                
                # Valida que la selección sea un entero válido dentro de las claves
                idx = int(seleccion)
                if idx in archivos:
                    # Lee el contenido del archivo elegido
                    contenido = gestor.leer_archivo_texto(archivos[idx])
                    # Muestra el contenido del archivo en la consola
                    ui.console.print(f"\n[bold green]--- CONTENIDO DE {archivos[idx].name} ---[/bold green]")
                    ui.console.print(contenido)
                    ui.console.print("[bold green]------------------------------------------[/bold green]\n")
                else:
                    # Excepción si selecciona un número fuera de rango
                    ui.mostrar_mensaje_error("El número seleccionado no existe en la lista de archivos.")

            # OPCIÓN 2: Escribir en la bitácora diaria (Criterio 4)
            elif opcion == "2":
                # Solicita la nota o evento a registrar
                registro = ui.console.input("[bold cyan]Ingresa la nota/evento para la bitácora de hoy: [/bold cyan]")
                
                # Guarda el registro en el archivo de bitácora usando la tupla de fecha
                ruta = gestor.escribir_bitacora(fecha_actual_tupla, registro)
                # Notifica el éxito y la ruta del archivo modificado
                ui.mostrar_mensaje_exito(f"Evento registrado correctamente en: {ruta}")

            # OPCIÓN 3: Crear ticket / comprobante de préstamo (Criterio 4)
            elif opcion == "3":
                # Carga la lista de libros del inventario JSON
                libros = gestor.cargar_inventario_json()
                # Muestra la tabla de libros disponibles
                ui.mostrar_tabla_libros(libros)
                
                # Solicita el ID del libro a prestar
                id_sel = ui.console.input("[bold cyan]Ingresa el ID del libro a prestar: [/bold cyan]")
                id_libro = int(id_sel)
                
                # Busca el libro en el catálogo
                libro_encontrado = None
                for l in libros:
                    if l["id"] == id_libro:
                        libro_encontrado = l
                        break
                
                # Evalúa si se encontró el libro y si está disponible
                if libro_encontrado and libro_encontrado["disponible"]:
                    # Cambia el estatus del libro a NO disponible
                    libro_encontrado["disponible"] = False
                    # Guarda el cambio en el archivo JSON
                    gestor.guardar_inventario_json(libros)
                    
                    # Crea el archivo de ticket .txt usando la tupla de fecha y el nickname
                    ruta_ticket = gestor.crear_ticket_prestamo(
                        fecha_actual_tupla, 
                        usuario_actual.nickname, 
                        libro_encontrado["titulo"]
                    )
                    ui.mostrar_mensaje_exito(f"¡Ticket generado exitosamente en: {ruta_ticket}!")
                    
                elif libro_encontrado and not libro_encontrado["disponible"]:
                    ui.mostrar_mensaje_error("El libro seleccionado ya se encuentra prestado.")
                else:
                    ui.mostrar_mensaje_error("No se encontró ningún libro con ese ID.")

            # OPCIÓN 4: Consultar catálogo de libros
            elif opcion == "4":
                # Carga los libros del archivo JSON
                libros = gestor.cargar_inventario_json()
                # Imprime la tabla con los libros registrados
                ui.mostrar_tabla_libros(libros)

            # OPCIÓN 5: Cambiar de usuario
            elif opcion == "5":
                ui.mostrar_mensaje_exito("Cambiando de sesión...")
                # Solicita nuevo nickname y actualiza la sesión
                usuario_actual = solicitar_nickname()
                mensaje_bienvenida = usuario_actual.obtener_mensaje_bienvenida()
                ui.mostrar_banner_bienvenida(mensaje_bienvenida)

            # OPCIÓN 0: Salir del programa
            elif opcion == "0":
                ui.mostrar_mensaje_exito("Gracias por utilizar el Sistema de Biblioteca Central Ateneo. ¡Hasta luego!")
                # Rompe el bucle while para terminar la ejecución
                mantenimiento_activo = False

            else:
                # Opción no contemplada en el menú
                ui.mostrar_mensaje_error("Opción no válida. Ingresa un número del 0 al 5.")

        except ValueError as ve:
            # Captura errores de conversión numérica (ej. ingresar letras cuando se espera un ID)
            ui.mostrar_mensaje_error(f"Entrada de datos inválida: {str(ve)}")
            
        except FileNotFoundError as fnfe:
            # Captura errores de archivos no encontrados
            ui.mostrar_mensaje_error(str(fnfe))
            
        except Exception as ex:
            # Captura cualquier otra excepción inesperada para garantizar la estabilidad
            ui.mostrar_mensaje_error(f"Ocurrió un error inesperado: {str(ex)}")


# Punto de entrada estándar de Python
if __name__ == "__main__":
    main()