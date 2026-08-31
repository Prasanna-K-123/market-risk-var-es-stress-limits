from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.backtesting import christoffersen_test, conditional_coverage, kupiec_test, rolling_historical_var
from src.config import CONFIDENCE, EWMA_LAMBDA, MC_SIMULATIONS, RANDOM_STATE, ROLLING_WINDOW
from src.data import load_market_factors, validate_market_factors
from src.limits import limit_assessment
from src.pnl import FACTOR_COLUMNS, factor_changes, factor_pnl, position_summary
from src.reporting import build_market_risk_report, save_backtest_plot, write_json
from src.risk import component_var, historical_var_es, monte_carlo_var_es, parametric_var_es
from src.stress import empirical_tail_events, historical_window_stress, hypothetical_stress_table
from src.volatility import ewma_covariance

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "data" / "processed" / "market_factors_2019_2025.csv"
OUTPUTS = ROOT / "outputs"
REPORTS = ROOT / "reports" / "generated"


def main() -> None:
    factors = load_market_factors(CACHE)
    validate_market_factors(factors)
    changes = factor_changes(factors)
    pnl = factor_pnl(changes)
    factor_only = pnl[FACTOR_COLUMNS]

    hist = historical_var_es(pnl["total_pnl"], CONFIDENCE)
    param = parametric_var_es(pnl["total_pnl"], CONFIDENCE)
    ewma_cov = ewma_covariance(factor_only, EWMA_LAMBDA)
    mc = monte_carlo_var_es(factor_only.mean().to_numpy(), ewma_cov, CONFIDENCE, MC_SIMULATIONS, RANDOM_STATE)
    components = component_var(factor_only, CONFIDENCE)

    backtest = rolling_historical_var(pnl["total_pnl"], ROLLING_WINDOW, CONFIDENCE)
    kupiec = kupiec_test(backtest["exception"], CONFIDENCE)
    christ = christoffersen_test(backtest["exception"])
    cc = conditional_coverage(kupiec, christ)

    hypothetical = hypothetical_stress_table()
    historical = historical_window_stress(factors)
    tail = empirical_tail_events(pnl["total_pnl"])

    metrics = {
        "data": {
            "start": str(factors.index.min().date()),
            "end": str(factors.index.max().date()),
            "factor_rows": int(len(factors)),
            "pnl_rows": int(len(pnl)),
            "source": "Pratheek Nagaraj Financial Markets public GitHub dataset (MIT); OHLC histories described by source as best-effort cross-referenced to primary sources",
        },
        "methodology_flags": {
            "market_moves": "empirical public historical observations from third-party GitHub dataset; not an official feed",
            "positions_and_dv01": "illustrative",
            "internal_limits": "illustrative",
            "hypothetical_stresses": "illustrative",
            "valuation": "linear factor-sensitivity P&L; not full revaluation",
        },
        "historical": hist,
        "parametric": param,
        "monte_carlo": mc,
        "tail_events": tail,
        "backtesting": {"kupiec": kupiec, "christoffersen": christ, "conditional_coverage": cc},
        "worst_hypothetical_loss": float(hypothetical["loss"].max()),
    }
    limit_map = limit_assessment(metrics, metrics["worst_hypothetical_loss"])
    limit_table = pd.DataFrame([{"metric": k, **v} for k, v in limit_map.items()])
    metrics["limits"] = limit_map

    OUTPUTS.mkdir(exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    pnl.to_csv(OUTPUTS / "daily_factor_pnl.csv")
    backtest.to_csv(OUTPUTS / "var_backtest.csv")
    components.to_csv(OUTPUTS / "component_var.csv", index=False)
    hypothetical.to_csv(OUTPUTS / "hypothetical_stress.csv", index=False)
    historical.to_csv(OUTPUTS / "historical_stress.csv", index=False)
    position_summary().to_csv(OUTPUTS / "position_sensitivities.csv", index=False)
    limit_table.to_csv(OUTPUTS / "limit_monitoring.csv", index=False)
    write_json(metrics, OUTPUTS / "metrics.json")
    save_backtest_plot(backtest, REPORTS / "var_backtest.png")
    build_market_risk_report(metrics, components, hypothetical, historical, limit_table, REPORTS / "market_risk_report.md")
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
