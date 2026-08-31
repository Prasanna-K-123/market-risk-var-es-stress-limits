from __future__ import annotations

from src.config import LIMITS, NOTIONALS


def limit_assessment(metrics: dict, worst_hypothetical_loss: float) -> dict:
    gross_notional = sum(abs(v) for v in NOTIONALS.values())
    largest_share = max(abs(v) for v in NOTIONALS.values()) / gross_notional
    values = {
        "historical_var": float(metrics["historical"]["var"]),
        "historical_es": float(metrics["historical"]["es"]),
        "monte_carlo_var": float(metrics["monte_carlo"]["var"]),
        "worst_hypothetical_stress": float(worst_hypothetical_loss),
        "largest_notional_share": float(largest_share),
    }
    return {
        key: {"value": value, "limit": float(LIMITS[key]), "breach": bool(value > LIMITS[key])}
        for key, value in values.items()
    }
