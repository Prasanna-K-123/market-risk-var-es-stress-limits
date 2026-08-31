from __future__ import annotations

START_DATE = "2018-01-01"
END_DATE = "2025-12-31"
CONFIDENCE = 0.99
ROLLING_WINDOW = 250
EWMA_LAMBDA = 0.94
MC_SIMULATIONS = 100_000
RANDOM_STATE = 20260831

FRED_SERIES = {
    "sp500": "SP500",
    "eurusd": "DEXUSEU",
    "brent": "DCOILBRENTEU",
    "usd_broad": "DTWEXBGS",
    "ust10y": "DGS10",
}

# Illustrative position sensitivities, expressed in USD P&L terms.
NOTIONALS = {
    "sp500": 35_000_000.0,
    "eurusd": 20_000_000.0,
    "brent": 15_000_000.0,
    "usd_broad": 10_000_000.0,
}
UST10Y_DV01 = 25_000.0  # USD loss for a +1 bp parallel 10Y yield move.
PORTFOLIO_GROSS = sum(abs(x) for x in NOTIONALS.values()) + 25_000_000.0

LIMITS = {
    "historical_var": 2_000_000.0,
    "historical_es": 3_000_000.0,
    "monte_carlo_var": 2_250_000.0,
    "worst_hypothetical_stress": 10_000_000.0,
    "largest_notional_share": 0.40,
}
