import numpy as np
import pandas as pd

from src.pnl import factor_changes, factor_pnl
from src.volatility import ewma_covariance


def test_rate_dv01_sign_and_total_pnl():
    idx = pd.date_range("2020-01-01", periods=3)
    f = pd.DataFrame({"dow":[100,101,101],"eurusd":[1,1,1],"gbpusd":[1.25,1.25,1.25],"gold":[1500,1500,1500],"ust10y":[4.0,4.1,4.0]}, index=idx)
    p = factor_pnl(factor_changes(f))
    assert p.iloc[0]["ust10y"] < 0
    assert np.allclose(p["total_pnl"], p.drop(columns="total_pnl").sum(axis=1))


def test_ewma_covariance_symmetric_psdish():
    x = pd.DataFrame(np.arange(100, dtype=float).reshape(50,2))
    cov = ewma_covariance(x)
    assert np.allclose(cov, cov.T)
    assert np.linalg.eigvalsh(cov).min() > -1e-8
