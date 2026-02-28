from __future__ import annotations

import time


class Cooldown:
    def __init__(self, seconds: int) -> None:
        self.seconds = seconds
        self._last_trigger = 0.0

    def ready(self) -> bool:
        return time.time() - self._last_trigger >= self.seconds

    def trigger(self) -> None:
        self._last_trigger = time.time()
