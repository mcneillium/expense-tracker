"""Currency helpers shared by the GUI and the tests.

Money is held as Decimal, never float, so totals are exact to the penny:
0.1 + 0.2 is 0.30000000000000004 in floating point but exactly 0.3 here.
The rates are fixed examples, not live exchange rates.
"""

from decimal import Decimal, InvalidOperation

import pandas as pd

CONVERSION_RATES: dict[str, Decimal] = {
    "£": Decimal("1"),
    "$": Decimal("0.75"),  # example: 1 USD = 0.75 GBP
    "€": Decimal("0.85"),  # example: 1 EUR = 0.85 GBP
    "¥": Decimal("0.0055"),  # example: 1 JPY = 0.0055 GBP
}


def parse_amount(text: str) -> Decimal:
    """Turn what the user typed into an amount of money.

    Raises ValueError for anything that is not a positive, finite number
    (float() would have accepted "nan" and "inf").
    """
    try:
        value = Decimal(text.strip())
    except InvalidOperation:
        raise ValueError(f"Not a number: {text!r}") from None
    if not value.is_finite() or value <= 0:
        raise ValueError(f"Amount must be a positive number: {text!r}")
    return value


def amount_to_gbp(amount: str) -> Decimal:
    """Convert a stored amount such as "$12.50" to pounds.

    Raises ValueError for an unknown currency symbol or a bad number.
    """
    text = str(amount).strip()
    if not text or text[0] not in CONVERSION_RATES:
        raise ValueError(f"Unrecognised currency in amount: {amount!r}")
    return parse_amount(text[1:]) * CONVERSION_RATES[text[0]]


def totals_by_category(df: pd.DataFrame) -> "pd.Series[float]":
    """Total spend per category in pounds, converting every currency.

    The sum is done in Decimal; the result is floats only because that is
    what the chart needs.
    """
    return df.groupby("Category")["Amount"].apply(
        lambda amounts: float(sum((amount_to_gbp(a) for a in amounts), Decimal(0)))
    )
