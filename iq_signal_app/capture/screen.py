from __future__ import annotations

from dataclasses import dataclass

import numpy as np

try:
    import mss
except ImportError:  # optional dependency
    mss = None


@dataclass
class MonitorRegion:
    x: int
    y: int
    width: int
    height: int


class ScreenCapturer:
    """Thread-safe screen capturer."""

    def get_monitor_region(self, monitor_index: int) -> MonitorRegion:
        if mss:
            with mss.mss() as sct:
                monitors = sct.monitors
                if monitor_index < 1 or monitor_index >= len(monitors):
                    monitor_index = 1
                monitor = monitors[monitor_index]
                return MonitorRegion(
                    x=int(monitor["left"]),
                    y=int(monitor["top"]),
                    width=int(monitor["width"]),
                    height=int(monitor["height"]),
                )

        return MonitorRegion(x=0, y=0, width=1920, height=1080)

    def capture_monitor(self, monitor_index: int) -> np.ndarray:
        monitor = self.get_monitor_region(monitor_index)
        if mss:
            with mss.mss() as sct:
                mon = {
                    "top": monitor.y,
                    "left": monitor.x,
                    "width": monitor.width,
                    "height": monitor.height,
                }
                frame = np.array(sct.grab(mon))
                return frame[:, :, :3]

        from PIL import ImageGrab

        img = ImageGrab.grab(
            bbox=(
                monitor.x,
                monitor.y,
                monitor.x + monitor.width,
                monitor.y + monitor.height,
            )
        )
        return np.array(img)

    def crop_center(self, frame: np.ndarray, ratio: float) -> np.ndarray:
        ratio = min(1.0, max(0.2, ratio))
        h, w = frame.shape[:2]
        crop_w = int(w * ratio)
        crop_h = int(h * ratio)
        x0 = (w - crop_w) // 2
        y0 = (h - crop_h) // 2
        return frame[y0 : y0 + crop_h, x0 : x0 + crop_w]
