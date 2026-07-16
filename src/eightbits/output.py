"""
Módulo que contiene las funciones para imprimir texto con colores.

Contenido
---------
- Clase Output: contiene las funciones para imprimir texto con colores.
"""
import os
import subprocess
import time
import sys
from typing import Optional, TextIO
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
              width: int = 0, fill: bool = True, file: Optional[TextIO] = None,
              flush: bool = False) -> None:
        """Imprime objetos con un color y alineación específicos.

        Funciona como el print() estándar de Python (acepta sep, end, file y
        flush con el mismo significado), pero además permite aplicar color y
        alinear el texto al ancho de la consola.

        Args:
            *objects (object): Uno o más objetos a imprimir. Se convierten a
                str() igual que hace el print() estándar.
            sep (str, optional): Separador entre objetos. Por defecto es ' '.
            end (str, optional): Cadena final al terminar la impresión.
                Por defecto es '\n'.
            color (str, optional): Color a aplicar al texto (ver clase Colors).
            alignment (str, optional): Alineación del texto ('left', 'center',
                'right').
            width (int, optional): Ancho para la alineación. Si es 0, usa el
                ancho actual de la terminal.
            fill (bool, optional): Si es False, no aplica relleno/alineación al
                ancho de la terminal, y el texto se imprime tal cual. Útil para
                imprimir fragmentos de una misma línea (por ejemplo, celdas de
                una tabla) sin que cada fragmento se estire hasta el ancho de la
                consola. Por defecto es True.
            file (TextIO, optional): Stream donde escribir. Si es None
                (default), se usa sys.stdout evaluado en el momento de la
                llamada, no al definir la función. Esto es importante: usar
                directamente `file: TextIO = sys.stdout` como valor por
                defecto lo fijaría una sola vez, cuando Python arma la
                función, y ya no reaccionaría si algo más adelante reemplaza
                sys.stdout (como hacen los tests con capsys, o Jupyter).
            flush (bool, optional): Si es True, fuerza el vaciado inmediato del
                buffer de salida, igual que en el print() estándar. Por defecto
                es False.
        """
        # 1. Resolver sys.stdout en tiempo de llamada, no en tiempo de definición
        if file is None:
            file = sys.stdout

        # 2. Validar color y alineación (si no son válidos, se usan los
        #    valores por defecto de cada clase)
        color = Colors.validate_color(color)
        alignment = Alignment.validate_alignment(alignment)

        # 3. Unir todos los objetos recibidos en un solo string, igual que hace
        #    internamente el print() estándar con el parámetro 'sep'
        full_text = sep.join(str(obj) for obj in objects)

        # 4. Envolver el texto ya unido con los códigos ANSI del color elegido
        text_color = Colors.colorize(full_text, color)

        # 5. Si no se pide relleno, escribir el texto coloreado tal cual, sin
        #    alinear ni rellenar con espacios, y terminar acá
        if not fill:
            print(text_color, end=end, file=file, flush=flush)
            return

        # 6. Si no se especificó un ancho, usar el ancho actual de la consola
        #    (se recalcula en cada llamada por si la terminal cambió de tamaño)
        if width == 0:
            width = Output.console_size()[0]

        # 7. Alinear el texto ya coloreado dentro de ese ancho y escribirlo en
        #    el stream indicado (file), respetando 'end' y 'flush'
        if alignment == Alignment.CENTER:
            aligned_text = text_color.center(width)
        elif alignment == Alignment.RIGHT:
            aligned_text = text_color.rjust(width)
        else:
            aligned_text = text_color.ljust(width)

        print(aligned_text, end=end, file=file, flush=flush)

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
        """Muestra un mensaje de error en rojo.

        El mensaje se envía a sys.stderr (no a sys.stdout) porque
        semánticamente es un error, no salida normal del programa. En una
        terminal común esto no cambia nada visualmente: el mensaje se sigue
        viendo igual, mezclado con el resto de la salida. La diferencia solo
        se nota si alguien redirige la salida normal a un archivo (por
        ejemplo `python script.py > salida.txt`): en ese caso el archivo
        queda limpio y el error se sigue mostrando en la pantalla.

        Args:
            message (str): Mensaje de error a mostrar.
        """
        # OJO: color se pasa como keyword argument, no posicional. Output.print
        # recibe *objects primero, así que un Colors.RED posicional se
        # interpretaría como "otro objeto a imprimir" y no como el color.
        Output.print(message, color=Colors.RED, file=sys.stderr)

    @staticmethod
    def warning(message: str) -> None:
        """Muestra un mensaje de advertencia.

        Args:
            message (str): Mensaje de advertencia.
        """
        Output.print(message, color=Colors.YELLOW)

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
