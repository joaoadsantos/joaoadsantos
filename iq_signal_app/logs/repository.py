from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


class EventRepository:
    def __init__(self, file_path: str) -> None:
        self.path = Path(file_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            with self.path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "timestamp",
                        "action",
                        "score",
                        "prob_call",
                        "prob_put",
                        "triggered",
                    ],
                )
                writer.writeheader()

    def append(self, event: dict[str, Any]) -> None:
        with self.path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(event.keys()))
            writer.writerow(event)
