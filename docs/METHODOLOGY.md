# Market-risk methodology

## Risk-factor data

The empirical risk-factor history uses a fixed **2016-01-04 through 2021-04-30** window of public daily OHLC histories from the MIT-licensed `pratheeknagaraj/financial-markets` GitHub repository: Dow Jones Industrial Average, EUR/USD, GBP/USD, gold and the 10-year U.S. Treasury yield. The source repository describes the data as dynamically updated, publicly available and best-effort cross-referenced to primary sources; it is not treated here as an official market-data feed. Adjusted close (or close if unavailable) is used. The Dow trading calendar anchors alignment and other factors are forward-filled only across short trading/publication gaps.

The fixed window was chosen only after validating common-history coverage. It yields 1,341 aligned factor observations, enough for a 250-day rolling VaR backtest. WTI was excluded from the final factor panel because the 2020 negative futures-price episode makes percentage returns unsuitable without an alternative P&L treatment; substituting gold avoids silently applying an invalid transformation.

## P&L mapping

Equity, FX and commodity factors use simple percentage changes times illustrative USD notionals. The 10-year Treasury factor uses daily yield changes in basis points times an illustrative USD DV01. This produces daily factor P&L contributions and a total portfolio P&L series. The approximation is linear and does not perform instrument-level repricing.

## VaR and Expected Shortfall

Historical VaR/ES use the empirical P&L distribution. Parametric VaR/ES use a normal approximation to total P&L. Monte Carlo VaR/ES use 100,000 multivariate-normal draws from the latest EWMA factor-P&L covariance matrix with λ=0.94. These methods are intentionally compared rather than treated as interchangeable truth.

Verified 99% results are Historical VaR $1.285m / ES $2.226m, Parametric VaR $1.073m / ES $1.233m, and EWMA Monte Carlo VaR $0.688m / ES $0.794m.

## Backtesting

A 250-observation rolling Historical VaR is shifted by one day before comparison with realized losses to avoid look-ahead. The final backtest contains 1,090 forecast observations and 17 exceptions (1.56%). Kupiec unconditional coverage has p=0.0861, so it is not rejected at a 5% level. Christoffersen independence has p=0.0015 and combined conditional coverage p=0.0015, so exception independence and combined coverage are rejected. The observed clustering is reported as model-risk evidence, not suppressed.

## Decomposition, stress and limits

Normal-theory component VaR attributes portfolio risk to factor P&L contributions. Historical-window stresses replay observed factor moves over Brexit repricing, the February 2018 volatility shock, the COVID selloff and pandemic reflation. Hypothetical shocks, positions and internal limits are transparent illustrative assumptions. The worst modeled hypothetical loss is $7.525m. The illustrative largest-notional concentration threshold is breached at 43.75% versus a 40% limit, while the VaR, ES, Monte Carlo VaR and hypothetical-stress thresholds are not breached.
