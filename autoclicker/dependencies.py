import tkinter as tk
import threading
import time
import random
import json
import os
import sys

# ─── Dependency check ────────────────────────────────────────────────────────
missing = []
try:
    import customtkinter as ctk
except ImportError:
    missing.append("customtkinter")
try:
    import pyautogui

    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0
except ImportError:
    missing.append("pyautogui")
try:
    from pynput import mouse as pmouse, keyboard as pkeyboard
    from pynput.keyboard import Key, KeyCode
except ImportError:
    missing.append("pynput")

if missing:
    root = tk.Tk()
    root.title("AutoClicker Pro — Missing Dependencies")
    root.geometry("500x210")
    root.configure(bg="#0d0d0d")
    tk.Label(
        root,
        text="⚠  Missing packages detected",
        fg="#ff4757",
        bg="#0d0d0d",
        font=("Courier", 15, "bold"),
    ).pack(pady=(28, 6))
    cmd = "pip install " + " ".join(missing)
    tk.Label(
        root,
        text="Run this command in your terminal:",
        fg="#888",
        bg="#0d0d0d",
        font=("Courier", 10),
    ).pack()
    fr = tk.Frame(root, bg="#1a1a1a", padx=14, pady=10)
    fr.pack(pady=8, padx=30, fill="x")
    tk.Label(fr, text=cmd, fg="#00d4aa", bg="#1a1a1a", font=("Courier", 11)).pack()
    tk.Button(
        root,
        text="Copy command",
        bg="#2a2a2a",
        fg="white",
        relief="flat",
        padx=12,
        pady=4,
        command=lambda: (root.clipboard_clear(), root.clipboard_append(cmd)),
    ).pack()
    root.mainloop()
    sys.exit(1)

# ─── Constants ────────────────────────────────────────────────────────────────
