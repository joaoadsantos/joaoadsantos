from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np

try:
    import mss
except ImportError:  # optional dependency
    mss = None


@dataclass
class ROI:
    x: int
    y: int
    width: int
    height: int


class ScreenCapturer:
    def __init__(self) -> None:
        self._sct: Optional["mss.mss"] = mss.mss() if mss else None

    def capture(self, roi: ROI) -> np.ndarray:
        if self._sct:
            mon = {"top": roi.y, "left": roi.x, "width": roi.width, "height": roi.height}
            frame = np.array(self._sct.grab(mon))
            return frame[:, :, :3]

        # fallback using PIL if mss unavailable
        from PIL import ImageGrab

        img = ImageGrab.grab(bbox=(roi.x, roi.y, roi.x + roi.width, roi.y + roi.height))
        return np.array(img)
