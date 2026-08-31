# Market-risk methodology

## Risk-factor data

The empirical risk-factor history is downloaded from the Federal Reserve Bank of St. Louis FRED public CSV interface for a fixed 2018–2025 window: S&P 500 (`SP500`), USD/EUR exchange rate (`DEXUSEU`), Brent crude oil (`DCOILBRENTEU`), broad trade-weighted U.S. dollar index (`DTWEXBGS`) and 10-year Treasury yield (`DGS10`). The S&P 500 calendar anchors the alignment; other factors are forward-filled only across short publication/holiday gaps.

## P&L mapping

Equity, FX, commodity and dollar-index factors use simple percentage changes times illustrative USD notionals. The 10-year Treasury factor uses daily yield changes in basis points times an illustrative USD DV01. This produces daily factor P&L contributions and a total portfolio P&L series.

## VaR and Expected Shortfall

Historical VaR/ES use the empirical P&L distribution. Parametric VaR/ES use a normal approximation to total P&L. Monte Carlo VaR/ES use 100,000 multivariate-normal draws from the latest EWMA factor-P&L covariance matrix. These methods are intentionally compared rather than treated as interchangeable truth.

## Backtesting

A 250-observation rolling Historical VaR is shifted by one day before comparison with realized losses to avoid look-ahead. The report includes exception count/rate, Kupiec unconditional-coverage, Christoffersen independence and combined conditional-coverage tests.

## Decomposition, stress and limits

Normal-theory component VaR attributes portfolio risk to factor P&L contributions. Historical-window stresses replay observed factor moves over named market episodes. Hypothetical shocks, positions and internal limits are transparent illustrative assumptions. Limit monitoring flags risk metrics that exceed those assumptions.
