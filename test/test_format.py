"""
Pruebas unitarias para el módulo Format.
"""

import locale
from datetime import date

from src.eightbits.format import Format


def test_set_locale():
    """Verifica que set_locale() cambie efectivamente el locale del proceso.

    Se usa 'en_US.UTF-8' porque suele estar disponible en la mayoría de
    los sistemas (a diferencia de locales regionales menos comunes, que
    podrían no estar instalados en el entorno donde corren los tests).
    """
    Format.set_locale('en_US.UTF-8')

    # locale.getlocale() sin argumentos consulta LC_CTYPE por defecto.
    assert locale.getlocale() == ('en_US', 'UTF-8')


def test_integer_number():
    """Verifica que integer_number() agregue separador de miles."""
    # Requiere que el locale esté en formato "en_US" (separador de miles
    # con coma) para que el resultado esperado sea determinístico. Por eso
    # fijamos el locale explícitamente en vez de depender del de test_set_locale,
    # ya que pytest no garantiza el orden de ejecución entre archivos/tests.
    Format.set_locale('en_US.UTF-8')

    assert Format.integer_number(1000) == '1,000'


def test_float_number():
    """Verifica que float_number() formatee con separador de miles y 2 decimales."""
    Format.set_locale('en_US.UTF-8')

    assert Format.float_number(1234.56) == '1,234.56'


def test_currency_number():
    """Verifica que currency_number() formatee como moneda según el locale activo."""
    Format.set_locale('en_US.UTF-8')

    assert Format.currency_number(1234.56) == '$1,234.56'


def test_percentage_number():
    """Verifica que percentage_number() formatee con el símbolo de porcentaje."""
    Format.set_locale('en_US.UTF-8')

    assert Format.percentage_number(99.99) == '99.99%'


def test_date_short_format():
    """Verifica el formato corto de date() (equivalente a %x del locale).

    date() no tenía ninguna prueba antes de este cambio; se agrega acá
    aprovechando la migración del resto de las pruebas de formato.
    """
    Format.set_locale('en_US.UTF-8')
    sample_date = date(2025, 2, 20)

    # En locale en_US, %x da como resultado 'MM/DD/YY'.
    assert Format.date(sample_date, short_format=True) == '02/20/25'


def test_date_long_format():
    """Verifica el formato largo de date() ('20 febrero 2025')."""
    sample_date = date(2025, 2, 20)

    # El formato largo está hardcodeado en español dentro de Format.date()
    # (no depende del locale), por eso no hace falta fijar uno acá.
    assert Format.date(
        sample_date, short_format=False) == '20 febrero 2025'


def test_date_invalid_custom_locale_keeps_current_locale():
    """Verifica que un custom_locale inválido no rompa la función.

    Si el locale pedido no existe en el sistema, date() debe capturar el
    error internamente y seguir funcionando con el locale que ya estaba
    activo, en vez de propagar la excepción.
    """
    Format.set_locale('en_US.UTF-8')
    sample_date = date(2025, 2, 20)

    # 'locale-que-no-existe' no es un locale válido en ningún sistema.
    result = Format.date(
        sample_date, custom_locale='locale-que-no-existe', short_format=True
    )

    assert result == '02/20/25'
