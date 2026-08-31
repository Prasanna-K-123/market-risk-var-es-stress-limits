# Market data provenance

The market-risk engine downloads public daily OHLC histories from Pratheek Nagaraj's `financial-markets` GitHub repository under its MIT license. The upstream repository documents a standard Date/Open/High/Low/Close/Adj Close/Volume schema, daily updates, and best-effort consistency checks against primary sources.

Factors used in this project are Nasdaq Composite, EUR/USD, GBP/USD, Brent crude oil and the 10-year U.S. Treasury yield. The analysis uses a fixed 2019-01-01 through 2025-12-31 window and caches the aligned factor panel under `data/processed/` during execution.

Important evidence boundary: this is a public research dataset, not an exchange, central-bank, government or licensed vendor feed. The project makes no claim that the observations are suitable for production valuation, regulatory reporting or official P&L. A production implementation would source governed market data with vendor identifiers, corrections, holiday calendars, corporate-action controls, timestamps, lineage and reconciliation.

Upstream citation: Pratheek Nagaraj, *Financial Markets*, `github.com/pratheeknagaraj/financial-markets`.
