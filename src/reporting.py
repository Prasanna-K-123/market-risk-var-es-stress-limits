from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate


def write_json(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def save_backtest_plot(backtest: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(backtest.index, backtest["loss"], label="Daily loss")
    ax.plot(backtest.index, backtest["var"], label="99% rolling historical VaR")
    exc = backtest[backtest["exception"]]
    ax.scatter(exc.index, exc["loss"], marker="x", label="Exceptions")
    ax.set_title("Rolling VaR backtest")
    ax.set_ylabel("USD")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def build_market_risk_report(metrics: dict, components: pd.DataFrame, hypo: pd.DataFrame, historical: pd.DataFrame, limits: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    h, p, m = metrics["historical"], metrics["parametric"], metrics["monte_carlo"]
    bt = metrics["backtesting"]
    tail = metrics["tail_events"]
    text = f"""# Daily market-risk assessment

## Executive risk metrics

- Historical 99% VaR: **{h['var']:,.0f} USD**; ES: **{h['es']:,.0f} USD**
- Parametric 99% VaR: **{p['var']:,.0f} USD**; ES: **{p['es']:,.0f} USD**
- EWMA Monte Carlo 99% VaR: **{m['var']:,.0f} USD**; ES: **{m['es']:,.0f} USD**
- Worst observed 1-day portfolio P&L: **{tail['worst_1d_pnl']:,.0f} USD** on {tail['worst_1d_date']}
- Worst observed rolling 5-day P&L: **{tail['worst_5d_pnl']:,.0f} USD** ending {tail['worst_5d_end_date']}

## VaR backtesting

- Observations: **{bt['kupiec']['observations']}**
- Exceptions: **{bt['kupiec']['exceptions']}** ({bt['kupiec']['exception_rate']:.2%})
- Kupiec p-value: **{bt['kupiec']['p_value']:.4f}**
- Christoffersen independence p-value: **{bt['christoffersen']['p_value']:.4f}**
- Conditional-coverage p-value: **{bt['conditional_coverage']['p_value']:.4f}**

## Component VaR

{tabulate(components, headers='keys', tablefmt='github', showindex=False, floatfmt='.4g')}

## Hypothetical stress scenarios

{tabulate(hypo, headers='keys', tablefmt='github', showindex=False, floatfmt='.4g')}

## Historical-window stresses

{tabulate(historical, headers='keys', tablefmt='github', showindex=False, floatfmt='.4g')}

## Limit monitoring

{tabulate(limits, headers='keys', tablefmt='github', showindex=False)}

## Model-risk judgement

Market data are public FRED observations. The positions, DV01, limits and hypothetical stress severities are illustrative. Historical VaR is backward-looking; normal parametric VaR can understate fat tails; EWMA responds to recent volatility but is not a full volatility model; Monte Carlo inherits the covariance/distribution assumptions; and the portfolio uses linear first-order sensitivities rather than full revaluation.

A production implementation would require validated position feeds, instrument-level valuation, nonlinear Greeks, basis risks, liquidity horizons, approved market-data sources, model-change governance, independent validation, P&L attribution and reconciliation to official risk reporting.
"""
    path.write_text(text, encoding="utf-8")
