from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import NOTIONALS, UST10Y_DV01

FACTOR_COLUMNS = ["nasdaq", "eurusd", "gbpusd", "brent", "ust10y"]


def factor_changes(factors: pd.DataFrame) -> pd.DataFrame:
    changes = pd.DataFrame(index=factors.index)
    for factor in ["nasdaq", "eurusd", "gbpusd", "brent"]:
        changes[factor] = factors[factor].pct_change(fill_method=None)
    changes["ust10y"] = factors["ust10y"].diff() * 100.0  # percentage points -> bp
    return changes.dropna()


def factor_pnl(changes: pd.DataFrame) -> pd.DataFrame:
    pnl = pd.DataFrame(index=changes.index)
    for factor, notional in NOTIONALS.items():
        pnl[factor] = changes[factor] * notional
    pnl["ust10y"] = -changes["ust10y"] * UST10Y_DV01
    pnl["total_pnl"] = pnl[FACTOR_COLUMNS].sum(axis=1)
    return pnl


def position_summary() -> pd.DataFrame:
    rows = [{"factor": k, "sensitivity_type": "notional", "sensitivity": v} for k, v in NOTIONALS.items()]
    rows.append({"factor": "ust10y", "sensitivity_type": "DV01_USD_per_bp", "sensitivity": UST10Y_DV01})
    return pd.DataFrame(rows)
