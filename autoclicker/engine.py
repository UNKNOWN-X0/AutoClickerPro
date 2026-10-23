import random
import time
from .dependencies import pyautogui
from .state import state

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


def click_loop(cfg, update_counter, schedule_refresh):
    mode = cfg["mode"]
    repeat_n = cfg["repeat_n"]
    btn = cfg["button"]
    action = cfg["action"]
    interval = cfg["interval"]
    rnd_min = cfg["rand_min"]
    rnd_max = cfg["rand_max"]
    use_mp = cfg["use_multipoint"]
    points = cfg["points"]
    rand_pos = cfg["rand_pos"]
    mp_idx = 0
    count = 0

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
        update_counter()
        delay = interval
        if rnd_min < rnd_max:
            delay += random.randint(rnd_min, rnd_max) / 1000.0
        time.sleep(delay)

    state.running = False
    schedule_refresh()


def macro_replay(events, repeat_n, infinite, update_counter, schedule_refresh):
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
                    update_counter()
                elif ev["type"] == "key":
                    pyautogui.press(ev["key"])
            except Exception:
                pass
        loops += 1
    state.running = False
    schedule_refresh()


