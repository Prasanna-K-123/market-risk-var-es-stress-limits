from __future__ import annotations

START_DATE = "2019-01-01"
END_DATE = "2025-12-31"
CONFIDENCE = 0.99
ROLLING_WINDOW = 250
EWMA_LAMBDA = 0.94
MC_SIMULATIONS = 100_000
RANDOM_STATE = 20260831

# CI-stable public daily market-history snapshots. The upstream repository is
# MIT-licensed and describes its data as best-effort, cross-referenced to
# primary sources. These are research inputs, not an official market-data feed.
DATA_URLS = {
    "nasdaq": "https://raw.githubusercontent.com/pratheeknagaraj/financial-markets/main/data/us/stock/nasdaq/nasdaq.csv",
    "eurusd": "https://raw.githubusercontent.com/pratheeknagaraj/financial-markets/main/data/global/currency/fiat/eurusd/eurusd.csv",
    "gbpusd": "https://raw.githubusercontent.com/pratheeknagaraj/financial-markets/main/data/global/currency/fiat/gbpusd/gbpusd.csv",
    "brent": "https://raw.githubusercontent.com/pratheeknagaraj/financial-markets/main/data/us/commodity/energy/brent_crude_oil/brent_crude_oil.csv",
    "ust10y": "https://raw.githubusercontent.com/pratheeknagaraj/financial-markets/main/data/us/treasury/tyield_10/tyield_10.csv",
}

# Illustrative position sensitivities, expressed in USD P&L terms.
NOTIONALS = {
    "nasdaq": 35_000_000.0,
    "eurusd": 20_000_000.0,
    "gbpusd": 10_000_000.0,
    "brent": 15_000_000.0,
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
