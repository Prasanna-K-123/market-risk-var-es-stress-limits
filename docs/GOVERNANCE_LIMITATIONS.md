# Governance, assumptions and limitations

This is a market-risk methodology demonstration, not a bank risk report or regulatory model.

Empirical: public FRED market-factor observations in the fixed source window.

Illustrative: positions, notionals, DV01, risk limits, hypothetical stress shocks and management thresholds.

Key limitations: linear first-order P&L mapping; no option Greeks or full revaluation; no intraday risk; no liquidity horizon; no basis/spread risk beyond selected factors; normal Parametric/Monte Carlo assumptions do not reproduce all fat-tail dynamics; EWMA is a covariance response model, not a complete volatility process; Historical VaR depends on the observed sample; FRED is a public economic-data source rather than an institution's approved trading-book feed.

Production remediation would require governed position/market-data feeds, instrument-level pricing, nonlinear sensitivities, approved data hierarchies, liquidity horizons, P&L attribution, desk/entity aggregation, model validation, exception governance, reconciliation and risk-committee escalation procedures.
