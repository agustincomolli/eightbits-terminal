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
    def print(*objects: object, sep: str = ' ', end: str = '\n',
              color: str = Colors.DEFAULT, alignment: str = Alignment.LEFT,
              width: int = 0) -> None:
        """Imprime objetos con un color y alineación específicos.

        Args:
            *objects (object): Uno o más objetos a imprimir.
            sep (str, optional): Separador entre objetos. Por defecto es ' '.
            end (str, optional): Cadena final al terminar la impresión. Por defecto es '\n'.
            color (str, optional): Color a aplicar al texto.
            alignment (str, optional): Alineación del texto ('left', 'center', 'right').
            width (int, optional): Ancho para la alineación. Si es 0, usa la terminal.
        """
        # 1. Validar color y alineación
        color = Colors.validate_color(color)
        alignment = Alignment.validate_alignment(alignment)

        # 2. Unir los objetos usando el separador 'sep'
        full_text = sep.join(str(obj) for obj in objects)

        # 3. Aplicar color al texto completo ya unido
        text_color = Colors.colorize(full_text, color)

        # 4. Calcular ancho de la pantalla
        if width == 0:
            width = Output.console_size()[0]

        # 5. Alinear e imprimir aplicando el parámetro 'end'
        if alignment == Alignment.CENTER:
            print(text_color.center(width), end=end)
        elif alignment == Alignment.RIGHT:
            print(text_color.rjust(width), end=end)
        else:
            print(text_color.ljust(width), end=end)

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

            if response == "n":
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
        if total <= 0:
            raise ValueError(
                f"'total' debe ser mayor a 0, se recibió: {total}"
            )
        if iteration < 0 or iteration > total:
            raise ValueError(
                f"'iteration' debe estar entre 0 y {total}, se recibió: {iteration}"
            )

        percent = f"{100 * (iteration / float(total)):.1f}"
        filled_length = int(length * iteration // total)
        progress_bar = '█' * filled_length + '-' * (length - filled_length)
        print(f'\r|{progress_bar}| {percent}% Completo', end='\r')
        if iteration == total:
            print()
