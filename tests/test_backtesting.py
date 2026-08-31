import pandas as pd

from src.backtesting import christoffersen_test, conditional_coverage, kupiec_test


def test_backtesting_statistics_are_valid():
    exc = pd.Series(([False] * 98 + [True] + [False]) * 5)
    k = kupiec_test(exc, 0.99)
    c = christoffersen_test(exc)
    cc = conditional_coverage(k, c)
    assert k["observations"] == 500
    assert 0 <= k["p_value"] <= 1
    assert 0 <= c["p_value"] <= 1
    assert 0 <= cc["p_value"] <= 1
