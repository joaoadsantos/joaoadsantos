from __future__ import annotations

from dataclasses import dataclass

from .ma import sma


@dataclass
class YuriLevels:
    ext_top: float = 10
    ext_bot: float = -10
    sig_top: float = 9
    sig_bot: float = -9


@dataclass
class YuriState:
    value: float
    near_top: bool
    near_bottom: bool


def compute_yuri_oscillator(closes: list[float], highs: list[float], lows: list[float], length: int = 21) -> YuriState:
    if not closes:
        return YuriState(0.0, False, False)

    base = sma([(h + l) / 2 for h, l in zip(highs, lows)], min(length, len(closes)))
    rng = max((max(highs[-length:]) - min(lows[-length:])), 1e-6) if len(highs) >= length else max(max(highs) - min(lows), 1e-6)
    value = ((closes[-1] - base) / (rng * 0.2))

    levels = YuriLevels()
    return YuriState(
        value=value,
        near_top=value >= levels.sig_top,
        near_bottom=value <= levels.sig_bot,
    )
