
# ─── App State ────────────────────────────────────────────────────────────────
class AppState:
    def __init__(self):
        self.running = False
        self.recording = False
        self.click_count = 0
        self.macro_events = []
        self.multipoints = []


state = AppState()
