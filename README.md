# ⚡ AutoClicker Pro

A powerful, cross-platform auto clicker with a clean dark UI — built with Python.

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)
![Release](https://img.shields.io/github/v/release/UNKNOWN-X0/AutoClickerPro/releases/tag/V1.0.0)

---

## ✨ Features

| Feature | Description |
|---|---|
| ⚡ **Custom Speed** | Set interval by Hours / Mins / Secs / Milliseconds |
| 🖱️ **Click Types** | Left, Right, Middle — Single or Double click |
| 🗺️ **Multi-Point** | Sequential click targets with automatic looping |
| 🎲 **Anti-Detection** | Random interval jitter + random position offset |
| ⌨️ **Hotkeys** | Fully customizable start/stop keyboard shortcuts |
| 🔁 **Repeat Modes** | Infinite loop or fixed repeat count |
| 🎬 **Macro Recorder** | Record & replay mouse + keyboard sequences with timing |
| 💾 **Config Saving** | Settings auto-saved and restored on next launch |

---

## 📥 Download (No Python required)

Go to the [**Releases**](../../releases) page and download for your OS:

| OS | File |
|---|---|
| 🪟 Windows | `AutoClickerPro-windows.exe` |
| 🍎 macOS | `AutoClickerPro-macos` |
| 🐧 Linux | `AutoClickerPro-linux` |

> **Windows:** You may see a SmartScreen warning — click "More info → Run anyway". This is normal for unsigned apps.  
> **macOS:** Run `chmod +x AutoClickerPro-macos && ./AutoClickerPro-macos` or right-click → Open.  
> **Linux:** Run `chmod +x AutoClickerPro-linux && ./AutoClickerPro-linux`

---

## 🐍 Run from Source

### Requirements
- Python 3.8+
- pip

### Install dependencies

```bash
pip install customtkinter pyautogui pynput
```

### Run

```bash
python auto_clicker.py
```

---

## 🔨 Build Executable Yourself

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name AutoClickerPro auto_clicker.py
```

Output will be in the `dist/` folder.

---

## 🛡️ Safety

- PyAutoGUI **failsafe is enabled** — move your mouse to the **top-left corner** of the screen to emergency-stop all clicking.
- No data is collected. The app only saves your settings locally at `~/.autoclicker_config.json`.

---

## 🖥️ Screenshots

> _Add screenshots here after first run_

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

## 🤝 Contributing

Pull requests welcome! Please open an issue first to discuss major changes.
