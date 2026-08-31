from __future__ import annotations

import pandas as pd

from src.config import NOTIONALS, UST10Y_DV01

HYPOTHETICAL = {
    "equity_rates_selloff": {"sp500": -0.15, "eurusd": -0.05, "brent": -0.12, "usd_broad": 0.05, "ust10y_bp": 75.0},
    "global_recession": {"sp500": -0.20, "eurusd": -0.03, "brent": -0.25, "usd_broad": 0.04, "ust10y_bp": -80.0},
    "inflation_energy_shock": {"sp500": -0.10, "eurusd": -0.04, "brent": 0.30, "usd_broad": 0.05, "ust10y_bp": 120.0},
    "usd_depreciation": {"sp500": 0.03, "eurusd": 0.10, "brent": 0.08, "usd_broad": -0.08, "ust10y_bp": 20.0},
}

HISTORICAL_WINDOWS = {
    "covid_selloff": ("2020-02-19", "2020-03-23"),
    "2022_rates_energy": ("2022-01-03", "2022-06-16"),
    "2018_q4_riskoff": ("2018-10-01", "2018-12-24"),
}


def hypothetical_stress_table() -> pd.DataFrame:
    rows = []
    for name, s in HYPOTHETICAL.items():
        pnl = sum(NOTIONALS[k] * s[k] for k in NOTIONALS) - UST10Y_DV01 * s["ust10y_bp"]
        rows.append({"scenario": name, **s, "portfolio_pnl": float(pnl), "loss": float(-pnl)})
    return pd.DataFrame(rows)


def historical_window_stress(factors: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, (start, end) in HISTORICAL_WINDOWS.items():
        sample = factors.loc[start:end]
        if len(sample) < 2:
            continue
        first, last = sample.iloc[0], sample.iloc[-1]
        moves = {k: float(last[k] / first[k] - 1.0) for k in NOTIONALS}
        rate_bp = float((last["ust10y"] - first["ust10y"]) * 100.0)
        pnl = sum(NOTIONALS[k] * moves[k] for k in NOTIONALS) - UST10Y_DV01 * rate_bp
        rows.append({"scenario": name, "start": str(sample.index[0].date()), "end": str(sample.index[-1].date()), **moves, "ust10y_bp": rate_bp, "portfolio_pnl": float(pnl), "loss": float(-pnl)})
    return pd.DataFrame(rows)


def empirical_tail_events(total_pnl: pd.Series) -> dict:
    pnl = pd.Series(total_pnl).dropna()
    rolling5 = pnl.rolling(5).sum()
    return {
        "worst_1d_date": str(pnl.idxmin().date()),
        "worst_1d_pnl": float(pnl.min()),
        "worst_5d_end_date": str(rolling5.idxmin().date()),
        "worst_5d_pnl": float(rolling5.min()),
    }
