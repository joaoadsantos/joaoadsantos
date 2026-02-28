from iq_signal_app.config import AppConfig
from iq_signal_app.ui.main_window import run_app


if __name__ == "__main__":
    cfg = AppConfig.load("config.yaml")
    run_app(cfg)
