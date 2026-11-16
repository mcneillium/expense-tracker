from decimal import Decimal

import pandas as pd
import pytest

from money import amount_to_gbp, parse_amount, totals_by_category


def test_amount_to_gbp_converts_each_currency_exactly():
    assert amount_to_gbp("£10.00") == Decimal("10.00")
    assert amount_to_gbp("$10.00") == Decimal("7.50")
    assert amount_to_gbp("€10.00") == Decimal("8.50")
    assert amount_to_gbp("¥1000") == Decimal("5.50")


def test_pennies_add_up_exactly():
    # In floating point 0.10 + 0.20 is 0.30000000000000004.
    assert amount_to_gbp("£0.10") + amount_to_gbp("£0.20") == Decimal("0.30")


def test_unknown_currency_is_rejected():
    with pytest.raises(ValueError):
        amount_to_gbp("CHF10")


@pytest.mark.parametrize("text", ["", "abc", "nan", "inf", "-5", "0"])
def test_parse_amount_rejects_what_is_not_a_positive_number(text):
    # float() accepted "nan" and "inf", which were then saved as "£nan".
    with pytest.raises(ValueError):
        parse_amount(text)


def test_parse_amount_accepts_ordinary_amounts():
    assert parse_amount(" 12.5 ") == Decimal("12.5")


def test_category_totals_convert_before_summing():
    # Before the fix the chart summed 10 + 10 = 20 "pounds" here.
    df = pd.DataFrame(
        {"Category": ["Food", "Food", "Transport"], "Amount": ["£10.00", "$10.00", "£2.00"]}
    )
    totals = totals_by_category(df)
    assert totals["Food"] == pytest.approx(17.5)
    assert totals["Transport"] == pytest.approx(2.0)
