# AutoClicker Pro

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/UNKNOWN-X0/AutoClickerPro)](https://github.com/UNKNOWN-X0/AutoClickerPro/releases)
[![Pylint](https://github.com/UNKNOWN-X0/AutoClickerPro/actions/workflows/pylint.yml/badge.svg)](https://github.com/UNKNOWN-X0/AutoClickerPro/actions/workflows/pylint.yml)

AutoClicker Pro is a Python desktop app for automating mouse clicks and recording simple mouse-and-keyboard macros. It uses a dark interface and saves its settings locally.

## Features

- Configure click interval down to milliseconds and choose left, right, or middle click, including double-clicks.
- Repeat clicks indefinitely or set a fixed count.
- Cycle through multiple screen coordinates, with optional timing and position variation.
- Assign keyboard shortcuts to start and stop clicking.
- Record and replay mouse and keyboard input sequences.
- Save and restore app settings automatically.
- Move the pointer to the top-left corner to trigger PyAutoGUI's emergency failsafe.

## Run from source

Requires Python 3.8 or later.

```bash
python -m pip install -r requirements.txt
python auto_clicker.py
```

On macOS, you may need to grant Accessibility permissions to the terminal or packaged app before it can control the mouse and keyboard. Platform permissions and input-library support can also affect behavior on other systems.

## Build an executable

Run the build helper on the operating system you want to package for:

```bash
python build.py
```

The helper installs PyInstaller if needed, then writes the executable to `dist/`. Build artifacts are local; download-ready binaries are available only if published on the [Releases](../../releases) page.

## Configuration and privacy

The app stores settings in `~/.autoclicker_config.json`. The project code does not include an analytics or telemetry service. Macro files can contain recorded key presses and screen coordinates, so review them before sharing.

## Project layout

- `auto_clicker.py` — launcher
- `autoclicker/app.py` — desktop interface and event handlers
- `autoclicker/engine.py` — click and macro playback logic
- `autoclicker/config.py` — app constants and local settings path
- `autoclicker/state.py` — shared runtime state
- `autoclicker/dependencies.py` — UI and input-library setup
- `build.py` — local executable packaging helper
- `tests/test_engine.py` — engine regression tests

## Tests

Run the engine tests with:

```bash
python -m unittest discover -s tests
```

The tests use fake input devices and do not move or click the real mouse.

## License

MIT — see [LICENSE](LICENSE).
