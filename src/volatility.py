from __future__ import annotations

import numpy as np
import pandas as pd


def ewma_covariance(x: pd.DataFrame, lam: float = 0.94) -> np.ndarray:
    arr = np.asarray(x, dtype=float)
    if arr.ndim != 2 or len(arr) < 2:
        raise ValueError("EWMA covariance requires at least two observations")
    centered = arr - np.mean(arr, axis=0, keepdims=True)
    cov = np.cov(centered, rowvar=False, ddof=1)
    for row in centered:
        cov = lam * cov + (1.0 - lam) * np.outer(row, row)
    return cov
