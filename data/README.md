# Data provenance

The pipeline retrieves public daily series through the Federal Reserve Bank of St. Louis FRED CSV interface for a fixed 2018-01-01 to 2025-12-31 study window.

Series: `SP500`, `DEXUSEU`, `DCOILBRENTEU`, `DTWEXBGS`, `DGS10`.

The first successful pipeline run caches the aligned processed snapshot in `data/processed/market_factors_2018_2025.csv`, and GitHub Actions commits that snapshot so later runs remain reproducible even if a public endpoint changes.

The market observations are empirical. Portfolio sensitivities and risk limits are not sourced from FRED and are explicitly illustrative.
