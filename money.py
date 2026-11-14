"""Currency helpers shared by the GUI and the tests.

The rates are fixed examples, not live exchange rates.
"""

CONVERSION_RATES = {
    "£": 1.0,
    "$": 0.75,    # example: 1 USD = 0.75 GBP
    "€": 0.85,    # example: 1 EUR = 0.85 GBP
    "¥": 0.0055,  # example: 1 JPY = 0.0055 GBP
}


def amount_to_gbp(amount):
    """Convert a stored amount such as "$12.50" to pounds.

    Raises ValueError for an unknown currency symbol or a bad number.
    """
    text = str(amount).strip()
    if not text or text[0] not in CONVERSION_RATES:
        raise ValueError(f"Unrecognised currency in amount: {amount!r}")
    return float(text[1:]) * CONVERSION_RATES[text[0]]


def totals_by_category(df):
    """Total spend per category in pounds, converting every currency."""
    return df.groupby("Category")["Amount"].apply(lambda s: sum(amount_to_gbp(a) for a in s))
