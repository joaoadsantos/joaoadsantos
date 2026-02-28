from __future__ import annotations

import platform


def beep() -> None:
    if platform.system().lower().startswith("win"):
        import winsound

        winsound.Beep(1200, 500)
        return
    print("\a", end="", flush=True)
