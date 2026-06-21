"""
Utility helpers for the budget_tracker package.
"""

from datetime import date, datetime
from decimal import Decimal, InvalidOperation

DATE_FORMAT = "%Y-%m-%d"
CURRENCY_DECIMAL_PLACES = Decimal("0.01")

MIN_MONTH = 1
MAX_MONTH = 12


def parse_date(value):
    """
    Convert a date-like value into a datetime.date instance.

    :param value: Date value as ``date``, ``datetime``,
        or ``YYYY-MM-DD``.
    :return: Normalized ``date`` instance.
    :raises TypeError: If the input type is unsupported.
    :raises ValueError: If the string does not match
        ``YYYY-MM-DD``.
    """
    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    if isinstance(value, str):
        stripped_value = value.strip()

        if not stripped_value:
            raise ValueError("date must not be empty")

        return datetime.strptime(
            stripped_value,
            DATE_FORMAT,
        ).date()

    raise TypeError(
        "date must be a date, datetime, or YYYY-MM-DD string"
    )


def format_date(value):
    """
    Format a date-like value as YYYY-MM-DD.

    :param value: Date value as ``date``, ``datetime``,
        or ``YYYY-MM-DD``.
    :return: Date formatted as a string.
    """
    return parse_date(value).strftime(DATE_FORMAT)


def to_decimal(value):
    """
    Convert a numeric value into a money-safe Decimal.

    :param value: Value to convert.
    :return: Decimal rounded to two places.
    :raises TypeError: If the value cannot represent money.
    :raises ValueError: If the value is empty or not numeric.
    """
    if isinstance(value, bool):
        raise TypeError(
            "amount must be a number, not a boolean"
        )

    if isinstance(value, str) and not value.strip():
        raise ValueError("amount must not be empty")

    try:
        decimal_value = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(
            "amount must be numeric"
        ) from exc

    return decimal_value.quantize(
        CURRENCY_DECIMAL_PLACES
    )


def month_key(year, month):
    """
    Return a stable YYYY-MM key for monthly reports.

    :param year: Four-digit year.
    :param month: Month number from 1 to 12.
    :return: Formatted month key.
    :raises ValueError: If month is outside 1 through 12.
    """
    if not MIN_MONTH <= month <= MAX_MONTH:
        raise ValueError(
            "month must be between 1 and 12"
        )

    return f"{year:04d}-{month:02d}"


def format_currency(amount):
    """
    Format a money value with two decimal places.

    :param amount: Numeric amount to format.
    :return: Currency string prefixed with ``KRW``.
    """
    return f"KRW {to_decimal(amount):,.2f}"
