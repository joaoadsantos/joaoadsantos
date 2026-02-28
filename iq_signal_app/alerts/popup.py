from __future__ import annotations

import tkinter as tk
from tkinter import messagebox


def show_signal_popup(parent: tk.Tk, action: str, probability: float) -> bool:
    msg = f"Ação sugerida: {action}\nProbabilidade: {probability:.2%}"
    return messagebox.showinfo("Sinal detectado", msg, parent=parent) == "ok"
