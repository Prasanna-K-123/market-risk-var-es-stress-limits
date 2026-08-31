# Governance and limitations

## Evidence boundary

- Market histories are empirical public observations from the MIT-licensed `pratheeknagaraj/financial-markets` research dataset; the upstream author describes them as best-effort and cross-referenced to primary sources, not as an official feed.
- Portfolio notionals, DV01, limits and hypothetical stress shocks are illustrative.
- Linear factor-sensitivity P&L is not full instrument revaluation and omits optionality, basis, liquidity, intraday and nonlinear Greeks unless explicitly modelled.
- VaR and Expected Shortfall estimates are analytical demonstrations, not approved regulatory or internal-capital models.

## Validation findings

The final 250-day rolling 99% Historical VaR backtest has 17 exceptions across 1,090 forecasts. Kupiec unconditional coverage is not rejected at 5% (p=0.0861), but Christoffersen independence and combined conditional coverage are rejected (both approximately p=0.0015). Exceptions therefore cluster more than an independent exceedance process would imply. A production response would investigate volatility responsiveness, regime shifts, P&L mapping, data issues and alternative/current-period VaR specifications rather than label the model as simply "passing".

The illustrative largest-notional concentration threshold is also breached at 43.75% versus 40%. Limit ownership and escalation are not modeled as institutional processes here.

## Production controls required

A production implementation would use governed/vendor market data, instrument-level positions, valuation libraries, independent price verification, missing-data and stale-price controls, P&L attribution, model-change governance, stressed/current-period calibration rules, risk-factor eligibility, desk/entity aggregation, limit ownership/escalation, backtesting-exception governance and independent validation.

The third-party dataset itself must also be independently reconciled before any production use.
