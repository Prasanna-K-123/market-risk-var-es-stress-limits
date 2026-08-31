# Market data provenance

The market-risk engine downloads public daily OHLC histories from Pratheek Nagaraj's `financial-markets` GitHub repository under its MIT license. The upstream repository documents a standard Date/Open/High/Low/Close/Adj Close/Volume schema, daily updates, and best-effort consistency checks against primary sources.

Final factors are **Dow Jones Industrial Average, EUR/USD, GBP/USD, gold and the 10-year U.S. Treasury yield**. The analysis uses a fixed **2016-01-04 through 2021-04-30** overlapping window and caches the aligned factor panel under `data/processed/` during execution. This produces 1,341 aligned observations.

The factor/window choice is part of the data-quality control. An earlier candidate equity history did not provide enough observations in the target period, and WTI was rejected from the final percentage-return panel because negative futures prices in 2020 invalidate the simple percentage-return transformation without a different valuation treatment.

Important evidence boundary: this is a public research dataset, not an exchange, central-bank, government or licensed vendor feed. The project makes no claim that the observations are suitable for production valuation, regulatory reporting or official P&L. A production implementation would source governed market data with vendor identifiers, corrections, holiday calendars, corporate-action controls, timestamps, lineage and reconciliation.

Upstream citation: Pratheek Nagaraj, *Financial Markets*, `github.com/pratheeknagaraj/financial-markets`.
