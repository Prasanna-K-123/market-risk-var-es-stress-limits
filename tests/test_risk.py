import numpy as np
import pandas as pd

from src.risk import historical_var_es, monte_carlo_var_es, parametric_var_es


def test_historical_es_not_below_var():
    pnl = pd.Series([100, -50, 20, -400, 40, -200, 10, -800, 30, 5] * 20)
    m = historical_var_es(pnl, 0.95)
    assert m["es"] >= m["var"] >= 0


def test_parametric_es_not_below_var():
    pnl = pd.Series(np.linspace(-100, 100, 500))
    m = parametric_var_es(pnl, 0.99)
    assert m["es"] >= m["var"]


def test_monte_carlo_reproducible():
    mean = np.array([0.0, 0.0])
    cov = np.array([[100.0, 20.0], [20.0, 50.0]])
    a = monte_carlo_var_es(mean, cov, 0.99, 5000, 7)
    b = monte_carlo_var_es(mean, cov, 0.99, 5000, 7)
    assert a == b
