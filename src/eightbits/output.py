"""
Módulo que contiene las funciones para imprimir texto con colores.

Contenido
---------
- Clase Output: contiene las funciones para imprimir texto con colores.
"""
import os
import subprocess
import time
from .colors import Colors
from .alignment import Alignment


class Output:
    """Clase que contiene las funciones para imprimir texto con colores."""

    def __new__(cls):
        raise TypeError(
            "Output is a static utility class and cannot be instantiated."
        )

    @staticmethod
    def print(text: object, color: str = Colors.DEFAULT,
              alignment: str = Alignment.LEFT, width: int = 0) -> None:
        """Imprime un texto con un color y alineación.

        Args:
            text (object): Texto a imprimir.
            color (str, optional): Color a aplicar al texto.
            alignment (str, optional): Alineación del texto ('left', 'center', 'right').
            width (int, optional): Ancho para centrar el texto. Si no se proporciona,
            se usará el ancho de la terminal.
        """
        # Validar el color
        color = Colors.validate_color(color)
        # Validar la alineación
        alignment = Alignment.validate_alignment(alignment)

        text = Colors.colorize(str(text), color)

        if width == 0:
            width = Output.console_size()[0]

        if alignment == Alignment.CENTER:
            print(text.center(width))
        elif alignment == Alignment.RIGHT:
            print(text.rjust(width))
        else:
            print(text.ljust(width))

    @staticmethod
    def clear() -> None:
        """Limpia la consola."""
        subprocess.run('cls' if os.name == 'nt' else 'clear',
                       shell=True,
                       check=False)

    @staticmethod
    def console_size() -> tuple[int, int]:
        """Obtiene el tamaño de la consola.

        Returns:
            tuple[int, int]: Tamaño de la consola.
        """
        try:
            return os.get_terminal_size()
        except OSError:
            # Proporcionar un tamaño de consola predeterminado
            return (80, 24)

    @staticmethod
    def press_enter_to_continue() -> None:
        """Pide al usuario que presione Enter para continuar."""
        input(
            f"Presione {Colors.colorize('ENTER', Colors.YELLOW)} para continuar...")

    @staticmethod
    def error(message: str) -> None:
        """Muestra un mensaje de error.

        Args:
            message (str): Mensaje de error.
        """
        Output.print(message, Colors.RED)

    @staticmethod
    def warning(message: str) -> None:
        """Muestra un mensaje de advertencia.

        Args:
            message (str): Mensaje de advertencia.
        """
        Output.print(message, Colors.YELLOW)

    @staticmethod
    def confirm(message: str) -> bool:
        """Muestra un mensaje de confirmación al usuario y solicita una respuesta
        afirmativa o negativa.

        Args:
            message (str): Mensaje de confirmación a mostrar.

        Returns:
            bool: True si el usuario responde afirmativamente, False en caso contrario.

        """
        while True:
            response = input(f"{message} (s/n) ").lower()
            if response in ("s", "y"):
                return True
            return False

    @staticmethod
    def typewriter(text: str) -> None:
        """Imprime los caracteres de la cadena de texto uno por uno en un intervalo de
        tiempo determinado para simular el efecto de que se está escribiendo en tiempo
        real.

        Args:
            text (str): La cadena de texto que se quiere imprimir con efecto de tipeo.
        """
        # Itera a través de cada carácter en la cadena de texto
        for char in text:
            # Imprime el carácter sin un salto de línea al final, y hace flush del
            # flujo de salida inmediatamente
            print(char, end='', flush=True)
            # Espera un breve intervalo de tiempo antes de imprimir el siguiente carácter
            time.sleep(0.05)
        # Imprime un salto de línea al final para separar esta salida de la próxima en la consola
        print("\n")

    @staticmethod
    def print_title(title: str, color: str, underline: str = "*",
                    alignment: str = Alignment.LEFT, width: int = 0) -> None:
        """Imprime un título con un color y un subrayado.

        Args:
            title (str): Título a imprimir.
            color (str): Color del título.
            underline (str, optional): Carácter de subrayado. Por defecto es "*".
            alignment (str, optional): Alineación del texto ('left', 'center', 'right').
            width (int, optional): Ancho para centrar el texto. Si no se proporciona,
            se usará el ancho de la terminal.
        """
        Output.print(title.title(), color=color,
                     alignment=alignment, width=width)
        Output.print(underline * len(title), color=color,
                     alignment=alignment, width=width)

    @staticmethod
    def show_progress_bar(iteration: int, total: int, length: int = 50) -> None:
        """Muestra una barra de progreso en la consola.

        Args:
            iteration (int): Iteración actual.
            total (int): Número total de iteraciones.
            length (int, optional): Longitud de la barra de progreso. Por defecto es 50.
        """
        percent = f"{100 * (iteration / float(total)):.1f}"
        filled_length = int(length * iteration // total)
        progress_bar = '█' * filled_length + '-' * (length - filled_length)
        print(f'\r|{progress_bar}| {percent}% Completo', end='\r')
        if iteration == total:
            print()
