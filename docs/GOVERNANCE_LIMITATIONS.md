# Governance and limitations

## Evidence boundary

- Market histories are empirical public observations from the MIT-licensed `pratheeknagaraj/financial-markets` research dataset; the upstream author describes them as best-effort and cross-referenced to primary sources, not as an official feed.
- Portfolio notionals, DV01, limits and hypothetical stress shocks are illustrative.
- Linear factor-sensitivity P&L is not full instrument revaluation and omits optionality, basis, liquidity, intraday and nonlinear Greeks unless explicitly modelled.
- VaR and Expected Shortfall estimates are analytical demonstrations, not approved regulatory or internal-capital models.

## Production controls required

A production implementation would use governed/vendor market data, instrument-level positions, valuation libraries, independent price verification, missing-data and stale-price controls, P&L attribution, model-change governance, stressed/current-period calibration rules, risk-factor eligibility, desk/entity aggregation, limit ownership/escalation, backtesting exceptions governance and independent validation.

The third-party dataset itself must also be independently reconciled before any production use.
