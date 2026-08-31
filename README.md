# Market Risk, VaR/Expected Shortfall, Stress & Limits

A reproducible **cross-asset market-risk platform** built around public daily market histories, factor-sensitivity P&L, Historical/Parametric/Monte Carlo VaR, Expected Shortfall, EWMA risk, VaR backtesting, stress testing, risk decomposition and automated limit monitoring.

The workflow mirrors a compact daily market-risk process: ingest equity/FX/commodity/rates factors, translate market moves into position P&L, calculate and backtest risk, explain factor contributions, apply historical and hypothetical stresses, flag limit breaches, and generate a risk-manager report.

## Verified CI evidence

The final pipeline is green in GitHub Actions and generated the following reproducible results from **1,341 aligned daily factor observations (2016-01-04 to 2021-04-30)**:

| Metric | Verified result |
|---|---:|
| Historical 99% VaR | $1.285m |
| Historical 99% Expected Shortfall | $2.226m |
| Parametric 99% VaR | $1.073m |
| Parametric 99% Expected Shortfall | $1.233m |
| EWMA Monte Carlo 99% VaR | $0.688m |
| EWMA Monte Carlo 99% Expected Shortfall | $0.794m |
| Rolling backtest exceptions | 17 / 1,090 (1.56%) |
| Kupiec unconditional-coverage p-value | 0.0861 |
| Christoffersen independence p-value | 0.0015 |
| Conditional-coverage p-value | 0.0015 |
| Worst observed 1-day P&L | -$4.451m (2020-03-16) |
| Worst observed rolling 5-day P&L | -$8.948m (ending 2020-03-18) |
| Worst hypothetical stress loss | $7.525m |

The backtest is deliberately **not presented as a clean pass**. At the 5% level, Kupiec does not reject unconditional coverage, but Christoffersen independence and combined conditional coverage are rejected, indicating clustered exceptions. That is a material model-risk finding and a limitation of this rolling Historical VaR specification rather than something hidden from the report.

The illustrative concentration limit also flags a breach: the largest notional is **43.75%** of the modeled notional book versus an illustrative **40%** threshold.

## What this repository demonstrates

| Layer | Implementation |
|---|---|
| Public data | fixed 2016-2021 histories for Dow Jones Industrial Average, EUR/USD, GBP/USD, gold and 10Y U.S. Treasury yield |
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

The fixed 2016-2021 interval is intentional: it provides more than 1,000 overlapping daily observations across all five selected factors for a 250-day rolling backtest. WTI was specifically not used in the final panel because negative futures prices in 2020 make simple percentage-return P&L inappropriate without a different return/valuation treatment; gold is used instead.

## Evidence standard

Market moves are empirical observations from that public dataset. **Portfolio positions, notional sensitivities, DV01, internal limits and hypothetical stress shocks are illustrative.** No claim is made that this is a real institution's book, approved model or regulatory capital calculation. The P&L model is linear factor sensitivity, not full instrument revaluation.

Run locally:

```bash
python -m pip install -r requirements.txt
python -m pytest
python run_pipeline.py
```

The pipeline writes `outputs/metrics.json`, backtesting/limit/stress tables, a cached processed market snapshot under `data/processed/`, and a generated report under `reports/generated/`.
