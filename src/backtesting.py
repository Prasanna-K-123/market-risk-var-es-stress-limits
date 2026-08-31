from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import chi2


def rolling_historical_var(pnl: pd.Series, window: int = 250, confidence: float = 0.99) -> pd.DataFrame:
    pnl = pd.Series(pnl, dtype=float).dropna()
    losses = -pnl
    var = losses.rolling(window).quantile(confidence).shift(1)
    out = pd.DataFrame({"pnl": pnl, "loss": losses, "var": var}).dropna()
    out["exception"] = out["loss"] > out["var"]
    return out


def kupiec_test(exceptions: pd.Series, confidence: float = 0.99) -> dict:
    exc = pd.Series(exceptions).astype(int).to_numpy()
    n = len(exc)
    x = int(exc.sum())
    p = 1.0 - confidence
    phat = x / n if n else np.nan
    eps = 1e-12
    ph = float(np.clip(phat, eps, 1 - eps))
    pp = float(np.clip(p, eps, 1 - eps))
    log_l0 = (n - x) * np.log(1 - pp) + x * np.log(pp)
    log_l1 = (n - x) * np.log(1 - ph) + x * np.log(ph)
    lr = float(-2.0 * (log_l0 - log_l1))
    return {"observations": n, "exceptions": x, "exception_rate": float(phat), "lr_uc": lr, "p_value": float(chi2.sf(lr, 1))}


def christoffersen_test(exceptions: pd.Series) -> dict:
    e = pd.Series(exceptions).astype(int).to_numpy()
    if len(e) < 2:
        raise ValueError("At least two backtest observations are required")
    n00 = n01 = n10 = n11 = 0
    for a, b in zip(e[:-1], e[1:]):
        if a == 0 and b == 0: n00 += 1
        elif a == 0 and b == 1: n01 += 1
        elif a == 1 and b == 0: n10 += 1
        else: n11 += 1
    eps = 1e-12
    pi0 = np.clip(n01 / max(n00 + n01, 1), eps, 1 - eps)
    pi1 = np.clip(n11 / max(n10 + n11, 1), eps, 1 - eps)
    pi = np.clip((n01 + n11) / max(n00 + n01 + n10 + n11, 1), eps, 1 - eps)
    log_ind = (n00 + n10) * np.log(1 - pi) + (n01 + n11) * np.log(pi)
    log_dep = n00*np.log(1-pi0) + n01*np.log(pi0) + n10*np.log(1-pi1) + n11*np.log(pi1)
    lr_ind = float(-2 * (log_ind - log_dep))
    return {"n00": n00, "n01": n01, "n10": n10, "n11": n11, "lr_ind": lr_ind, "p_value": float(chi2.sf(lr_ind, 1))}


def conditional_coverage(kupiec: dict, christoffersen: dict) -> dict:
    lr = float(kupiec["lr_uc"] + christoffersen["lr_ind"])
    return {"lr_cc": lr, "p_value": float(chi2.sf(lr, 2))}
