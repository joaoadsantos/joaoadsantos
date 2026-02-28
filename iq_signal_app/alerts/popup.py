from __future__ import annotations

import tkinter as tk
from tkinter import messagebox


def show_signal_popup(parent: tk.Tk, action: str) -> bool:
    msg = f"Sinal detectado: {action}"
    return messagebox.showinfo("Sinal detectado", msg, parent=parent) == "ok"
