"""
Módulo que contiene las funciones para formatear un texto en diferentes tipos.

Contenido
---------
- Clase Format: contiene las funciones para formatear un texto en diferentes tipos.
"""

import locale
from datetime import date as DateType


class Format:
    """Clase que contiene las funciones para formatear un texto."""

    def __new__(cls):
        raise TypeError(
            "Format is a static utility class and cannot be instantiated."
        )

    @staticmethod
    def set_locale(region: str) -> None:
        """Establece la localidad regional de la consola.

        Args:
            region (str): Localidad regional a establecer.
        """
        locale.setlocale(locale.LC_ALL, region)

    @staticmethod
    def integer_number(value: int) -> str:
        """Formatea un número entero con separadores de miles y decimales.

        Args:
            value (int): Número entero a formatear.

        Returns:
            str: Número entero formateado con separadores de miles y decimales.
        """
        return locale.format_string("%d", value, grouping=True)

    @staticmethod
    def float_number(value: float) -> str:
        """Formatea un número decimal con separadores de miles y decimales.

        Args:
            value (float): Número decimal a formatear.

        Returns:
            str: Número decimal formateado con separadores de miles y decimales.
        """
        return locale.format_string("%.2f", value, grouping=True)

    @staticmethod
    def currency_number(value: float) -> str:
        """Formatea un número como una cantidad de dinero con separadores de miles y decimales.

        Args:
            value (float): Número a formatear como una cantidad de dinero.

        Returns:
            str: Número formateado como una cantidad de dinero con separadores de miles y decimales.
        """
        # locale.setlocale(locale.LC_ALL, locale.getlocale()[0])
        return locale.currency(value, grouping=True)

    @staticmethod
    def percentage_number(value: float) -> str:
        """Formatea un número como un porcentaje con separadores de miles y decimales.

        Args:
            value (float): Número a formatear como un porcentaje.

        Returns:
            str: Número formateado como un porcentaje con separadores de miles y decimales.
        """
        return locale.format_string("%.2f%%", value, grouping=True)

    @staticmethod
    def date(date: DateType, custom_locale: str = "", short_format: bool = True) -> str:
        """Formatea una fecha según el locale actual o uno específico.

        Args:
            date (datetime.date): Objeto date a formatear
            custom_locale (str): Locale específico a usar (opcional)
            short_format (bool): True para formato corto (20/02/2025), False para 
            formato largo (20 de febrero de 2025)

        Returns:
            str: Fecha formateada según el locale y formato especificado
        """
        # Guardar el locale actual
        current_locale = locale.getlocale(locale.LC_TIME)

        try:
            # Establecer nuevo locale si se especifica
            if custom_locale:
                try:
                    locale.setlocale(locale.LC_TIME, custom_locale)
                except locale.Error:
                    # Si falla, mantener el locale actual (equivalente a custom_locale="")
                    pass

            if short_format:
                # %x: formato de fecha corto según el locale
                return date.strftime("%x")

            # Formato largo: "20 de febrero de 2025"
            return date.strftime("%d de %B de %Y").lower()

        finally:
            # Restaurar el locale original si se cambió
            if custom_locale:
                try:
                    locale.setlocale(locale.LC_TIME, current_locale)
                except locale.Error:
                    # Si falla, mantener el locale actual
                    pass
