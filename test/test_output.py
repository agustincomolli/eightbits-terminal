"""
Pruebas unitarias para el módulo Output.
"""

import os
from src.eightbits.output import Output
from src.eightbits.colors import Colors


def test_clear(monkeypatch):
    """Test para la función clear."""
    monkeypatch.setattr('os.system', lambda x: None)
    Output.clear()
    # Expected output: Console is cleared


def test_console_size(monkeypatch):
    """Test para la función console_size."""
    monkeypatch.setattr('os.get_terminal_size',
                        lambda: os.terminal_size((80, 24)))
    size = Output.console_size()
    assert isinstance(size, tuple)
    assert len(size) == 2


def test_warning(capsys):
    """Verifica que warning() imprima el mensaje coloreado en amarillo.

    Nota: antes este test comprobaba un valor de retorno True/False,
    duplicando exactamente lo que ya cubre test_confirm. warning() no
    pide confirmación ni devuelve nada: solo muestra un mensaje en
    amarillo por stdout. Este test verifica eso específicamente, y de
    paso cubre la corrección del bug donde el color se pasaba como
    argumento posicional en vez de como color=..., lo que hacía que el
    mensaje se imprimiera sin colorear y con el código ANSI crudo
    pegado como texto al final.

    Args:
        capsys: fixture de pytest que captura stdout/stderr.
    """
    Output.warning("This is a warning message")
    captured = capsys.readouterr()

    # El mensaje debe estar presente...
    assert "This is a warning message" in captured.out
    # ...y el código ANSI de color amarillo debe envolverlo, no aparecer
    # suelto como texto plano al final del mensaje.
    assert Colors.YELLOW in captured.out


def test_error(capsys):
    """Verifica que error() escriba en sys.stderr, no en sys.stdout.

    Este test no existía antes: error() se agregó a stderr como parte de
    separar mensajes de error de la salida normal del programa (así, si
    alguien redirige stdout a un archivo, los errores se siguen viendo
    en pantalla). capsys separa ambos streams, así que podemos verificar
    la separación directamente.

    Args:
        capsys: fixture de pytest que captura stdout/stderr por separado.
    """
    Output.error("Something went wrong")
    captured = capsys.readouterr()

    # No debe aparecer en la salida estándar...
    assert "Something went wrong" not in captured.out
    # ...sino en la salida de error, coloreado en rojo.
    assert "Something went wrong" in captured.err
    assert Colors.RED in captured.err


def test_confirm(monkeypatch):
    """Test para la función confirm."""
    monkeypatch.setattr('builtins.input', lambda _: 's')
    assert Output.confirm("Are you sure?") is True
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    assert Output.confirm("Are you sure?") is False


def test_typewriter(monkeypatch, capsys):
    """Test para el efecto de escritura."""
    monkeypatch.setattr('time.sleep', lambda _: None)
    Output.typewriter("Typing effect")
    captured = capsys.readouterr()
    assert "Typing effect" in captured.out


def test_print_title(capsys):
    """Test para la función print_title."""
    Output.print_title("Title", color=Colors.DEFAULT, underline="-")
    captured = capsys.readouterr()
    assert "Title" in captured.out
    assert "-----" in captured.out
