from __future__ import annotations

START_DATE = "2016-01-01"
END_DATE = "2021-04-30"
CONFIDENCE = 0.99
ROLLING_WINDOW = 250
EWMA_LAMBDA = 0.94
MC_SIMULATIONS = 100_000
RANDOM_STATE = 20260831

# CI-stable public daily market-history snapshots. The upstream repository is
# MIT-licensed and describes its data as best-effort, cross-referenced to
# primary sources. These are research inputs, not an official market-data feed.
# The fixed 2016-2021 window is intentional: all selected factors have enough
# overlapping observations to support a 250-day rolling VaR backtest.
DATA_URLS = {
    "dow": "https://raw.githubusercontent.com/pratheeknagaraj/financial-markets/main/data/us/stock/dow/dow.csv",
    "eurusd": "https://raw.githubusercontent.com/pratheeknagaraj/financial-markets/main/data/global/currency/fiat/eurusd/eurusd.csv",
    "gbpusd": "https://raw.githubusercontent.com/pratheeknagaraj/financial-markets/main/data/global/currency/fiat/gbpusd/gbpusd.csv",
    "gold": "https://raw.githubusercontent.com/pratheeknagaraj/financial-markets/main/data/us/commodity/metals/gold/gold.csv",
    "ust10y": "https://raw.githubusercontent.com/pratheeknagaraj/financial-markets/main/data/us/treasury/tyield_10/tyield_10.csv",
}

# Illustrative position sensitivities, expressed in USD P&L terms.
NOTIONALS = {
    "dow": 35_000_000.0,
    "eurusd": 20_000_000.0,
    "gbpusd": 10_000_000.0,
    "gold": 15_000_000.0,
}
UST10Y_DV01 = 25_000.0  # USD loss for a +1 bp 10Y yield move.
PORTFOLIO_GROSS = sum(abs(x) for x in NOTIONALS.values()) + 25_000_000.0

LIMITS = {
    "historical_var": 2_000_000.0,
    "historical_es": 3_000_000.0,
    "monte_carlo_var": 2_250_000.0,
    "worst_hypothetical_stress": 10_000_000.0,
    "largest_notional_share": 0.40,
}
