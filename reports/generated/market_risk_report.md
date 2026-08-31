# Daily market-risk assessment

## Executive risk metrics

- Historical 99% VaR: **1,285,499 USD**; ES: **2,225,681 USD**
- Parametric 99% VaR: **1,072,706 USD**; ES: **1,233,263 USD**
- EWMA Monte Carlo 99% VaR: **688,392 USD**; ES: **794,242 USD**
- Worst observed 1-day portfolio P&L: **-4,450,591 USD** on 2020-03-16
- Worst observed rolling 5-day P&L: **-8,947,947 USD** ending 2020-03-18

## VaR backtesting

- Observations: **1090**
- Exceptions: **17** (1.56%)
- Kupiec p-value: **0.0861**
- Christoffersen independence p-value: **0.0015**
- Conditional-coverage p-value: **0.0015**

## Component VaR

| factor   |   component_var |   share_of_parametric_var |
|----------|-----------------|---------------------------|
| dow      |       8.661e+05 |                  0.7858   |
| eurusd   |       7.145e+04 |                  0.06482  |
| gbpusd   |       3.9e+04   |                  0.03538  |
| gold     |       1.299e+05 |                  0.1178   |
| ust10y   |   -4226         |                 -0.003834 |

## Hypothetical stress scenarios

| scenario             |   dow |   eurusd |   gbpusd |   gold |   ust10y_bp |   portfolio_pnl |       loss |
|----------------------|-------|----------|----------|--------|-------------|-----------------|------------|
| equity_rates_selloff | -0.15 |    -0.05 |    -0.06 |   0.08 |          75 |      -7.525e+06 |  7.525e+06 |
| global_recession     | -0.2  |    -0.03 |    -0.04 |   0.12 |         -80 |      -4.2e+06   |  4.2e+06   |
| inflation_shock      | -0.1  |    -0.04 |    -0.05 |   0.18 |         120 |      -5.1e+06   |  5.1e+06   |
| usd_depreciation     |  0.03 |     0.1  |     0.08 |   0.1  |          20 |       4.85e+06  | -4.85e+06  |

## Historical-window stresses

| scenario           | start      | end        |      dow |    eurusd |   gbpusd |     gold |   ust10y_bp |   portfolio_pnl |       loss |
|--------------------|------------|------------|----------|-----------|----------|----------|-------------|-----------------|------------|
| brexit_repricing   | 2016-06-23 | 2016-06-27 | -0.04835 | -0.02578  | -0.09047 |  0.0486  |       -27.9 |      -1.686e+06 |  1.686e+06 |
| volmageddon_2018   | 2018-02-01 | 2018-02-09 | -0.07621 | -0.01272  | -0.01873 | -0.02321 |         5.6 |      -3.597e+06 |  3.597e+06 |
| covid_selloff      | 2020-02-19 | 2020-03-23 | -0.3665  | -0.009356 | -0.1061  | -0.02519 |       -80.6 |      -1.244e+07 |  1.244e+07 |
| pandemic_reflation | 2020-11-02 | 2021-03-31 |  0.2249  |  0.007043 |  0.06343 | -0.09342 |        89.7 |       5.004e+06 | -5.004e+06 |

## Limit monitoring

| metric                    |            value |    limit | breach   |
|---------------------------|------------------|----------|----------|
| historical_var            |      1.2855e+06  | 2e+06    | False    |
| historical_es             |      2.22568e+06 | 3e+06    | False    |
| monte_carlo_var           | 688392           | 2.25e+06 | False    |
| worst_hypothetical_stress |      7.525e+06   | 1e+07    | False    |
| largest_notional_share    |      0.4375      | 0.4      | True     |

## Model-risk judgement

Market data are public FRED observations. The positions, DV01, limits and hypothetical stress severities are illustrative. Historical VaR is backward-looking; normal parametric VaR can understate fat tails; EWMA responds to recent volatility but is not a full volatility model; Monte Carlo inherits the covariance/distribution assumptions; and the portfolio uses linear first-order sensitivities rather than full revaluation.

A production implementation would require validated position feeds, instrument-level valuation, nonlinear Greeks, basis risks, liquidity horizons, approved market-data sources, model-change governance, independent validation, P&L attribution and reconciliation to official risk reporting.
