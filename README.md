# PaceBar

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-555)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![Made with Claude Code](https://img.shields.io/badge/Made%20with-Claude%20Code-D97757?logo=anthropic&logoColor=white)

A small desktop tool that keeps you on time through any sequence of timed stages —
a sales call, a talk, a workout, even a recipe. You enter the stages and how many
minutes each should take; on **Start** a flat,
always-on-top strip appears across the top of the screen and counts the current
section down. The strip is **green** while you are on pace, **pastel yellow** when
the section is almost over, and **pastel red** once you have run over — so you can
feel the pacing without staring at numbers.

Written in Python with **PySide6**. Built cross-platform (Windows + Linux);
**tested and working on Windows 11**, **not yet tested on Linux** (feedback welcome).

## Screenshots

The setup window — one row per section, plus the start / lateness / reset toolbar:

![Setup window](https://raw.githubusercontent.com/Rioran/pacebar/main/docs/images/editor.png)

The running strip (here ~2 minutes left on the current section, next section as a
button), and the minimized square that signals status by color alone:

![Running strip](https://raw.githubusercontent.com/Rioran/pacebar/main/docs/images/strip.png)

![Minimized square](https://raw.githubusercontent.com/Rioran/pacebar/main/docs/images/minimized.png)

## Requirements

- [uv](https://docs.astral.sh/uv/) (manages the virtual environment and dependencies)
- Python 3.10+ (uv can install it for you)

## Install & run

PaceBar is on [PyPI](https://pypi.org/project/pacebar/) — no clone needed. It pulls in
PySide6 automatically (a ~100 MB download the first time). Pick whichever fits you:

**With [uv](https://docs.astral.sh/uv/) — recommended** (isolated, adds a global `pacebar` command):

```bash
uv tool install pacebar
pacebar
```

If the `pacebar` command isn't found afterwards, run `uv tool update-shell` once and
reopen the terminal. Upgrade later with `uv tool upgrade pacebar`.

**Just try it once, without installing:**

```bash
uvx pacebar
```

**With plain pip** (into a virtual environment):

```bash
python -m venv .venv
# Windows:        .venv\Scripts\activate
# Linux / macOS:  source .venv/bin/activate
pip install pacebar
pacebar
```

Runs from any folder; the last schedule is saved to `pacebar_last_run.json` in the
current working directory. Not a Python user? Grab the standalone executable instead
(see [Build a standalone executable](#build-a-standalone-executable)).

## Run from source

```bash
uv sync            # create the venv and install dependencies
uv run pacebar
```

Or run it in **one click** — double-click the script for your OS:

- **Windows:** `scripts\run.bat`
- **Linux / macOS:** `scripts/run.sh`

(`uv sync` runs automatically the first time `uv run` is used.)

## Build a standalone executable

One click: double-click `scripts\build.bat` (Windows) or `scripts/build.sh`
(Linux / macOS). Or run it manually:

```bash
uv run --extra build pyinstaller --noconfirm --clean pacebar.spec
```

The build is driven by [`pacebar.spec`](pacebar.spec) (a single
`--windowed --onefile` build). The result lands in `dist/` (`pacebar.exe` on
Windows) — one shareable file; it starts a touch slower because it unpacks to a temp
dir on launch.

PyInstaller does **not** cross-compile: it freezes for the OS you run the build on.
Build on Windows to get the `.exe`, and on Linux (or WSL) to get a Linux binary — each
runs only on its own platform. For a platform-independent option, use `pip install`
above instead.

## Lint & format

```bash
uv run ruff format .   # format
uv run ruff check .    # lint
```

## Publishing to PyPI (maintainer)

```bash
uv build                          # builds the wheel + sdist into dist/
uv publish dist/pacebar-*    # upload (needs a PyPI account + API token)
```

The `pacebar-*` glob is deliberate: it uploads only the wheel and sdist and skips
`pacebar.exe`, which also lives in `dist/`. Test on TestPyPI first
(`uv publish --publish-url https://test.pypi.org/legacy/ ...`), and make sure the
project name is still available on PyPI before the first real upload.

## How to use

**Setup window**

- Each row is one section: **minutes** (whole positive number — arrows or type) and a
  **name** (max 30 characters; it blinks red if you try to type more).
- **Tab / Shift+Tab** move between the two fields of the current row only.
  **Up / Down** (while in the name field) jump to the name field of the row above /
  below. **Enter** adds a new row. The `+` button also adds one; the ▲/▼ control
  reorders; `✕` deletes.
- **Start** is top-left. Next to it is **minutes late** — how late the meeting is
  actually starting (subtracted from the first section). **Reset** clears everything
  back to one empty row (no confirmation, by design).
- **Yellow at … % or … s** controls the warning threshold: the strip turns yellow
  when the remaining time drops below *whichever is larger* — that percentage of the
  section, or that many seconds.

**Running strip** (left → right)

- ◀ **Back** — roll back one section. It resumes on the same global timeline: with the
  time it still had if you switched early, or already overdue if you had overrun it.
- **Timer** — counts the current section down; format `HH:MM:SS` with the hours group
  hidden when no section is an hour or longer. Goes negative when you run over.
- **Current section name.**
- **→ Next section** — click to advance. On the last section it reads **→ End**;
  clicking it exits the program.
- ▢ **Minimize** — collapses to a small square that signals status by color only.
  Drag it anywhere; click it to restore the full strip.
- ✕ **Cancel** — quits the program.

**Global hotkeys** (work even when another app is focused), laid out like game
left/right (D = forward, A = back):

- **Ctrl+Alt+D** — next section (right); on the last section it triggers **End** (exit)
- **Ctrl+Alt+A** — back (left)

> Chosen to stay clear of common conflicts: plain Alt+A mutes the mic in Zoom and
> Alt+D jumps to the browser address bar. On non-US layouts Ctrl+Alt equals AltGr,
> but that only matters while typing into a text field, not during a call.

> The strip is intentionally visible to everyone on a screen share — it keeps the
> whole call honest about time. There is deliberately **no pause**: business calls
> have hard stops.

## Saved state

On every Start the schedule (order, minutes, names — no lateness, no thresholds) is
written to `pacebar_last_run.json`, and it is loaded back the next time you launch. This
also makes the tool handy for rehearsing a talk.

The file lives **next to the running exe**, so each copy of the app keeps its own
typical call scenario — drop a copy in a different project folder and it remembers a
different schedule. (When running from source there is no exe, so it uses the current
working directory instead.)

## Notes & limitations

- Global hotkeys need the `pynput` package (already a dependency). On Linux they work
  under **X11**; under **Wayland** they may be blocked — the on-strip buttons always
  work regardless.
- Always-on-top is reliable over windowed apps (Zoom/Meet/Teams). A few apps in true
  fullscreen-exclusive mode can still cover any topmost window.
- The strip width is fixed for the run from the widest section name and worst-case
  timer. An extreme overrun (more minutes over than the longest section) can still
  nudge the timer width.
