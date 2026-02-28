from __future__ import annotations

from dataclasses import dataclass

from iq_signal_app.indicators.ma import ema, sma
from iq_signal_app.indicators.yuri import YuriState, compute_yuri_oscillator

from .probability import sigmoid


@dataclass
class SignalResult:
    action: str
    score: float
    prob_call: float
    prob_put: float


def evaluate_signal(closes: list[float], highs: list[float], lows: list[float]) -> SignalResult:
    if len(closes) < 10:
        return SignalResult("NONE", 0.0, 0.5, 0.5)

    ema3 = ema(closes, 3)
    ema5 = ema(closes, 5)
    ema7 = ema(closes, 7)
    sma21 = sma(closes, 21)
    yuri: YuriState = compute_yuri_oscillator(closes, highs, lows, 21)

    trend = 0.0
    if ema3 > ema5 > ema7:
        trend = 1.0
    elif ema3 < ema5 < ema7:
        trend = -1.0

    base = 1.0 if closes[-1] > sma21 else -1.0

    confirmation = 0.0
    recent = closes[-3:]
    if recent[0] < recent[1] < recent[2]:
        confirmation = 1.0
    elif recent[0] > recent[1] > recent[2]:
        confirmation = -1.0

    yuri_bias = 0.0
    if yuri.near_bottom and confirmation >= 0:
        yuri_bias = 1.0
    elif yuri.near_top and confirmation <= 0:
        yuri_bias = -1.0

    score = (0.35 * trend) + (0.2 * base) + (0.3 * yuri_bias) + (0.15 * confirmation)
    p_call = sigmoid(3.0 * score)
    p_put = 1 - p_call
    action = "CALL" if p_call > p_put else "PUT"

    return SignalResult(action=action, score=score, prob_call=p_call, prob_put=p_put)
