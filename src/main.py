# ==========================================
# Módulo: main.py
# Propósito: Punto de entrada principal y orquestador del flujo del sistema
# ==========================================

import time
import sys
from pathlib import Path

# Importación de los módulos locales del proyecto necesarios para funcionar
from modelos import Usuario, Libro
from utilidades import capturar_fecha_tupla, TIEMPO_LIMITE_INACTIVIDAD
import gestor_archivos as gestor
import ui


def solicitar_nickname() -> Usuario:
    """Solicita el nombre al usuario y genera la instancia de Usuario (Criterio 1)."""
    while True:
        # Pide el nombre de usuario mediante la consola de Rich para darle color
        nick = ui.console.input("[bold cyan]Ingresa tu nombre o nickname: [/bold cyan]")
        # Valida que el nombre introducido no esté vacío quitando espacios extra
        if nick.strip():
            # Retorna una nueva instancia de la clase Usuario si el texto es válido
            return Usuario(nick)
        
        # Muestra mensaje de error en rojo si el campo se dejó en blanco
        ui.mostrar_mensaje_error("El nombre no puede estar vacío. Intenta de nuevo.")


def solicitar_fecha_sistema() -> tuple:
    """Solicita la fecha al usuario y la guarda en una tupla (Criterio 3)."""
    while True:
        try:
            # Solicita la fecha en formato numérico dd/mm/aaaa al inicio de la sesión
            entrada_fecha = ui.console.input("[bold yellow]Ingresa la fecha de hoy (dd/mm/aaaa): [/bold yellow]")
            
            # Procesa la cadena ingresada y valida la fecha retornando la tupla (día, mes, año)
            fecha_tupla = capturar_fecha_tupla(entrada_fecha)
            
            # Muestra confirmación en color verde de la tupla capturada exitosamente
            ui.mostrar_mensaje_exito(f"Fecha registrada en tupla correctamente: {fecha_tupla}")
            
            # Retorna la tupla guardada para usarla en bitácoras y tickets
            return fecha_tupla
            
        except ValueError as e:
            # Captura errores de formato o fechas inválidas sin cerrar el programa (Criterio 5)
            ui.mostrar_mensaje_error(str(e))


def main():
    """Función principal que controla el bucle de ejecución de la aplicación."""
    
    # Muestra la animación de pantalla de carga inicial <= 5 segundos (Criterio 1)
    ui.mostrar_pantalla_carga()
    
    # 1. Captura de usuario e interacción inicial para arrancar el sistema
    usuario_actual = solicitar_nickname()
    
    # Obtiene el mensaje formateado con operadores de string (+) desde el modelo
    mensaje_bienvenida = usuario_actual.obtener_mensaje_bienvenida()
    
    # Despliega el banner estilizado de bienvenida utilizando Rich
    ui.mostrar_banner_bienvenida(mensaje_bienvenida)
    
    # 2. Captura de la tupla de fecha para el registro de los movimientos
    fecha_actual_tupla = solicitar_fecha_sistema()
    
    # 3. Ciclo Principal del Menú (Criterio 2)
    mantenimiento_activo = True
    
    while mantenimiento_activo:
        # Verifica si el usuario actual es administrador verificando su nombre
        es_admin = usuario_actual.nickname.strip().lower() == "admin"
        
        # Dependiendo del tipo de usuario, despliega el menú correspondiente
        if es_admin:
            # Despliega el menú exclusivo de administrador
            ui.mostrar_menu_admin()
        else:
            # Despliega el menú estándar en formato de tabla de 2 columnas
            ui.mostrar_menu_principal()
        
        # Registra la estampa de tiempo justo antes de pedir la entrada del usuario
        tiempo_inicio = time.time()
        
        # Solicita la opción seleccionada por el usuario (admin o normal)
        opcion = ui.console.input("\n[bold yellow]Selecciona una opción: [/bold yellow]").strip()
        
        # Registra la estampa de tiempo inmediatamente después de recibir la entrada
        tiempo_fin = time.time()
        
        # Calcula la diferencia de segundos transcurridos durante la selección en el menú
        segundos_transcurridos = int(tiempo_fin - tiempo_inicio)
        
        # Variable bandera para detectar inactividad prolongada del usuario
        inactividad_detectada = False
        
        # Ciclo FOR obligatorio para evaluar si se superó el tiempo límite (Criterio 2)
        for segundo in range(segundos_transcurridos):
            # Compara si los segundos transcurridos exceden el tiempo máximo configurado
            if segundo >= TIEMPO_LIMITE_INACTIVIDAD:
                # Cambia el estado de la bandera si se sobrepasa el límite
                inactividad_detectada = True
                # Rompe el ciclo for al confirmar la inactividad para ahorrar recursos
                break 
        
        # Si se detecta inactividad (ej. 10 minutos o tiempo de prueba), pregunta si desea continuar
        if inactividad_detectada:
            # Avisa al usuario del tiempo que se ausentó de la pantalla
            ui.mostrar_mensaje_error(f"¡Atención! Tardaste {segundos_transcurridos} segundos en responder.")
            # Pregunta explícitamente si requiere seguir usando el sistema
            respuesta = ui.console.input("[bold magenta]¿Deseas continuar en el menú? (si/no): [/bold magenta]").strip().lower()
            
            # Si el usuario responde distinto de 'si', el sistema vuelve a la pantalla inicial de login
            if respuesta != "si":
                ui.mostrar_mensaje_exito("Reiniciando sesión por inactividad...")
                # Pide de nuevo los datos de ingreso
                usuario_actual = solicitar_nickname()
                mensaje_bienvenida = usuario_actual.obtener_mensaje_bienvenida()
                ui.mostrar_banner_bienvenida(mensaje_bienvenida)
                # Regresa al inicio del ciclo while ignorando la opción ingresada
                continue 
        
        # Manejo de excepciones global para proteger la navegación de la opción elegida
        try:
            # ==========================================
            # LÓGICA DEL MENÚ DE ADMINISTRADOR
            # ==========================================
            if es_admin:
                # ADMIN OPCIÓN 1: Ver todo el inventario de libros
                if opcion == "1":
                    # Carga el inventario directo del archivo JSON
                    libros = gestor.cargar_inventario_json()
                    # Muestra los datos tabulados en la consola
                    ui.mostrar_tabla_libros(libros)
                
                # ADMIN OPCIÓN 2: Agregar un libro nuevo al catálogo
                elif opcion == "2":
                    # Pide los datos necesarios para registrar el nuevo título
                    titulo = ui.console.input("[bold cyan]Ingresa el título del nuevo libro: [/bold cyan]")
                    autor = ui.console.input("[bold cyan]Ingresa el autor del libro: [/bold cyan]")
                    # Envía los datos al gestor para agregarlos al archivo json
                    gestor.agregar_libro(titulo, autor)
                    ui.mostrar_mensaje_exito("Libro agregado al catálogo exitosamente.")
                
                # ADMIN OPCIÓN 3: Cambiar estado de un libro (Disponible/Prestado)
                elif opcion == "3":
                    # Pide el ID del libro que se va a modificar
                    id_sel = ui.console.input("[bold cyan]Ingresa el ID del libro a modificar: [/bold cyan]")
                    # Intenta cambiar el estado enviando el ID casteado a entero
                    if gestor.cambiar_estado_libro(int(id_sel)):
                        ui.mostrar_mensaje_exito("Estado del libro actualizado correctamente.")
                    else:
                        ui.mostrar_mensaje_error("No se encontró ningún libro con ese ID.")
                
                # ADMIN OPCIÓN 4: Cerrar sesión (Cambiar de usuario)
                elif opcion == "4":
                    ui.mostrar_mensaje_exito("Cerrando sesión de administrador...")
                    # Solicita nuevo nickname y actualiza la sesión actual
                    usuario_actual = solicitar_nickname()
                    mensaje_bienvenida = usuario_actual.obtener_mensaje_bienvenida()
                    ui.mostrar_banner_bienvenida(mensaje_bienvenida)
                
                # ADMIN OPCIÓN 0: Salir del sistema
                elif opcion == "0":
                    ui.mostrar_mensaje_exito("Cerrando sistema de administración. ¡Hasta luego!")
                    # Rompe el bucle while para terminar la ejecución de la app
                    mantenimiento_activo = False
                    
                else:
                    # Opción no contemplada en el menú del administrador
                    ui.mostrar_mensaje_error("Opción no válida. Ingresa un número del 0 al 4.")

            # ==========================================
            # LÓGICA DEL MENÚ DE USUARIO NORMAL
            # ==========================================
            else:
                # OPCIÓN 1: Leer archivo preexistente (Criterio 4)
                if opcion == "1":
                    # Obtiene el diccionario con los 4 archivos preexistentes en la carpeta /data
                    archivos = gestor.obtener_archivos_preexistentes()
                    # Muestra los archivos disponibles en una tabla bonita
                    ui.mostrar_tabla_archivos(archivos)
                    
                    # Solicita al usuario el ID numérico del archivo a leer
                    seleccion = ui.console.input("[bold cyan]Ingresa el número del archivo que deseas abrir: [/bold cyan]")
                    
                    # Valida que la selección sea un entero y se encuentre en las claves del diccionario
                    idx = int(seleccion)
                    if idx in archivos:
                        # Lee el texto plano del archivo elegido
                        contenido = gestor.leer_archivo_texto(archivos[idx])
                        # Imprime el contenido en la consola con un encabezado
                        ui.console.print(f"\n[bold green]--- CONTENIDO DE {archivos[idx].name} ---[/bold green]")
                        ui.console.print(contenido)
                        ui.console.print("[bold green]------------------------------------------[/bold green]\n")
                    else:
                        # Levanta un aviso si selecciona un número fuera de rango
                        ui.mostrar_mensaje_error("El número seleccionado no existe en la lista de archivos.")

                # OPCIÓN 2: Escribir en la bitácora diaria (Criterio 4)
                elif opcion == "2":
                    # Solicita al usuario la nota, recordatorio o evento a registrar
                    registro = ui.console.input("[bold cyan]Ingresa la nota/evento para la bitácora de hoy: [/bold cyan]")
                    
                    # Guarda el registro textual en el archivo de bitácora usando la tupla de fecha
                    ruta = gestor.escribir_bitacora(fecha_actual_tupla, registro)
                    # Notifica al usuario la ruta exacta donde quedó el archivo
                    ui.mostrar_mensaje_exito(f"Evento registrado correctamente en: {ruta}")

                # OPCIÓN 3: Crear ticket / comprobante de préstamo (Criterio 4)
                elif opcion == "3":
                    # Carga el inventario actual de libros para mostrárselo al usuario
                    libros = gestor.cargar_inventario_json()
                    # Muestra la tabla visual de libros y sus estatus
                    ui.mostrar_tabla_libros(libros)
                    
                    # Solicita el identificador del libro que se va a prestar
                    id_sel = ui.console.input("[bold cyan]Ingresa el ID del libro a prestar: [/bold cyan]")
                    id_libro = int(id_sel)
                    
                    # Variable auxiliar para guardar el libro si lo encontramos
                    libro_encontrado = None
                    # Itera sobre el inventario buscando coincidencia con el ID
                    for l in libros:
                        if l["id"] == id_libro:
                            libro_encontrado = l
                            break # Termina la búsqueda al hallar coincidencia
                    
                    # Revisa si encontró el libro y además verifica su disponibilidad booleana
                    if libro_encontrado and libro_encontrado["disponible"]:
                        # Modifica la bandera de disponibilidad en memoria (False = no disponible)
                        libro_encontrado["disponible"] = False
                        # Guarda los cambios de forma persistente en el JSON
                        gestor.guardar_inventario_json(libros)
                        
                        # Genera el archivo físico del ticket usando fecha y nombre de usuario
                        ruta_ticket = gestor.crear_ticket_prestamo(
                            fecha_actual_tupla, 
                            usuario_actual.nickname, 
                            libro_encontrado["titulo"]
                        )
                        # Notifica éxito con la ruta del entregable creado
                        ui.mostrar_mensaje_exito(f"¡Ticket generado exitosamente en: {ruta_ticket}!")
                        
                    # Si el libro existe pero está marcado como falso (ya prestado)
                    elif libro_encontrado and not libro_encontrado["disponible"]:
                        ui.mostrar_mensaje_error("El libro seleccionado ya se encuentra prestado.")
                    else:
                        # Si iteró todo el JSON y el ID no coincidió con ninguno
                        ui.mostrar_mensaje_error("No se encontró ningún libro con ese ID.")

                # OPCIÓN 4: Consultar catálogo de libros
                elif opcion == "4":
                    # Carga en memoria los libros desde la ruta del JSON
                    libros = gestor.cargar_inventario_json()
                    # Manda la lista a la interfaz gráfica para su visualización
                    ui.mostrar_tabla_libros(libros)

                # OPCIÓN 5: Cambiar de usuario
                elif opcion == "5":
                    # Brinda retroalimentación visual del proceso
                    ui.mostrar_mensaje_exito("Cambiando de sesión...")
                    # Interrumpe la sesión actual y solicita credenciales de nuevo
                    usuario_actual = solicitar_nickname()
                    mensaje_bienvenida = usuario_actual.obtener_mensaje_bienvenida()
                    # Vuelve a pintar el panel de bienvenida
                    ui.mostrar_banner_bienvenida(mensaje_bienvenida)

                # OPCIÓN 0: Salir del programa
                elif opcion == "0":
                    # Despedida amigable para el usuario normal
                    ui.mostrar_mensaje_exito("Gracias por utilizar el Sistema de Biblioteca Central Ateneo. ¡Hasta luego!")
                    # Cambia la variable de control a Falso para apagar el programa
                    mantenimiento_activo = False

                else:
                    # Filtro de seguridad por si escriben cualquier otra cosa en el menú normal
                    ui.mostrar_mensaje_error("Opción no válida. Ingresa un número del 0 al 5.")

        except ValueError as ve:
            # Captura errores de conversión numérica (ej. ingresar letras al pedir el ID de libro)
            ui.mostrar_mensaje_error(f"Entrada de datos inválida: {str(ve)}")
            
        except FileNotFoundError as fnfe:
            # Evita que un archivo faltante crashee la aplicación (Criterio 5)
            ui.mostrar_mensaje_error(str(fnfe))
            
        except Exception as ex:
            # Captura comodín para cualquier otra excepción imprevista manteniendo el ciclo activo
            ui.mostrar_mensaje_error(f"Ocurrió un error inesperado: {str(ex)}")


# Condición estándar para asegurar que este script sea el punto de ejecución inicial
if __name__ == "__main__":
    main()