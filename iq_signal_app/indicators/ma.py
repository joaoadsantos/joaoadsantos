from __future__ import annotations


def sma(values: list[float], period: int) -> float:
    if not values:
        return 0.0
    if len(values) < period:
        return sum(values) / len(values)
    window = values[-period:]
    return sum(window) / period


def ema(values: list[float], period: int) -> float:
    if not values:
        return 0.0
    alpha = 2 / (period + 1)
    value = values[0]
    for v in values[1:]:
        value = alpha * v + (1 - alpha) * value
    return value
