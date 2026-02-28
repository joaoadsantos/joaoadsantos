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
    """Thread-safe screen capturer.

    On Windows, MSS keeps thread-local handles. Reusing one MSS instance across
    threads can raise: AttributeError '_thread._local' has no attribute 'srcdc'.
    To avoid that, each call creates its own MSS context in the current thread.
    """

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

        # fallback assuming principal monitor 1920x1080
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

        # fallback using PIL if mss unavailable
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
