# EightBits Terminal by 8 Bits

Biblioteca moderna para crear aplicaciones de terminal elegantes en Python, con
entrada de datos validada, salida con colores y alineación, tablas formateadas
y formateo de números/fechas según el locale.

## 📦 Instalación

```bash
pip install eightbits-terminal
```

**Requisitos:** Python 3.9 o superior.

## 🧩 Módulos

La librería está organizada en seis clases de utilidad estática (ninguna se
instancia; todos sus métodos son `@staticmethod`), cada una con una única
responsabilidad:

| Clase | Responsabilidad |
|---|---|
| [`Input`](#input) | Leer y validar datos ingresados por el usuario |
| [`Output`](#output) | Escribir en la consola (imprimir, limpiar, colorear, alinear) |
| [`Format`](#format) | Transformar números y fechas en texto formateado, sin imprimir nada |
| [`Colors`](#colors) | Códigos ANSI de color y utilidades para aplicarlos a un texto |
| [`Alignment`](#alignment) | Constantes y validación de alineación de texto |
| [`Tabular`](#tabular) | Renderizar listas de diccionarios como tabla en consola |

> **Nota sobre `Format` vs `Output`:** si vienen de una versión anterior de
> esta librería, `Output` solía incluir `format_int()`, `format_currency()`,
> `set_locale()`, etc. Esos métodos se movieron a la clase `Format`, porque
> son funciones puras de transformación de datos (no hacen I/O de consola) y
> merecían vivir separadas de `Output`. Ver [Migrando desde v1.x](#-migrando-desde-v1x).

---

### Input

Entrada de datos por consola, con validación integrada y reintento automático
ante datos inválidos.

```python
Input.text(prompt, color_prompt=Colors.DEFAULT, color_input=Colors.DEFAULT) -> str
Input.integer(prompt, color_prompt, color_input, min_value=None, max_value=None) -> int
Input.float(prompt, color_prompt, color_input, min_value=None, max_value=None) -> float
Input.confirm(prompt, color_prompt, color_input) -> bool
Input.date(prompt, color_prompt, color_input) -> str
Input.email(prompt, color_prompt, color_input) -> str
Input.password(prompt, color_prompt, color_input) -> str
Input.choice(title, options, color_prompt, color_input) -> int
```

- `password()` usa `getpass` internamente, así que la contraseña no se
  muestra en pantalla mientras se escribe (esto significa que no funciona
  si se simula la entrada con `input()` mockeado en tests; hay que
  mockear `getpass.getpass` en su lugar, o alimentar `stdin` directamente).
- `choice()` valida que la opción elegida sea un número dentro del rango de
  opciones ofrecidas, y vuelve a preguntar si no lo es.

### Output

Todo lo que efectivamente escribe algo en la consola.

```python
Output.print(*objects, sep=' ', end='\n', color=Colors.DEFAULT,
             alignment=Alignment.LEFT, width=0, fill=True,
             file=None, flush=False) -> None
Output.clear() -> None
Output.console_size() -> tuple[int, int]
Output.press_enter_to_continue() -> None
Output.error(message: str) -> None
Output.warning(message: str) -> None
Output.confirm(message: str) -> bool
Output.typewriter(text: str) -> None
Output.print_title(title, color, underline="*", alignment=Alignment.CENTER) -> None
Output.show_progress_bar(iteration: int, total: int, length: int = 50) -> None
```

Detalles a tener en cuenta:

- **`color` va siempre como argumento nombrado**, nunca posicional:
  `Output.print("hola", color=Colors.GREEN)`, no
  `Output.print("hola", Colors.GREEN)`. Como `print()` recibe `*objects`
  primero, pasar el color sin `color=` hace que se trate como un objeto
  más a imprimir, en vez de aplicarse como color.
- **`fill`** controla si el texto se rellena hasta el ancho de la consola
  (`True`, por defecto, pensado para líneas completas) o se imprime tal
  cual (`False`, pensado para fragmentos de una misma línea, como celdas
  de una tabla que se arman con varias llamadas seguidas).
- **`file`** permite redirigir la salida (por ejemplo a `sys.stderr`, o a
  un `io.StringIO()` en un test) sin tocar la consola real.
- **`error()`** escribe en `sys.stderr`; el resto de los métodos (incluido
  `warning()`) escriben en `sys.stdout`. En una terminal normal esto no se
  nota (ambos streams se ven mezclados en pantalla); la diferencia importa
  si alguien redirige la salida estándar a un archivo.
- `show_progress_bar()` lanza `ValueError` si `total <= 0` o si
  `iteration` está fuera de `[0, total]`, en vez de fallar silenciosamente
  o dividir por cero.

### Format

Funciones puras: reciben un dato, devuelven un `str` ya formateado. No
imprimen nada ni dependen de `Colors`/`Alignment`.

```python
Format.set_locale(region: str) -> None
Format.integer_number(value: int) -> str
Format.float_number(value: float) -> str
Format.currency_number(value: float) -> str
Format.percentage_number(value: float) -> str
Format.date(date, custom_locale="", short_format=True) -> str
```

- Todas (salvo `date()` con `short_format=False`, que usa `%B` del locale
  activo) dependen del locale configurado con `set_locale()`. Si no se
  llamó a `set_locale()`, se usa el locale por defecto del sistema.
- `set_locale()` modifica el locale de **todo el proceso** (usa el módulo
  `locale` de Python, que es estado global, no por hilo). Si tu aplicación
  usa threads o async, tenelo en cuenta: cambiar el locale desde un hilo
  afecta a los demás.
- `date()` restaura el locale original al terminar si se le pasó
  `custom_locale`, incluso si ese locale no existe en el sistema (en ese
  caso, sigue con el locale que ya estaba activo, sin lanzar excepción).

### Colors

Constantes de color ANSI y utilidades para aplicarlas a un texto sin pasar
por `Output` (por ejemplo, para componer un string coloreado antes de
imprimirlo con otra herramienta).

```python
Colors.RED, Colors.GREEN, Colors.YELLOW, Colors.BLUE,
Colors.MAGENTA, Colors.CYAN, Colors.WHITE, Colors.DEFAULT,
Colors.BOLD, Colors.UNDERLINE

Colors.validate_color(color: str) -> str   # color si es válido, si no Colors.DEFAULT
Colors.colorize(text: str, color: str) -> str
Colors.bold(text: str) -> str
Colors.underline(text: str) -> str
```

### Alignment

Constantes de alineación, usadas por `Output.print()`, `Output.print_title()`
y `Tabular`.

```python
Alignment.LEFT   # 'left'
Alignment.CENTER # 'center'
Alignment.RIGHT  # 'right'

Alignment.validate_alignment(alignment: str) -> str  # alignment si es válido, si no Alignment.LEFT
```

### Tabular

Renderiza una lista de diccionarios como tabla, ajustando el ancho de las
columnas al espacio disponible (dividiendo el contenido en varias líneas si
hace falta).

```python
Tabular.print(data: list[dict], title: str = "", max_width: int = 0) -> None
```

- Todas las filas de `data` deben tener las mismas claves; las claves del
  primer diccionario se usan como encabezado de columna.
- Si `max_width` es 0 (por defecto), usa el ancho actual de la terminal.
- Si `data` está vacío, imprime `"No hay datos para mostrar."` en vez de
  una tabla vacía.

---

## 🎮 Ejemplo de uso

```python
import time
from datetime import datetime
from eightbits import Input, Output, Colors, Alignment, Tabular, Format

# --- Entrada de datos ---
nombre = Input.text("Ingrese su nombre: ", Colors.GREEN, Colors.BLUE)
edad = Input.integer("Ingrese su edad: ", Colors.GREEN, Colors.BLUE, 0, 120)
peso = Input.float("Ingrese su peso: ", Colors.GREEN, Colors.BLUE, 50, 150)
continuar = Input.confirm("¿Deseas continuar? (si/no): ", Colors.GREEN, Colors.BLUE)

# --- Salida formateada (color siempre como argumento nombrado) ---
Output.print(nombre, color=Colors.WHITE)
Output.print(edad, color=Colors.WHITE)
Output.print(peso, color=Colors.WHITE)
Output.print(continuar, color=Colors.WHITE)

Output.warning("Esto es un mensaje de advertencia.")
Output.error("Esto es un mensaje de error.")       # va a sys.stderr
Output.confirm("Esto es un mensaje de confirmación.")
Output.clear()

# --- Formateo de datos (clase Format, separada de Output) ---
Format.set_locale("es_AR.UTF-8")
Output.print(f"Mi sueldo es de {Format.currency_number(367000)}", color=Colors.GREEN)
Output.print(f"Número formateado: {Format.integer_number(1000)}")
Output.print(f"Porcentaje: {Format.percentage_number(99.99)}")
Output.print(f"Fecha: {Format.date(datetime.now())}")

# --- Alineación de texto ---
Output.print("Texto alineado a la izquierda")
Output.print("Texto centrado", color=Colors.BLUE, alignment=Alignment.CENTER)
Output.print("Texto alineado a la derecha", alignment=Alignment.RIGHT)

# --- Tabla ---
data = [
    {"nombre": "Juan Carlos González", "ciudad": "Madrid"},
    {"nombre": "María", "ciudad": "Barcelona"},
]
Tabular.print(data, title="Lista de Usuarios")
Tabular.print(data, title="Lista de Usuarios", max_width=80)  # ancho fijo

# --- Barra de progreso ---
total = 100
for i in range(total + 1):
    Output.show_progress_bar(i, total)
    time.sleep(0.02)

# --- Título con subrayado ---
Output.print_title("Esto es un título", Colors.GREEN, "=", Alignment.CENTER)
```

Un ejemplo más completo, que recorre todos los métodos de la librería, está
en [`examples/demo.py`](examples/demo.py). Para ejecutarlo:

```bash
python -m examples.demo
```

## 🔄 Migrando desde v1.x

Si tu código llama a estos métodos de `Output`, reemplazalos por sus
equivalentes en `Format`:

| Antes (`Output`) | Ahora (`Format`) |
|---|---|
| `Output.set_locale(...)` | `Format.set_locale(...)` |
| `Output.format_int(...)` | `Format.integer_number(...)` |
| `Output.format_float(...)` | `Format.float_number(...)` |
| `Output.format_currency(...)` | `Format.currency_number(...)` |
| `Output.format_percentage(...)` | `Format.percentage_number(...)` |
| `Output.format_date(...)` | `Format.date(...)` |

Además, si llamabas a `Output.print(texto, Colors.ALGO)` pasando el color
como segundo argumento posicional, cambialo a
`Output.print(texto, color=Colors.ALGO)`: la firma actual recibe `*objects`
primero, así que un color sin `color=` se trataba (incorrectamente) como
otro texto más a imprimir, y nunca se aplicaba.

## 🧪 Tests

```bash
pip install pytest
pytest
```

## 🛠️ Requisitos

- Python 3.9 o superior

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE)
para más detalles.

## 🎥 Video de presentación

https://youtu.be/2EZBuveqP9E

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor, siéntete libre de:

- Reportar bugs
- Sugerir nuevas funcionalidades
- Enviar pull requests
