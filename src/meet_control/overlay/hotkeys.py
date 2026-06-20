"""Global hotkey support via pynput, marshalled onto the Qt main thread."""

from PySide6.QtCore import QObject, Signal


class HotkeyBridge(QObject):
    """Turns pynput's background-thread callbacks into Qt main-thread signals."""

    next_requested = Signal()
    back_requested = Signal()


def start_global_hotkeys(bridge: HotkeyBridge):
    """Start listening for the global next/back hotkeys.

    Returns the listener (so it can be stopped later), or None when global
    hotkeys are unavailable (pynput missing, or blocked e.g. under Wayland).
    """
    try:
        from pynput import keyboard
    except Exception:
        return None
    try:
        listener = keyboard.GlobalHotKeys(
            {
                "<ctrl>+<alt>+d": bridge.next_requested.emit,  # right = next
                "<ctrl>+<alt>+a": bridge.back_requested.emit,  # left = back
            }
        )
        listener.start()
        return listener
    except Exception:
        return None
