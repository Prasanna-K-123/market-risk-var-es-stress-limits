from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm


def historical_var_es(pnl: pd.Series, confidence: float = 0.99) -> dict:
    losses = -pd.Series(pnl, dtype=float).dropna().to_numpy()
    var = float(np.quantile(losses, confidence))
    tail = losses[losses >= var]
    es = float(tail.mean()) if len(tail) else var
    return {"var": var, "es": es}


def parametric_var_es(pnl: pd.Series, confidence: float = 0.99) -> dict:
    values = pd.Series(pnl, dtype=float).dropna().to_numpy()
    mu = float(np.mean(values))
    sigma = float(np.std(values, ddof=1))
    z = float(norm.ppf(confidence))
    var = -mu + z * sigma
    es = -mu + sigma * float(norm.pdf(z) / (1.0 - confidence))
    return {"var": float(var), "es": float(es), "mean_pnl": mu, "sigma_pnl": sigma}


def monte_carlo_var_es(mean_vector, covariance, confidence=0.99, n=100_000, seed=20260831) -> dict:
    rng = np.random.default_rng(seed)
    sims = rng.multivariate_normal(np.asarray(mean_vector, float), np.asarray(covariance, float), size=n)
    total = sims.sum(axis=1)
    losses = -total
    var = float(np.quantile(losses, confidence))
    es = float(losses[losses >= var].mean())
    return {"var": var, "es": es, "simulations": int(n)}


def component_var(factor_pnl: pd.DataFrame, confidence: float = 0.99) -> pd.DataFrame:
    x = np.asarray(factor_pnl, float)
    cov = np.cov(x, rowvar=False, ddof=1)
    ones = np.ones(x.shape[1])
    sigma = float(np.sqrt(ones @ cov @ ones))
    z = float(norm.ppf(confidence))
    marginal_sigma = (cov @ ones) / sigma
    component = z * marginal_sigma
    total = float(component.sum())
    return pd.DataFrame({
        "factor": factor_pnl.columns,
        "component_var": component,
        "share_of_parametric_var": component / total if total else np.nan,
    })
