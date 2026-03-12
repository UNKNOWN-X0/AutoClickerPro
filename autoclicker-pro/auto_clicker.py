"""
AutoClicker Pro - Cross-platform Auto Clicker
Requirements: pip install pynput pyautogui customtkinter
"""

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
    tk.Label(root, text="⚠  Missing packages detected", fg="#ff4757", bg="#0d0d0d",
             font=("Courier", 15, "bold")).pack(pady=(28, 6))
    cmd = "pip install " + " ".join(missing)
    tk.Label(root, text="Run this command in your terminal:", fg="#888", bg="#0d0d0d",
             font=("Courier", 10)).pack()
    fr = tk.Frame(root, bg="#1a1a1a", padx=14, pady=10)
    fr.pack(pady=8, padx=30, fill="x")
    tk.Label(fr, text=cmd, fg="#00d4aa", bg="#1a1a1a",
             font=("Courier", 11)).pack()
    tk.Button(root, text="Copy command", bg="#2a2a2a", fg="white",
              relief="flat", padx=12, pady=4,
              command=lambda: (root.clipboard_clear(), root.clipboard_append(cmd))).pack()
    root.mainloop()
    sys.exit(1)

# ─── Constants ────────────────────────────────────────────────────────────────
APP_NAME    = "AutoClicker Pro"
VERSION     = "1.0.0"
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".autoclicker_config.json")

DARK   = "#0d0d0d"
PANEL  = "#141414"
CARD   = "#1a1a1a"
BORDER = "#2a2a2a"
ACCENT = "#00d4aa"
RED    = "#ff4757"
YELLOW = "#ffd32a"
PURPLE = "#8b5cf6"
TEXT   = "#e8e8e8"
MUTED  = "#666666"

# ─── App State ────────────────────────────────────────────────────────────────
class AppState:
    def __init__(self):
        self.running       = False
        self.recording     = False
        self.click_count   = 0
        self.macro_events  = []
        self.multipoints   = []

state = AppState()
click_thread            = None
macro_thread            = None
hotkey_listener         = None
macro_mouse_listener    = None
macro_keyboard_listener = None
macro_start_time        = None
pressed_keys            = set()

# ─── Core click logic ─────────────────────────────────────────────────────────
def do_click(btn, action, x=None, y=None):
    bmap = {"Left": "left", "Right": "right", "Middle": "middle"}
    b = bmap.get(btn, "left")
    if x is not None and y is not None:
        pyautogui.moveTo(x, y, duration=0.04)
    if action == "Double":
        pyautogui.doubleClick(button=b)
    else:
        pyautogui.click(button=b)

def click_loop(cfg):
    mode     = cfg["mode"]
    repeat_n = cfg["repeat_n"]
    btn      = cfg["button"]
    action   = cfg["action"]
    interval = cfg["interval"]
    rnd_min  = cfg["rand_min"]
    rnd_max  = cfg["rand_max"]
    use_mp   = cfg["use_multipoint"]
    points   = cfg["points"]
    rand_pos = cfg["rand_pos"]
    mp_idx   = 0
    count    = 0

    while state.running:
        if mode == "Fixed" and count >= repeat_n:
            break
        x, y = None, None
        if use_mp and points:
            x, y = points[mp_idx % len(points)]
            mp_idx += 1
            if rand_pos:
                x += random.randint(-5, 5)
                y += random.randint(-5, 5)
        try:
            do_click(btn, action, x, y)
        except Exception:
            break
        state.click_count += 1
        count += 1
        _update_counter()
        delay = interval
        if rnd_min < rnd_max:
            delay += random.randint(rnd_min, rnd_max) / 1000.0
        time.sleep(delay)

    state.running = False
    app.after(0, _refresh_status)

def macro_replay(events, repeat_n, infinite):
    loops = 0
    while state.running:
        if not infinite and loops >= repeat_n:
            break
        prev_t = None
        for ev in events:
            if not state.running:
                break
            t = ev["time"]
            if prev_t is not None:
                time.sleep(max(0, t - prev_t))
            prev_t = t
            try:
                if ev["type"] == "click":
                    do_click(ev["button"], "Single", ev["x"], ev["y"])
                    state.click_count += 1
                    _update_counter()
                elif ev["type"] == "key":
                    pyautogui.press(ev["key"])
            except Exception:
                pass
        loops += 1
    state.running = False
    app.after(0, _refresh_status)

# ─── Hotkeys ─────────────────────────────────────────────────────────────────
def _key_str(key):
    try:
        if hasattr(key, 'char') and key.char:
            return key.char.upper()
        return str(key).replace("Key.", "").upper()
    except Exception:
        return str(key)

def on_press(key):
    pressed_keys.add(key)
    combo = "+".join(sorted(_key_str(k) for k in pressed_keys))
    if combo == start_hotkey_var.get():
        app.after(0, toggle_clicking)
    elif combo == stop_hotkey_var.get():
        app.after(0, stop_clicking)

def on_release(key):
    pressed_keys.discard(key)

# ─── Actions ─────────────────────────────────────────────────────────────────
def toggle_clicking():
    if state.running:
        stop_clicking()
    else:
        start_clicking()

def start_clicking():
    global click_thread, macro_thread
    if state.running:
        return
    state.running = True

    tab = notebook.get()

    if tab == "Macro":
        if not state.macro_events:
            import tkinter.messagebox as mb
            mb.showwarning("No Macro", "Record a macro first.")
            state.running = False
            return
        is_inf = mode_var.get() == "Infinite"
        n = int(repeat_var.get()) if repeat_var.get().isdigit() else 10
        macro_thread = threading.Thread(
            target=macro_replay, args=(state.macro_events, n, is_inf), daemon=True)
        macro_thread.start()
    else:
        h   = int(hours_var.get())  if hours_var.get().isdigit()  else 0
        m   = int(mins_var.get())   if mins_var.get().isdigit()   else 0
        s   = int(secs_var.get())   if secs_var.get().isdigit()   else 0
        ms  = int(ms_var.get())     if ms_var.get().isdigit()     else 100
        iv  = h * 3600 + m * 60 + s + ms / 1000.0
        if iv <= 0:
            iv = 0.05
        cfg = {
            "mode":          mode_var.get(),
            "repeat_n":      int(repeat_var.get()) if repeat_var.get().isdigit() else 10,
            "button":        btn_var.get(),
            "action":        action_var.get(),
            "interval":      iv,
            "rand_min":      int(rnd_min_var.get()) if rnd_min_var.get().isdigit() else 0,
            "rand_max":      int(rnd_max_var.get()) if rnd_max_var.get().isdigit() else 0,
            "use_multipoint": mp_enable_var.get() and len(state.multipoints) > 0,
            "points":        list(state.multipoints),
            "rand_pos":      rand_pos_var.get(),
        }
        click_thread = threading.Thread(target=click_loop, args=(cfg,), daemon=True)
        click_thread.start()

    _refresh_status()

def stop_clicking():
    state.running = False
    _refresh_status()

def reset_counter():
    state.click_count = 0
    counter_var.set("0")

def _update_counter():
    app.after(0, lambda: counter_var.set(f"{state.click_count:,}"))

def _refresh_status():
    if state.running:
        status_label.configure(text="● ACTIVE", text_color=ACCENT)
        start_btn.configure(text="⏹  STOP", fg_color=RED, hover_color="#cc3344")
    else:
        status_label.configure(text="○  IDLE", text_color=MUTED)
        start_btn.configure(text="▶  START", fg_color=ACCENT, hover_color="#00b894")

# ─── Macro ────────────────────────────────────────────────────────────────────
def toggle_recording():
    if state.recording:
        _stop_recording()
    else:
        _start_recording()

def _start_recording():
    global macro_mouse_listener, macro_keyboard_listener, macro_start_time
    state.recording = True
    state.macro_events = []
    macro_start_time = time.time()
    rec_btn.configure(text="⏹ Stop Recording", fg_color=RED)
    macro_status_var.set("● Recording…")

    def on_mc(x, y, button, pressed):
        if not state.recording:
            return False
        if pressed:
            state.macro_events.append({
                "type": "click", "time": time.time() - macro_start_time,
                "x": x, "y": y,
                "button": ("Right" if "right" in str(button).lower()
                           else "Middle" if "middle" in str(button).lower()
                           else "Left")
            })
            app.after(0, lambda: macro_count_var.set(f"{len(state.macro_events)} events"))

    def on_kp(key):
        if not state.recording:
            return False
        try:
            k = key.char if hasattr(key, 'char') and key.char else str(key).replace("Key.", "")
            state.macro_events.append({"type": "key", "time": time.time() - macro_start_time, "key": k})
            app.after(0, lambda: macro_count_var.set(f"{len(state.macro_events)} events"))
        except Exception:
            pass

    macro_mouse_listener    = pmouse.Listener(on_click=on_mc)
    macro_keyboard_listener = pkeyboard.Listener(on_press=on_kp)
    macro_mouse_listener.start()
    macro_keyboard_listener.start()

def _stop_recording():
    global macro_mouse_listener, macro_keyboard_listener
    state.recording = False
    if macro_mouse_listener:
        macro_mouse_listener.stop()
    if macro_keyboard_listener:
        macro_keyboard_listener.stop()
    rec_btn.configure(text="⏺ Record", fg_color=PURPLE)
    macro_status_var.set(f"✓ {len(state.macro_events)} events recorded")

def clear_macro():
    state.macro_events = []
    macro_count_var.set("0 events")
    macro_status_var.set("No macro recorded")

def save_macro():
    if not state.macro_events:
        import tkinter.messagebox as mb
        mb.showinfo("Empty", "Nothing to save.")
        return
    from tkinter.filedialog import asksaveasfilename
    p = asksaveasfilename(defaultextension=".json", filetypes=[("JSON Macro", "*.json")])
    if p:
        with open(p, "w") as f:
            json.dump(state.macro_events, f, indent=2)

def load_macro():
    from tkinter.filedialog import askopenfilename
    p = askopenfilename(filetypes=[("JSON Macro", "*.json")])
    if p:
        with open(p) as f:
            state.macro_events = json.load(f)
        macro_count_var.set(f"{len(state.macro_events)} events")
        macro_status_var.set(f"✓ Loaded {os.path.basename(p)}")

# ─── Multi-point ─────────────────────────────────────────────────────────────
def add_current_pos():
    x, y = pyautogui.position()
    state.multipoints.append((x, y))
    _refresh_points()

def remove_selected():
    sel = points_lb.curselection()
    if sel:
        state.multipoints.pop(sel[0])
        _refresh_points()

def clear_points():
    state.multipoints.clear()
    _refresh_points()

def _refresh_points():
    points_lb.delete(0, tk.END)
    for i, (x, y) in enumerate(state.multipoints):
        points_lb.insert(tk.END, f"  {i+1}.   x={x}  y={y}")
    mp_count_var.set(f"{len(state.multipoints)} point(s)")

# ─── Config ───────────────────────────────────────────────────────────────────
def save_config():
    cfg = {k: v.get() for k, v in {
        "h": hours_var, "m": mins_var, "s": secs_var, "ms": ms_var,
        "btn": btn_var, "action": action_var, "mode": mode_var,
        "repeat": repeat_var, "rmin": rnd_min_var, "rmax": rnd_max_var,
        "hk_start": start_hotkey_var, "hk_stop": stop_hotkey_var,
        "rand_pos": rand_pos_var, "mp": mp_enable_var,
    }.items()}
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return
    try:
        with open(CONFIG_FILE) as f:
            c = json.load(f)
        hours_var.set(c.get("h", "0")); mins_var.set(c.get("m", "0"))
        secs_var.set(c.get("s", "0")); ms_var.set(c.get("ms", "100"))
        btn_var.set(c.get("btn", "Left")); action_var.set(c.get("action", "Single"))
        mode_var.set(c.get("mode", "Infinite")); repeat_var.set(c.get("repeat", "100"))
        rnd_min_var.set(c.get("rmin", "0")); rnd_max_var.set(c.get("rmax", "0"))
        start_hotkey_var.set(c.get("hk_start", "F6"))
        stop_hotkey_var.set(c.get("hk_stop", "F7"))
        rand_pos_var.set(c.get("rand_pos", False))
        mp_enable_var.set(c.get("mp", False))
    except Exception:
        pass

# ═════════════════════════════════ BUILD UI ═══════════════════════════════════
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title(f"{APP_NAME}  v{VERSION}")
app.geometry("680x760")
app.resizable(False, False)
app.configure(fg_color=DARK)

# Variables
hours_var       = tk.StringVar(value="0")
mins_var        = tk.StringVar(value="0")
secs_var        = tk.StringVar(value="0")
ms_var          = tk.StringVar(value="100")
btn_var         = tk.StringVar(value="Left")
action_var      = tk.StringVar(value="Single")
mode_var        = tk.StringVar(value="Infinite")
repeat_var      = tk.StringVar(value="100")
rnd_min_var     = tk.StringVar(value="0")
rnd_max_var     = tk.StringVar(value="0")
start_hotkey_var= tk.StringVar(value="F6")
stop_hotkey_var = tk.StringVar(value="F7")
counter_var     = tk.StringVar(value="0")
rand_pos_var    = tk.BooleanVar(value=False)
mp_enable_var   = tk.BooleanVar(value=False)
macro_count_var = tk.StringVar(value="0 events")
macro_status_var= tk.StringVar(value="No macro recorded")
mp_count_var    = tk.StringVar(value="0 point(s)")

# ── Header
hdr = ctk.CTkFrame(app, fg_color=PANEL, corner_radius=0, height=60)
hdr.pack(fill="x")
hdr.pack_propagate(False)

ctk.CTkLabel(hdr, text="⚡  AutoClicker Pro",
             font=ctk.CTkFont(family="Arial", size=19, weight="bold"),
             text_color=ACCENT).pack(side="left", padx=18)

sf = ctk.CTkFrame(hdr, fg_color="transparent")
sf.pack(side="right", padx=18)
status_label = ctk.CTkLabel(sf, text="○  IDLE",
                              font=ctk.CTkFont(size=11), text_color=MUTED)
status_label.pack()

# ── Counter
cbar = ctk.CTkFrame(app, fg_color=CARD, corner_radius=0, height=72)
cbar.pack(fill="x")
cbar.pack_propagate(False)

ctk.CTkLabel(cbar, textvariable=counter_var,
             font=ctk.CTkFont(family="Arial", size=36, weight="bold"),
             text_color=ACCENT).pack(side="left", padx=24)
ctk.CTkLabel(cbar, text="CLICKS",
             font=ctk.CTkFont(size=9), text_color=MUTED).pack(side="left")
ctk.CTkButton(cbar, text="Reset", width=60, height=28,
              fg_color=BORDER, hover_color="#333",
              font=ctk.CTkFont(size=10), command=reset_counter).pack(
    side="right", padx=16)

# ── Notebook
notebook = ctk.CTkTabview(
    app, fg_color=CARD,
    segmented_button_fg_color=PANEL,
    segmented_button_selected_color=ACCENT,
    segmented_button_selected_hover_color="#00b894",
    segmented_button_unselected_color=PANEL,
    segmented_button_unselected_hover_color=BORDER,
    text_color=TEXT,
)
notebook.pack(fill="both", expand=True, padx=12, pady=(8, 4))
for t in ["Clicker", "Multi-Point", "Macro", "Hotkeys"]:
    notebook.add(t)

# ──────────────── CLICKER TAB ─────────────────────────────────────────────────
ct = notebook.tab("Clicker")

def section(parent, text, pady=(14, 4)):
    ctk.CTkLabel(parent, text=text, anchor="w",
                 font=ctk.CTkFont(size=12, weight="bold"), text_color=TEXT
                 ).pack(anchor="w", padx=16, pady=pady)

def lrow(parent, lbl):
    f = ctk.CTkFrame(parent, fg_color="transparent")
    f.pack(fill="x", padx=16, pady=(4, 0))
    ctk.CTkLabel(f, text=lbl, width=148, anchor="w",
                 font=ctk.CTkFont(size=11), text_color=MUTED).pack(side="left")
    return f

def divider(parent):
    ctk.CTkFrame(parent, fg_color=BORDER, height=1).pack(
        fill="x", padx=16, pady=10)

section(ct, "Click Interval")

def spin(parent, var, label):
    f = ctk.CTkFrame(parent, fg_color=PANEL, corner_radius=8)
    f.pack(side="left", padx=3)
    ctk.CTkEntry(f, textvariable=var, width=58, justify="center",
                 font=ctk.CTkFont(family="Courier", size=13),
                 fg_color="transparent", border_color=BORDER).pack(padx=4, pady=4)
    ctk.CTkLabel(f, text=label, font=ctk.CTkFont(size=9),
                 text_color=MUTED).pack(pady=(0, 4))

ir = ctk.CTkFrame(ct, fg_color="transparent")
ir.pack(fill="x", padx=16, pady=4)
for v, l in [(hours_var, "Hours"), (mins_var, "Mins"), (secs_var, "Secs"), (ms_var, "Ms")]:
    spin(ir, v, l)

divider(ct)
section(ct, "Click Type", (4, 4))

r1 = lrow(ct, "Mouse Button")
ctk.CTkSegmentedButton(r1, values=["Left", "Right", "Middle"],
                        variable=btn_var, width=210,
                        fg_color=PANEL, selected_color=ACCENT,
                        font=ctk.CTkFont(size=11)).pack(side="left")

r2 = lrow(ct, "Action")
ctk.CTkSegmentedButton(r2, values=["Single", "Double"],
                        variable=action_var, width=140,
                        fg_color=PANEL, selected_color=ACCENT,
                        font=ctk.CTkFont(size=11)).pack(side="left")

divider(ct)
section(ct, "Repeat Mode", (4, 4))

r3 = lrow(ct, "Mode")
ctk.CTkSegmentedButton(r3, values=["Infinite", "Fixed"],
                        variable=mode_var, width=160,
                        fg_color=PANEL, selected_color=ACCENT,
                        font=ctk.CTkFont(size=11)).pack(side="left")

r4 = lrow(ct, "Repeat Count")
ctk.CTkEntry(r4, textvariable=repeat_var, width=80, justify="center",
             font=ctk.CTkFont(family="Courier", size=12),
             fg_color=PANEL, border_color=BORDER).pack(side="left")

divider(ct)
section(ct, "Anti-Detection", (4, 4))

r5 = lrow(ct, "Interval jitter (ms)")
ctk.CTkEntry(r5, textvariable=rnd_min_var, width=60, justify="center",
             placeholder_text="min", fg_color=PANEL, border_color=BORDER
             ).pack(side="left", padx=(0, 6))
ctk.CTkLabel(r5, text="–", text_color=MUTED).pack(side="left")
ctk.CTkEntry(r5, textvariable=rnd_max_var, width=60, justify="center",
             placeholder_text="max", fg_color=PANEL, border_color=BORDER
             ).pack(side="left", padx=6)

r6 = lrow(ct, "Random position ±5px")
ctk.CTkSwitch(r6, text="", variable=rand_pos_var, width=44,
              progress_color=ACCENT).pack(side="left")

# ──────────────── MULTI-POINT TAB ─────────────────────────────────────────────
mp_tab = notebook.tab("Multi-Point")

section(mp_tab, "Sequential Click Targets")
ctk.CTkLabel(mp_tab, text="Clicks each target in order, loops back to start.",
             anchor="w", font=ctk.CTkFont(size=10), text_color=MUTED
             ).pack(anchor="w", padx=16)

mp_br = ctk.CTkFrame(mp_tab, fg_color="transparent")
mp_br.pack(fill="x", padx=16, pady=8)
ctk.CTkButton(mp_br, text="＋ Add Position", width=130,
              fg_color=ACCENT, hover_color="#00b894", text_color=DARK,
              font=ctk.CTkFont(size=11, weight="bold"),
              command=add_current_pos).pack(side="left", padx=(0, 6))
ctk.CTkButton(mp_br, text="✕ Remove", width=90, fg_color=PANEL,
              hover_color=BORDER, font=ctk.CTkFont(size=11),
              command=remove_selected).pack(side="left", padx=4)
ctk.CTkButton(mp_br, text="Clear", width=70, fg_color=PANEL,
              hover_color=BORDER, font=ctk.CTkFont(size=11),
              command=clear_points).pack(side="left", padx=4)

lb_wrap = ctk.CTkFrame(mp_tab, fg_color=PANEL, corner_radius=8)
lb_wrap.pack(fill="both", expand=True, padx=16, pady=(0, 8))
points_lb = tk.Listbox(lb_wrap, bg=PANEL, fg=TEXT, selectbackground=ACCENT,
                        selectforeground=DARK, relief="flat",
                        font=("Courier", 10), bd=0, highlightthickness=0)
points_lb.pack(fill="both", expand=True, padx=6, pady=6)

mp_ft = ctk.CTkFrame(mp_tab, fg_color="transparent")
mp_ft.pack(fill="x", padx=16)
ctk.CTkLabel(mp_ft, textvariable=mp_count_var, text_color=MUTED,
             font=ctk.CTkFont(size=10)).pack(side="left")
mp_sw = ctk.CTkFrame(mp_ft, fg_color="transparent")
mp_sw.pack(side="right")
ctk.CTkLabel(mp_sw, text="Enable:", text_color=MUTED,
             font=ctk.CTkFont(size=10)).pack(side="left")
ctk.CTkSwitch(mp_sw, text="", variable=mp_enable_var, width=44,
              progress_color=ACCENT).pack(side="left")

# ──────────────── MACRO TAB ───────────────────────────────────────────────────
mc_tab = notebook.tab("Macro")

section(mc_tab, "Macro Recorder")
ctk.CTkLabel(mc_tab, text="Records mouse clicks and keystrokes with precise timing for replay.",
             anchor="w", font=ctk.CTkFont(size=10), text_color=MUTED
             ).pack(anchor="w", padx=16)

ms_bar = ctk.CTkFrame(mc_tab, fg_color=PANEL, corner_radius=8, height=46)
ms_bar.pack(fill="x", padx=16, pady=10)
ms_bar.pack_propagate(False)
ctk.CTkLabel(ms_bar, textvariable=macro_status_var,
             font=ctk.CTkFont(family="Courier", size=11), text_color=ACCENT
             ).pack(side="left", padx=12)
ctk.CTkLabel(ms_bar, textvariable=macro_count_var,
             font=ctk.CTkFont(size=10), text_color=MUTED
             ).pack(side="right", padx=12)

mc_btns = ctk.CTkFrame(mc_tab, fg_color="transparent")
mc_btns.pack(fill="x", padx=16, pady=4)

rec_btn = ctk.CTkButton(mc_btns, text="⏺ Record", width=120,
                         fg_color=PURPLE, hover_color="#7c3aed",
                         font=ctk.CTkFont(size=11, weight="bold"),
                         command=toggle_recording)
rec_btn.pack(side="left", padx=(0, 6))
ctk.CTkButton(mc_btns, text="💾 Save", width=80, fg_color=PANEL,
              hover_color=BORDER, font=ctk.CTkFont(size=11), command=save_macro
              ).pack(side="left", padx=4)
ctk.CTkButton(mc_btns, text="📂 Load", width=80, fg_color=PANEL,
              hover_color=BORDER, font=ctk.CTkFont(size=11), command=load_macro
              ).pack(side="left", padx=4)
ctk.CTkButton(mc_btns, text="🗑 Clear", width=70, fg_color=PANEL,
              hover_color=BORDER, font=ctk.CTkFont(size=11), command=clear_macro
              ).pack(side="left", padx=4)

divider(mc_tab)
section(mc_tab, "Replay Settings", (4, 4))

r_m1 = lrow(mc_tab, "Mode")
ctk.CTkSegmentedButton(r_m1, values=["Infinite", "Fixed"],
                        variable=mode_var, width=160,
                        fg_color=PANEL, selected_color=ACCENT,
                        font=ctk.CTkFont(size=11)).pack(side="left")
r_m2 = lrow(mc_tab, "Repeat Count")
ctk.CTkEntry(r_m2, textvariable=repeat_var, width=80, justify="center",
             font=ctk.CTkFont(family="Courier", size=12),
             fg_color=PANEL, border_color=BORDER).pack(side="left")

# ──────────────── HOTKEYS TAB ─────────────────────────────────────────────────
hk_tab = notebook.tab("Hotkeys")

section(hk_tab, "Keyboard Shortcuts")
ctk.CTkLabel(hk_tab, text="Click 'Change' then press any key to reassign.",
             anchor="w", font=ctk.CTkFont(size=10), text_color=MUTED
             ).pack(anchor="w", padx=16)

def hk_row(parent, label, var):
    f = ctk.CTkFrame(parent, fg_color=PANEL, corner_radius=8, height=54)
    f.pack(fill="x", padx=16, pady=6)
    f.pack_propagate(False)
    ctk.CTkLabel(f, text=label, width=180, anchor="w",
                 font=ctk.CTkFont(size=11), text_color=MUTED
                 ).pack(side="left", padx=14)
    badge = ctk.CTkLabel(f, textvariable=var, fg_color=BORDER,
                          corner_radius=6, padx=14, pady=4,
                          font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
                          text_color=ACCENT)
    badge.pack(side="left")

    capturing = {"on": False}

    def start_cap():
        capturing["on"] = True
        var.set("Press key…")
        badge.configure(text_color=YELLOW)

    def on_kp(key):
        if not capturing["on"]:
            return
        capturing["on"] = False
        var.set(_key_str(key))
        badge.configure(text_color=ACCENT)
        return False

    def listen():
        with pkeyboard.Listener(on_press=on_kp) as ln:
            ln.join()

    def on_change():
        start_cap()
        threading.Thread(target=listen, daemon=True).start()

    ctk.CTkButton(f, text="Change", width=70, fg_color=CARD,
                   hover_color=BORDER, font=ctk.CTkFont(size=10),
                   command=on_change).pack(side="right", padx=10)

hk_row(hk_tab, "▶  Start / Toggle clicking", start_hotkey_var)
hk_row(hk_tab, "⏹  Stop clicking",           stop_hotkey_var)

# ── Bottom bar
bot = ctk.CTkFrame(app, fg_color=PANEL, corner_radius=0, height=66)
bot.pack(fill="x", side="bottom")
bot.pack_propagate(False)

start_btn = ctk.CTkButton(
    bot, text="▶  START", width=240, height=44,
    fg_color=ACCENT, hover_color="#00b894",
    font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
    text_color=DARK, corner_radius=10,
    command=toggle_clicking,
)
start_btn.pack(side="left", padx=18, pady=11)

ctk.CTkButton(bot, text="💾 Save Config", width=108, height=44,
              fg_color=CARD, hover_color=BORDER,
              font=ctk.CTkFont(size=10), command=save_config
              ).pack(side="right", padx=(4, 10), pady=11)
ctk.CTkButton(bot, text="📂 Load Config", width=108, height=44,
              fg_color=CARD, hover_color=BORDER,
              font=ctk.CTkFont(size=10), command=load_config
              ).pack(side="right", padx=4, pady=11)

# ── Global hotkey listener
hotkey_listener = pkeyboard.Listener(on_press=on_press, on_release=on_release)
hotkey_listener.daemon = True
hotkey_listener.start()

# ── Init
load_config()

def on_close():
    stop_clicking()
    if state.recording:
        _stop_recording()
    if hotkey_listener:
        hotkey_listener.stop()
    save_config()
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_close)
app.mainloop()
