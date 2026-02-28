from __future__ import annotations

import threading
import time
from datetime import datetime

from tkinter import BOTH, LEFT, RIGHT, Button, Entry, Frame, Label, StringVar, Tk

from iq_signal_app.alerts.popup import show_signal_popup
from iq_signal_app.alerts.sound import beep
from iq_signal_app.capture.screen import ROI, ScreenCapturer
from iq_signal_app.config import AppConfig
from iq_signal_app.engine.cooldown import Cooldown
from iq_signal_app.engine.scoring import evaluate_signal
from iq_signal_app.logs.repository import EventRepository
from iq_signal_app.vision.candles import extract_candles
from iq_signal_app.vision.preprocess import preprocess_frame


class MainWindow:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.root = Tk()
        self.root.title("IQ Signal App (MVP)")
        self.root.geometry("620x420")

        self.status_var = StringVar(value="Parado")
        self.signal_var = StringVar(value="Sem sinal")

        self._running = False
        self._worker: threading.Thread | None = None

        self.capturer = ScreenCapturer()
        self.cooldown = Cooldown(config.cooldown_seconds)
        self.repo = EventRepository(config.csv_path)

        self.roi_x = Entry(self.root, width=6)
        self.roi_y = Entry(self.root, width=6)
        self.roi_w = Entry(self.root, width=6)
        self.roi_h = Entry(self.root, width=6)
        self.threshold_entry = Entry(self.root, width=6)

        self._build_ui()

    def _build_ui(self) -> None:
        top = Frame(self.root)
        top.pack(fill=BOTH, padx=10, pady=10)

        Label(top, text="ROI x").pack(side=LEFT)
        self.roi_x.pack(side=LEFT)
        Label(top, text="y").pack(side=LEFT)
        self.roi_y.pack(side=LEFT)
        Label(top, text="w").pack(side=LEFT)
        self.roi_w.pack(side=LEFT)
        Label(top, text="h").pack(side=LEFT)
        self.roi_h.pack(side=LEFT)

        for entry, value in [
            (self.roi_x, self.config.roi[0]),
            (self.roi_y, self.config.roi[1]),
            (self.roi_w, self.config.roi[2]),
            (self.roi_h, self.config.roi[3]),
        ]:
            entry.insert(0, str(value))

        bottom = Frame(self.root)
        bottom.pack(fill=BOTH, padx=10, pady=10)
        Label(bottom, text="Threshold").pack(side=LEFT)
        self.threshold_entry.pack(side=LEFT)
        self.threshold_entry.insert(0, str(self.config.threshold))

        controls = Frame(self.root)
        controls.pack(fill=BOTH, padx=10, pady=10)
        Button(controls, text="Iniciar", command=self.start).pack(side=LEFT)
        Button(controls, text="Parar", command=self.stop).pack(side=LEFT)
        Button(controls, text="Sair", command=self.close).pack(side=RIGHT)

        Label(self.root, text="Status:").pack(anchor="w", padx=10)
        Label(self.root, textvariable=self.status_var).pack(anchor="w", padx=10)
        Label(self.root, text="Último sinal:").pack(anchor="w", padx=10)
        Label(self.root, textvariable=self.signal_var, fg="blue").pack(anchor="w", padx=10)

    def get_roi(self) -> ROI:
        return ROI(
            x=int(self.roi_x.get()),
            y=int(self.roi_y.get()),
            width=int(self.roi_w.get()),
            height=int(self.roi_h.get()),
        )

    def get_threshold(self) -> float:
        try:
            return float(self.threshold_entry.get())
        except ValueError:
            return self.config.threshold

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self.status_var.set("Rodando")
        self._worker = threading.Thread(target=self._loop, daemon=True)
        self._worker.start()

    def stop(self) -> None:
        self._running = False
        self.status_var.set("Parado")

    def close(self) -> None:
        self.stop()
        self.root.destroy()

    def _loop(self) -> None:
        while self._running:
            roi = self.get_roi()
            frame = self.capturer.capture(roi)
            gray = preprocess_frame(frame)
            candles = extract_candles(gray, self.config.candle_count)

            closes = [c.close for c in candles]
            highs = [c.high for c in candles]
            lows = [c.low for c in candles]

            result = evaluate_signal(closes, highs, lows)
            best_prob = max(result.prob_call, result.prob_put)
            text = f"{result.action} | prob={best_prob:.2%} | score={result.score:.3f}"
            self.root.after(0, self.signal_var.set, text)

            threshold = self.get_threshold()
            triggered = False
            if best_prob >= threshold and self.cooldown.ready():
                triggered = True
                self.cooldown.trigger()
                self.root.after(0, self._alert_and_minimize, result.action, best_prob)

            self.repo.append(
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "action": result.action,
                    "score": f"{result.score:.5f}",
                    "prob_call": f"{result.prob_call:.5f}",
                    "prob_put": f"{result.prob_put:.5f}",
                    "triggered": str(triggered),
                }
            )
            time.sleep(self.config.capture_interval_ms / 1000)

    def _alert_and_minimize(self, action: str, probability: float) -> None:
        beep()
        ok = show_signal_popup(self.root, action, probability)
        if ok:
            self.root.iconify()

    def run(self) -> None:
        self.root.mainloop()


def run_app(config: AppConfig) -> None:
    MainWindow(config).run()
