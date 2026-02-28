from __future__ import annotations

import threading
import time
from datetime import datetime

from tkinter import BOTH, LEFT, RIGHT, Button, Entry, Frame, Label, StringVar, Tk

from iq_signal_app.alerts.popup import show_signal_popup
from iq_signal_app.alerts.sound import beep
from iq_signal_app.capture.screen import ScreenCapturer
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
        self.root.title("IQ Signal App (Auto Monitor)")
        self.root.geometry("560x320")

        self.status_var = StringVar(value="Parado")
        self.signal_var = StringVar(value="Sem sinal")
        self.monitor_var = StringVar(value="-")

        self._running = False
        self._worker: threading.Thread | None = None

        self.capturer = ScreenCapturer()
        self.cooldown = Cooldown(config.cooldown_seconds)
        self.repo = EventRepository(config.csv_path)

        self.threshold_entry = Entry(self.root, width=8)
        self._build_ui()

    def _build_ui(self) -> None:
        info = Frame(self.root)
        info.pack(fill=BOTH, padx=10, pady=10)

        Label(info, text=f"Monitor do gráfico (automático): {self.config.chart_monitor_index}").pack(anchor="w")
        Label(info, text="Região capturada:").pack(anchor="w")
        Label(info, textvariable=self.monitor_var, fg="gray").pack(anchor="w")

        threshold = Frame(self.root)
        threshold.pack(fill=BOTH, padx=10, pady=10)
        Label(threshold, text="Threshold").pack(side=LEFT)
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
            try:
                monitor = self.capturer.get_monitor_region(self.config.chart_monitor_index)
                monitor_text = f"x={monitor.x}, y={monitor.y}, w={monitor.width}, h={monitor.height}"
                self.root.after(0, self.monitor_var.set, monitor_text)

                frame = self.capturer.capture_monitor(self.config.chart_monitor_index)
                gray = preprocess_frame(frame)
                candles = extract_candles(gray, self.config.candle_count)

                closes = [c.close for c in candles]
                highs = [c.high for c in candles]
                lows = [c.low for c in candles]

                result = evaluate_signal(closes, highs, lows)
                best_prob = max(result.prob_call, result.prob_put)
                self.root.after(0, self.signal_var.set, result.action)

                threshold = self.get_threshold()
                triggered = False
                if best_prob >= threshold and result.action in {"CALL", "PUT"} and self.cooldown.ready():
                    triggered = True
                    self.cooldown.trigger()
                    self.root.after(0, self._alert_and_minimize, result.action)

                self.repo.append(
                    {
                        "timestamp": datetime.utcnow().isoformat(),
                        "action": result.action,
                        "score": f"{result.score:.5f}",
                        "prob_call": f"{result.prob_call:.5f}",
                        "prob_put": f"{result.prob_put:.5f}",
                        "triggered": str(triggered),
                        "monitor_index": str(self.config.chart_monitor_index),
                    }
                )
            except Exception as exc:
                self.root.after(0, self.status_var.set, f"Erro: {exc}")

            time.sleep(self.config.capture_interval_ms / 1000)

    def _alert_and_minimize(self, action: str) -> None:
        beep()
        ok = show_signal_popup(self.root, action)
        if ok:
            self.root.iconify()

    def run(self) -> None:
        self.root.mainloop()


def run_app(config: AppConfig) -> None:
    MainWindow(config).run()
