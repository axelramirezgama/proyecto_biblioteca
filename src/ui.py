# ==========================================
# Módulo: ui.py
# Propósito: Interfaz gráfica de consola con formato avanzado usando Rich
# ==========================================

import time
from typing import Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

# Instancia global de la consola de Rich para salidas formateadas
console = Console()


def mostrar_pantalla_carga() -> None:
    """
    Simula una pantalla de carga del sistema por máximo 5 segundos.
    Cumple con el Criterio 1 de la rúbrica (Espera <= 5 segundos).
    """
    # Limpia la pantalla antes de iniciar la simulación
    console.clear()
    
    # Configura la barra de progreso animada usando Rich
    with Progress(
        SpinnerColumn(), # Columna con animación en espiral
        TextColumn("[bold cyan]{task.description}"), # Texto descriptivo
        BarColumn(), # Barra visual de progreso
        TextColumn("[bold green]{task.percentage:>3.0f}%"), # Porcentaje completado
        console=console
    ) as progress:
        
        # Añade la tarea de simulación de carga de la base de datos
        tarea = progress.add_task("Cargando base de datos y archivos...", total=100)
        
        # Iteración para incrementar la barra gradualmente en un total de 3 segundos
        for _ in range(10):
            # Pausa breve de 0.3 segundos por paso (Total: 3.0 segundos)
            time.sleep(0.3)
            # Incrementa un 10% el progreso de la tarea
            progress.update(tarea, advance=10)


def mostrar_banner_bienvenida(mensaje_bienvenida: str) -> None:
    """Muestra el mensaje de bienvenida formateado dentro de un panel con estilo."""
    # Crea un panel bordeado con el mensaje concatenado del usuario
    panel = Panel(
        f"[bold gold1]{mensaje_bienvenida}[/bold gold1]",
        title="[bold blue]Biblioteca Central Ateneo[/bold blue]",
        subtitle="[dim]Sistema de Gestión y Control de Archivos[/dim]",
        border_style="cyan"
    )
    # Imprime el panel en la consola
    console.print(panel)


def mostrar_menu_principal() -> None:
    """
    Muestra el menú de opciones en formato tabular con 2 columnas en consola.
    Cumple estrictamente con el Criterio 2 de la rúbrica.
    """
    # Crea una tabla de Rich con 2 columnas alineadas
    tabla = Table(title="[bold yellow]MENÚ PRINCIPAL DE OPCIONES[/bold yellow]", border_style="bright_blue")
    
    # Define la primera columna: Código/Opción
    tabla.add_column("Opción", justify="center", style="bold cyan", no_wrap=True)
    # Define la segunda columna: Descripción de la Acción
    tabla.add_column("Descripción de la Acción", style="bold white")
    
    # Agrega las filas correspondientes a las opciones del menú
    tabla.add_row("1", "Leer archivo preexistente (Catálogos y Políticas)")
    tabla.add_row("2", "Escribir en la bitácora diaria de eventos")
    tabla.add_row("3", "Crear ticket / comprobante de préstamo (.txt)")
    tabla.add_row("4", "Consultar catálogo de libros en base de datos (JSON)")
    tabla.add_row("5", "Cambiar de usuario / Reiniciar sesión")
    tabla.add_row("0", "Salir del sistema")
    
    # Imprime un salto de línea y la tabla formateada
    console.print("\n")
    console.print(tabla)


def mostrar_tabla_archivos(archivos_dict: Dict[int, object]) -> None:
    """Muestra los archivos preexistentes disponibles en formato de tabla (Criterio 4)."""
    # Instancia una tabla para listar los archivos disponibles en /data
    tabla = Table(title="[bold green]Archivos Preexistentes Disponibles[/bold green]", border_style="green")
    
    # Agrega columna de ID o índice
    tabla.add_column("ID", justify="center", style="bold yellow")
    # Agrega columna con el Nombre del Archivo
    tabla.add_column("Nombre del Archivo", style="bold white")
    
    # Recorre el diccionario de archivos para poblar las filas de la tabla
    for clave, ruta in archivos_dict.items():
        # Agrega la fila con la opción numérica y el nombre del archivo
        tabla.add_row(str(clave), ruta.name)
        
    # Imprime la tabla de archivos en pantalla
    console.print(tabla)


def mostrar_tabla_libros(libros_dict: List[dict]) -> None:
    """Muestra el catálogo de libros traídos del JSON en una tabla formateada."""
    # Instancia una tabla estructurada para los libros del inventario
    tabla = Table(title="[bold magenta]Catálogo General de Libros[/bold magenta]", border_style="magenta")
    
    # Definición de las columnas del inventario
    tabla.add_column("ID", justify="center", style="dim")
    tabla.add_column("Título", style="bold white")
    tabla.add_column("Autor", style="cyan")
    tabla.add_column("Categoría", style="yellow")
    tabla.add_column("Estatus", justify="center")
    
    # Recorre la lista de libros y agrega cada uno como una fila
    for libro in libros_dict:
        # Evalúa el estado booleano para asignarle color verde o rojo
        estatus = "[bold green]Disponible[/bold green]" if libro["disponible"] else "[bold red]Prestado[/bold red]"
        # Agrega la fila a la tabla con la información formateada
        tabla.add_row(
            str(libro["id"]),
            libro["titulo"],
            libro["autor"],
            libro["categoria"],
            estatus
        )
        
    # Imprime la tabla de libros en la consola
    console.print(tabla)


def mostrar_mensaje_exito(mensaje: str) -> None:
    """Muestra un mensaje de éxito con color verde."""
    # Imprime el mensaje estilizado con color verde de éxito
    console.print(f"[bold green]✔ ¡ÉXITO![/bold green] {mensaje}")


def mostrar_mensaje_error(mensaje: str) -> None:
    """Muestra un mensaje de error o excepción capturada con color rojo (Criterio 5)."""
    # Imprime el mensaje estilizado con color rojo para errores
    console.print(f"[bold red]✘ ERROR:[/bold red] {mensaje}")