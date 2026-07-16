"""
Pruebas unitarias para el módulo Tabular.
"""

from src.eightbits.tabular import Tabular


def test_get_header():
    """Debe obtener correctamente los encabezados."""
    row = {
        "Name": "Alice",
        "Age": 30,
        "Country": "Argentina"
    }

    assert Tabular._get_header(row) == ["Name", "Age", "Country"]


def test_get_initial_widths():
    """Debe calcular correctamente el ancho inicial de cada columna."""
    data = [
        {"Name": "Alice", "Age": 30},
        {"Name": "Christopher", "Age": 100}
    ]

    widths = Tabular._get_initial_widths(data)

    assert widths["Name"] == len("Christopher")
    assert widths["Age"] == len("100")


def test_adjust_column_widths_no_resize():
    """No debe modificar los anchos cuando hay espacio suficiente."""
    initial = {
        "Name": 10,
        "Age": 10
    }

    adjusted = Tabular._adjust_column_widths(initial, 80)

    assert adjusted == initial


def test_adjust_column_widths_resize():
    """Debe reducir el ancho de las columnas cuando el espacio es insuficiente."""
    initial = {
        "Name": 40,
        "Description": 60
    }

    adjusted = Tabular._adjust_column_widths(initial, 40)

    assert sum(adjusted.values()) < sum(initial.values())

    for width in adjusted.values():
        assert width >= Tabular.MIN_COLUMN_WIDTH


def test_print_empty(capsys):
    """Debe informar cuando no existen datos."""
    Tabular.print([])

    captured = capsys.readouterr()

    assert "No hay datos para mostrar." in captured.out


def test_print_simple_table(capsys):
    """Debe imprimir correctamente una tabla sencilla."""

    data = [
        {
            "Name": "Alice",
            "Age": 30
        },
        {
            "Name": "Bob",
            "Age": 40
        }
    ]

    Tabular.print(data, max_width=80)

    output = capsys.readouterr().out

    assert "NAME" in output
    assert "AGE" in output

    assert "Alice" in output
    assert "Bob" in output

    assert "+" in output
    assert "|" in output


def test_print_with_title(capsys):
    """Debe imprimir el título cuando se especifica."""

    data = [
        {
            "Name": "Alice",
            "Age": 30
        }
    ]

    Tabular.print(
        data,
        title="Employees",
        max_width=80
    )

    output = capsys.readouterr().out

    assert "Employees" in output
    assert "NAME" in output


def test_print_wrap_long_text(capsys):
    """Debe dividir el texto largo en varias líneas."""

    data = [
        {
            "Name": "Alice",
            "Description": (
                "This is a very long description that should wrap "
                "across multiple lines."
            )
        }
    ]

    Tabular.print(data, max_width=40)

    output = capsys.readouterr().out

    assert "Alice" in output

    assert "This is" in output
    assert "description" in output


def test_print_separator(capsys):
    """Debe imprimir correctamente el separador."""

    Tabular._print_separator(
        2,
        [10, 10]
    )

    output = capsys.readouterr().out.strip()

    # El texto ahora viene envuelto en códigos ANSI (incluso con el color
    # por defecto), así que buscamos el contenido en vez de comparar el
    # string completo desde el principio/final.
    assert "+-" in output
    assert "-+" in output
    assert "-" in output


def test_print_row(capsys):
    """Debe imprimir correctamente una fila."""

    row = {
        "Name": "Alice",
        "Age": 30
    }

    widths = {
        "Name": 10,
        "Age": 10
    }

    Tabular._print_row(row, widths)

    output = capsys.readouterr().out

    assert "Alice" in output
    assert "30" in output
    assert "|" in output
