"""
Ejemplo de uso de todas las funciones del proyecto eightbits.

Para ejecutar el ejemplo, ejecutar python -m examples.demo.
"""
import time
from datetime import datetime
from src.eightbits import Input, Output, Colors, Alignment, Tabular, Format


def main() -> None:
    """ Función principal del módulo. """
    # Entrada de datos
    name = Input.text("Ingresa tu nombre: ", Colors.GREEN, Colors.BLUE)
    Output.print(name, color=Colors.WHITE)

    age = Input.integer("Ingresa tu edad: ",
                           Colors.GREEN, Colors.BLUE, 1, 99)
    Output.print(age, color=Colors.WHITE)

    weight = Input.float(
        "Ingresa tu peso: ", Colors.GREEN, Colors.BLUE, 50, 150)
    Output.print(weight, color=Colors.WHITE)

    next_step = Input.confirm(
        "¿Deseas continuar? (si/no): ", Colors.GREEN, Colors.BLUE)
    Output.print(next_step, color=Colors.WHITE)

    date_birth = Input.date("Ingresa tu fecha de nacimiento: ",
                            Colors.GREEN, Colors.BLUE)
    Output.print(date_birth, color=Colors.WHITE)

    email = Input.email("Ingresa tu email: ", Colors.GREEN, Colors.BLUE)
    Output.print(email, color=Colors.WHITE)

    password = Input.password("Ingresa tu contraseña: ",
                              Colors.GREEN, Colors.BLUE)
    Output.print(password, color=Colors.WHITE)

    choice = Input.choice("Selecciona una opción: ",
                        ["Opción 1", "Opción 2", "Opción 3"],
                        Colors.GREEN, Colors.BLUE)
    Output.print(choice, color=Colors.WHITE)

    # Salida formateada
    Output.warning("Esto es un mensaje de advertencia.")
    Output.error("Esto es un mensaje de error.")
    Output.confirm("Esto es un mensaje de confirmación.")
    Output.clear()
    Output.print("Esto es un mensaje de limpieza.", color=Colors.RED)

    # Formateo (clase Format, separada de Output)
    Format.set_locale("es_AR.UTF-8")
    Output.print(
        f"Mi sueldo es de {Format.currency_number(367000)}",
        color=Colors.GREEN
    )

    # Alineación de texto
    Output.print("Texto alineado a la izquierda")
    Output.print("Texto centrado", color=Colors.BLUE, alignment=Alignment.CENTER)
    Output.print("Texto alineado a la derecha", alignment=Alignment.RIGHT)

    # Datos de ejemplo para la tabla
    data = [
        {
            "nombre": "Juan Carlos González",
            "descripción": "Este es un texto muy largo que necesitará ser dividido",
            "ciudad": "Madrid"
        },
        {
            "nombre": "María",
            "descripción": "Texto corto",
            "ciudad": "Barcelona"
        }
    ]

    # Usar el método estático directamente
    Tabular.print(data, title="Lista de Usuarios")

    # O especificar un ancho máximo
    Tabular.print(data, title="Lista de Usuarios", max_width=80)

    # Barra de progreso
    total_iterations = 100
    for i in range(total_iterations + 1):
        Output.show_progress_bar(i, total_iterations)
        time.sleep(0.1)

    # Efecto de máquina de escribir
    Output.typewriter("Esto es un efecto de máquina de escribir.")

    # Formateo de números
    Output.print(
        f"Número entero formateado: {Format.integer_number(1000)}",
        color=Colors.WHITE
    )
    Output.print(
        f"Número decimal formateado: {Format.float_number(1234.56)}",
        color=Colors.WHITE
    )
    Output.print(
        f"Porcentaje formateado: {Format.percentage_number(99.99)}",
        color=Colors.WHITE
    )

    # Formateo de fecha
    current_date = datetime.now()
    Output.print(
        f"Fecha formateada: {Format.date(current_date)}",
        color=Colors.WHITE
    )

    # Título con subrayado
    Output.print_title("Esto es un título", Colors.GREEN, "=", Alignment.CENTER)


if __name__ == "__main__":
    main()
