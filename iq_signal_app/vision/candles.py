from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Candle:
    open: float
    high: float
    low: float
    close: float


def extract_candles(gray: np.ndarray, candle_count: int = 60) -> list[Candle]:
    h, w = gray.shape
    if w < candle_count:
        candle_count = max(10, w // 2)

    step = max(1, w // candle_count)
    candles: list[Candle] = []
    last_close = 0.0

    for i in range(candle_count):
        col_start = i * step
        col_end = min(w, col_start + step)
        if col_start >= w:
            break
        segment = gray[:, col_start:col_end]
        profile = segment.mean(axis=1)

        top = int(np.argmin(profile))
        bottom = int(np.argmax(profile))
        high = max(0.0, 1.0 - min(top, bottom) / h)
        low = max(0.0, 1.0 - max(top, bottom) / h)
        close = (high + low) / 2
        open_ = last_close if candles else close
        candles.append(Candle(open=open_, high=high, low=low, close=close))
        last_close = close

    return candles
