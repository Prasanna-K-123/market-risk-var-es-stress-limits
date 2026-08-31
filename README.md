# Market Risk, VaR/Expected Shortfall, Stress & Limits

A reproducible **cross-asset market-risk platform** built around public daily market histories, factor-sensitivity P&L, Historical/Parametric/Monte Carlo VaR, Expected Shortfall, EWMA risk, VaR backtesting, stress testing, risk decomposition and automated limit monitoring.

The workflow mirrors a compact daily market-risk process: ingest equity/FX/commodity/rates factors, translate market moves into position P&L, calculate and backtest risk, explain factor contributions, apply historical and hypothetical stresses, flag limit breaches, and generate a risk-manager report.

## What this repository demonstrates

| Layer | Implementation |
|---|---|
| Public data | fixed 2019–2025 histories for Nasdaq Composite, EUR/USD, GBP/USD, Brent crude and 10Y Treasury yield |
| Position mapping | illustrative equity/FX/commodity notionals plus USD DV01 for rates |
| VaR | Historical VaR, normal Parametric VaR and EWMA-covariance Monte Carlo VaR |
| Expected Shortfall | empirical and simulation tail-loss averages |
| Volatility | RiskMetrics-style EWMA covariance with λ=0.94 |
| Backtesting | 250-day rolling VaR, exception series, Kupiec coverage and Christoffersen independence/conditional coverage |
| Risk decomposition | marginal/component VaR from the factor P&L covariance matrix |
| Stress testing | observed worst-day/worst-5-day losses, named historical windows and transparent hypothetical shocks |
| Limits | VaR, ES, stress-loss and concentration thresholds with breach flags |
| Reporting | generated market-risk report, factor contributions and backtest evidence |
| Reproducibility | unit tests + GitHub Actions + cached processed public market snapshot |

## Data provenance

The raw histories are downloaded from the MIT-licensed `pratheeknagaraj/financial-markets` GitHub repository. Its documentation describes dynamically updated public OHLC histories and explicitly characterizes accuracy as best-effort/cross-referenced to primary sources. This project therefore treats the observations as a **public research dataset, not an official market-data feed**. See `data/README.md` and `docs/GOVERNANCE_LIMITATIONS.md`.

## Evidence standard

Market moves are empirical observations from that public dataset. **Portfolio positions, notional sensitivities, DV01, internal limits and hypothetical stress shocks are illustrative.** No claim is made that this is a real institution's book, approved model or regulatory capital calculation. The P&L model is linear factor sensitivity, not full instrument revaluation.

Run locally:

```bash
python -m pip install -r requirements.txt
python -m pytest
python run_pipeline.py
```

The pipeline writes `outputs/metrics.json`, backtesting/limit/stress tables, a cached processed market snapshot under `data/processed/`, and a generated report under `reports/generated/`.

Quantitative headline results are added only after the CI pipeline generates and verifies them.
