# Market-risk methodology

## Risk-factor data

The empirical risk-factor history uses a fixed 2019–2025 window of public daily OHLC histories from the MIT-licensed `pratheeknagaraj/financial-markets` GitHub repository: Nasdaq Composite, EUR/USD, GBP/USD, Brent crude oil and the 10-year Treasury yield. The source repository describes the data as dynamically updated, publicly available and best-effort cross-referenced to primary sources; it is not treated here as an official market-data feed. Adjusted close (or close if unavailable) is used. The Nasdaq calendar anchors alignment and other factors are forward-filled only across short trading/publication gaps.

## P&L mapping

Equity, FX and commodity factors use simple percentage changes times illustrative USD notionals. The 10-year Treasury factor uses daily yield changes in basis points times an illustrative USD DV01. This produces daily factor P&L contributions and a total portfolio P&L series.

## VaR and Expected Shortfall

Historical VaR/ES use the empirical P&L distribution. Parametric VaR/ES use a normal approximation to total P&L. Monte Carlo VaR/ES use 100,000 multivariate-normal draws from the latest EWMA factor-P&L covariance matrix. These methods are intentionally compared rather than treated as interchangeable truth.

## Backtesting

A 250-observation rolling Historical VaR is shifted by one day before comparison with realized losses to avoid look-ahead. The report includes exception count/rate, Kupiec unconditional-coverage, Christoffersen independence and combined conditional-coverage tests.

## Decomposition, stress and limits

Normal-theory component VaR attributes portfolio risk to factor P&L contributions. Historical-window stresses replay observed factor moves over named episodes. Hypothetical shocks, positions and internal limits are transparent illustrative assumptions. Limit monitoring flags metrics that exceed those assumptions.
