# Market Risk, VaR/Expected Shortfall, Stress & Limits

A reproducible **cross-asset market-risk platform** built around real public daily market series, factor-sensitivity P&L, Historical/Parametric/Monte Carlo VaR, Expected Shortfall, EWMA risk, VaR backtesting, stress testing, risk decomposition and automated limit monitoring.

The project is designed as a compact daily market-risk workflow: ingest risk factors, translate moves into position P&L, calculate and backtest risk, explain factor contributions, apply historical and hypothetical stresses, flag limit breaches, and generate a risk-manager report.

## What this repository demonstrates

| Layer | Implementation |
|---|---|
| Public data | fixed 2018–2025 FRED snapshot for S&P 500, EUR/USD, Brent oil, broad USD index and 10Y Treasury yield |
| Position mapping | equity/FX/commodity notional sensitivities plus USD DV01 for rates |
| VaR | rolling Historical VaR, normal Parametric VaR and EWMA-covariance Monte Carlo VaR |
| Expected Shortfall | empirical and simulation tail-loss averages |
| Volatility | RiskMetrics-style EWMA covariance with λ=0.94 |
| Backtesting | exception series, Kupiec unconditional coverage and Christoffersen independence/conditional coverage |
| Risk decomposition | marginal/component VaR from the factor P&L covariance matrix |
| Stress testing | observed worst-day/worst-5-day losses, named historical windows and transparent hypothetical shocks |
| Limits | VaR, ES, stress-loss and concentration thresholds with breach flags |
| Reporting | generated market-risk report, risk-factor contributions and backtest evidence |
| Reproducibility | unit tests + GitHub Actions + cached processed public data |

## Evidence standard

Market moves are empirical public observations. **Portfolio positions, notional sensitivities, DV01, internal limits and hypothetical stress shocks are illustrative.** No claim is made that this is a real institution's book, approved model or regulatory capital calculation.

Run locally:

```bash
python -m pip install -r requirements.txt
python -m pytest
python run_pipeline.py
```

The pipeline writes `outputs/metrics.json`, backtesting/limit/stress tables, a cached processed FRED snapshot under `data/processed/`, and a generated report under `reports/generated/`.

Quantitative headline results are added to this README only after the CI pipeline generates and verifies them.
