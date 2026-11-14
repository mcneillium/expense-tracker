import pandas as pd
import pytest

from money import amount_to_gbp, totals_by_category


def test_amount_to_gbp_converts_each_currency():
    assert amount_to_gbp("£10.00") == pytest.approx(10.0)
    assert amount_to_gbp("$10.00") == pytest.approx(7.5)
    assert amount_to_gbp("€10.00") == pytest.approx(8.5)
    assert amount_to_gbp("¥1000") == pytest.approx(5.5)


def test_unknown_currency_is_rejected():
    with pytest.raises(ValueError):
        amount_to_gbp("CHF10")


def test_category_totals_convert_before_summing():
    # Before the fix the chart summed 10 + 10 = 20 "pounds" here.
    df = pd.DataFrame({"Category": ["Food", "Food", "Transport"],
                       "Amount": ["£10.00", "$10.00", "£2.00"]})
    totals = totals_by_category(df)
    assert totals["Food"] == pytest.approx(17.5)
    assert totals["Transport"] == pytest.approx(2.0)
