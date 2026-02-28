from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class AppConfig:
    capture_interval_ms: int = 200
    candle_count: int = 60
    threshold: float = 0.78
    cooldown_seconds: int = 20
    chart_monitor_index: int = 1
    center_crop_ratio: float = 0.70
    confirm_ticks: int = 2
    min_score_alert: int = 25
    min_frame_delta: float = 0.50
    csv_path: str = "iq_signal_app/data/events.csv"

    @classmethod
    def load(cls, path: str | Path = "config.yaml") -> "AppConfig":
        cfg_path = Path(path)
        if not cfg_path.exists():
            return cls()

        data: dict[str, Any] = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
        return cls(
            capture_interval_ms=int(data.get("capture_interval_ms", 200)),
            candle_count=int(data.get("candle_count", 60)),
            threshold=float(data.get("threshold", 0.78)),
            cooldown_seconds=int(data.get("cooldown_seconds", 20)),
            chart_monitor_index=int(data.get("chart_monitor_index", 1)),
            center_crop_ratio=float(data.get("center_crop_ratio", 0.70)),
            confirm_ticks=int(data.get("confirm_ticks", 2)),
            min_score_alert=int(data.get("min_score_alert", 25)),
            min_frame_delta=float(data.get("min_frame_delta", 0.50)),
            csv_path=str(data.get("csv_path", "iq_signal_app/data/events.csv")),
        )
