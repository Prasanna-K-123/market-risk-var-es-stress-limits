from __future__ import annotations

from io import StringIO
from pathlib import Path
import time

import pandas as pd
import requests

from src.config import DATA_URLS, END_DATE, START_DATE


def _download_series(url: str, name: str, start: str = START_DATE, end: str = END_DATE) -> pd.Series:
    """Download one OHLC history and return adjusted-close observations."""
    headers = {"User-Agent": "market-risk-research-project/2.0"}
    last_error = None
    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=(10, 45))
            response.raise_for_status()
            df = pd.read_csv(StringIO(response.text))
            required = {"Date", "Close"}
            if not required.issubset(df.columns):
                raise ValueError(f"Unexpected market-data schema for {name}: {list(df.columns)}")
            value_col = "Adj Close" if "Adj Close" in df.columns else "Close"
            dates = pd.to_datetime(df["Date"], errors="coerce")
            values = pd.to_numeric(df[value_col], errors="coerce")
            out = pd.Series(values.to_numpy(), index=dates, name=name).dropna()
            out = out[~out.index.duplicated(keep="last")].sort_index()
            out = out.loc[pd.Timestamp(start):pd.Timestamp(end)]
            if len(out) < 1000:
                raise ValueError(f"Insufficient observations for {name}: {len(out)}")
            return out
        except Exception as exc:
            last_error = exc
            time.sleep(1.0 + 2.0 * attempt)
    raise RuntimeError(f"Failed to download market series {name}: {last_error}")


def load_market_factors(cache_path: Path | None = None, force_download: bool = False) -> pd.DataFrame:
    if cache_path is not None and cache_path.exists() and not force_download:
        cached = pd.read_csv(cache_path, parse_dates=["date"]).set_index("date")
        return cached.sort_index()

    raw = {name: _download_series(url, name) for name, url in DATA_URLS.items()}
    anchor = raw["nasdaq"].index
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
    required = set(DATA_URLS)
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing market factors: {sorted(missing)}")
    if len(df) < 1000:
        raise ValueError("Insufficient daily history for robust backtesting")
    if not df.index.is_monotonic_increasing or df.index.has_duplicates:
        raise ValueError("Dates must be unique and increasing")
    if df[list(required)].isna().any().any():
        raise ValueError("Market factor history contains missing values after alignment")
    if (df[list(required)] <= 0).any().any():
        raise ValueError("Market factor levels must be positive")
