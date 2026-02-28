from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class AppConfig:
    capture_interval_ms: int = 200
    candle_count: int = 60
    threshold: float = 0.75
    cooldown_seconds: int = 45
    roi: tuple[int, int, int, int] = (100, 100, 900, 500)
    csv_path: str = "iq_signal_app/data/events.csv"

    @classmethod
    def load(cls, path: str | Path = "config.yaml") -> "AppConfig":
        cfg_path = Path(path)
        if not cfg_path.exists():
            return cls()
        data: dict[str, Any] = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
        roi_raw = data.get("roi", {})
        roi = (
            int(roi_raw.get("x", 100)),
            int(roi_raw.get("y", 100)),
            int(roi_raw.get("width", 900)),
            int(roi_raw.get("height", 500)),
        )
        return cls(
            capture_interval_ms=int(data.get("capture_interval_ms", 200)),
            candle_count=int(data.get("candle_count", 60)),
            threshold=float(data.get("threshold", 0.75)),
            cooldown_seconds=int(data.get("cooldown_seconds", 45)),
            roi=roi,
            csv_path=str(data.get("csv_path", "iq_signal_app/data/events.csv")),
        )
