from __future__ import annotations

from io import StringIO
from pathlib import Path
import time

import pandas as pd
import requests

from src.config import END_DATE, FRED_SERIES, START_DATE

FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"


def _download_series(series_id: str, start: str = START_DATE, end: str = END_DATE) -> pd.Series:
    params = {"id": series_id, "cosd": start, "coed": end}
    headers = {"User-Agent": "market-risk-research-project/1.0"}
    last_error = None
    for attempt in range(3):
        try:
            response = requests.get(FRED_URL, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            df = pd.read_csv(StringIO(response.text))
            if df.shape[1] < 2:
                raise ValueError(f"Unexpected FRED response for {series_id}")
            date_col, value_col = df.columns[:2]
            dates = pd.to_datetime(df[date_col], errors="coerce")
            values = pd.to_numeric(df[value_col], errors="coerce")
            out = pd.Series(values.to_numpy(), index=dates, name=series_id).dropna()
            if out.empty:
                raise ValueError(f"No numeric observations returned for {series_id}")
            return out.sort_index()
        except Exception as exc:
            last_error = exc
            time.sleep(1.0 + attempt)
    raise RuntimeError(f"Failed to download FRED series {series_id}: {last_error}")


def load_market_factors(cache_path: Path | None = None, force_download: bool = False) -> pd.DataFrame:
    if cache_path is not None and cache_path.exists() and not force_download:
        cached = pd.read_csv(cache_path, parse_dates=["date"]).set_index("date")
        return cached.sort_index()

    raw = {name: _download_series(series_id) for name, series_id in FRED_SERIES.items()}
    anchor = raw["sp500"].index
    factors = pd.DataFrame(index=anchor)
    for name, series in raw.items():
        factors[name] = series.reindex(anchor).ffill(limit=5)
    factors = factors.dropna().sort_index()
    factors.index.name = "date"

    if cache_path is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        factors.reset_index().to_csv(cache_path, index=False)
    return factors


def validate_market_factors(df: pd.DataFrame) -> None:
    required = set(FRED_SERIES)
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing market factors: {sorted(missing)}")
    if len(df) < 1000:
        raise ValueError("Insufficient daily history for robust backtesting")
    if not df.index.is_monotonic_increasing or df.index.has_duplicates:
        raise ValueError("Dates must be unique and increasing")
    if df[list(required)].isna().any().any():
        raise ValueError("Market factor history contains missing values after alignment")
