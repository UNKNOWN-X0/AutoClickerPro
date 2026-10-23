# Graph Report - AutoClickerPro  (2026-10-24)

## Corpus Check
- Corpus is ~2,836 words - fits in a single context window. You may not need a graph.

## Summary
- 109 nodes · 162 edges · 8 communities (5 shown, 3 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 15 edges (avg confidence: 0.85)
- Token cost: unavailable (agent usage metadata was not exposed)

## Community Hubs (Navigation)
- Application Interface
- Click and Macro Engine
- Pylint CI Workflow
- Input Engine Tests
- App Guide and Safety
- Build Configuration
- Input Event Listeners

## God Nodes (most connected - your core abstractions)
1. `EngineTests` - 8 edges
2. `AutoClicker Pro desktop app` - 7 edges
3. `steps` - 5 edges
4. `click_loop()` - 5 edges
5. `macro_replay()` - 5 edges
6. `start_clicking()` - 5 edges
7. `stop_clicking()` - 5 edges
8. `_refresh_status()` - 5 edges
9. `hk_row()` - 5 edges
10. `click_loop()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `click_loop()` --calls--> `click_loop()`  [EXTRACTED]
  autoclicker/app.py → autoclicker/engine.py
- `macro_replay()` --calls--> `macro_replay()`  [EXTRACTED]
  autoclicker/app.py → autoclicker/engine.py
- `Mouse click automation` --conceptually_related_to--> `PyAutoGUI input automation dependency`  [INFERRED]
  README.md → requirements.txt
- `Mouse and keyboard macro recording and replay` --conceptually_related_to--> `pynput keyboard and mouse input dependency`  [INFERRED]
  README.md → requirements.txt

## Import Cycles
- None detected.

## Communities (8 total, 3 thin omitted)

### Community 0 - "Application Interface"
Cohesion: 0.13
Nodes (16): add_current_pos(), clear_points(), click_loop(), macro_replay(), on_close(), on_press(), _refresh_points(), _refresh_status() (+8 more)

### Community 1 - "Click and Macro Engine"
Cohesion: 0.17
Nodes (4): click_loop(), do_click(), macro_replay(), AppState

### Community 2 - "Pylint CI Workflow"
Cohesion: 0.13
Nodes (14): runs-on, steps, strategy, jobs, build, python-version, name, name (+6 more)

### Community 4 - "App Guide and Safety"
Cohesion: 0.17
Nodes (11): AutoClicker Pro desktop app, Top-left pointer emergency failsafe, Engine tests use fake input devices, Locally saved application settings, Mouse and keyboard macro recording and replay, Mouse click automation, Python package requirements, CustomTkinter UI dependency (+3 more)

### Community 6 - "Input Event Listeners"
Cohesion: 0.28
Nodes (8): hk_row(), listen(), on_change(), on_kp(), start_cap(), _key_str(), _start_recording(), on_kp()

## Knowledge Gaps
- **5 isolated node(s):** `Locally saved application settings`, `Top-left pointer emergency failsafe`, `Engine tests use fake input devices`, `CustomTkinter UI dependency`, `Pillow image library dependency`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 42 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `hk_row()` connect `Input Event Listeners` to `Application Interface`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `click_loop()` (e.g. with `_refresh_status()` and `_update_counter()`) actually correct?**
  _`click_loop()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Locally saved application settings`, `Top-left pointer emergency failsafe`, `Engine tests use fake input devices` to the rest of the system?**
  _5 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Application Interface` be split into smaller, more focused modules?**
  _Cohesion score 0.1282051282051282 - nodes in this community are weakly interconnected._
- **Why does `_start_recording()` connect `Input Event Listeners` to `Application Interface`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `macro_replay()` (e.g. with `_refresh_status()` and `_update_counter()`) actually correct?**
  _`macro_replay()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `Pylint CI Workflow` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._