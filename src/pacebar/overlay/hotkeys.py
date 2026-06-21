"""Global hotkeys.

On Windows we use the native ``RegisterHotKey`` API plugged into Qt's own
message loop via a native event filter. That is far more robust in a frozen
``--windowed`` exe than a background low-level keyboard hook (which silently
receives no events there). On other platforms we fall back to pynput.
"""

import sys

from PySide6.QtCore import QAbstractNativeEventFilter, QCoreApplication, QObject, Signal


class HotkeyBridge(QObject):
    """Carries hotkey events as Qt signals delivered on the main thread."""

    next_requested = Signal()
    back_requested = Signal()


# Win32 RegisterHotKey modifiers / message / virtual-key codes.
_MOD_ALT = 0x0001
_MOD_CONTROL = 0x0002
_MOD_NOREPEAT = 0x4000
_WM_HOTKEY = 0x0312
_VK_A = 0x41
_VK_D = 0x44
_HOTKEY_NEXT = 1
_HOTKEY_BACK = 2


class _WindowsHotkeys(QAbstractNativeEventFilter):
    """Ctrl+Alt+D / Ctrl+Alt+A via native RegisterHotKey + Qt's message pump."""

    def __init__(self, bridge: HotkeyBridge):
        super().__init__()
        import ctypes
        from ctypes import wintypes

        self._wintypes = wintypes
        self._user32 = ctypes.windll.user32
        self._user32.RegisterHotKey.argtypes = [
            wintypes.HWND,
            ctypes.c_int,
            wintypes.UINT,
            wintypes.UINT,
        ]
        self._user32.RegisterHotKey.restype = wintypes.BOOL
        self._user32.UnregisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int]
        self._user32.UnregisterHotKey.restype = wintypes.BOOL

        self._bridge = bridge
        self._ids: list[int] = []
        modifiers = _MOD_CONTROL | _MOD_ALT | _MOD_NOREPEAT
        for hotkey_id, virtual_key in ((_HOTKEY_NEXT, _VK_D), (_HOTKEY_BACK, _VK_A)):
            if self._user32.RegisterHotKey(None, hotkey_id, modifiers, virtual_key):
                self._ids.append(hotkey_id)
        QCoreApplication.instance().installNativeEventFilter(self)

    def nativeEventFilter(self, event_type, message):
        if event_type == b"windows_generic_MSG":
            msg = self._wintypes.MSG.from_address(int(message))
            if msg.message == _WM_HOTKEY:
                if msg.wParam == _HOTKEY_NEXT:
                    self._bridge.next_requested.emit()
                elif msg.wParam == _HOTKEY_BACK:
                    self._bridge.back_requested.emit()
        return False, 0

    def stop(self):
        app = QCoreApplication.instance()
        if app is not None:
            app.removeNativeEventFilter(self)
        for hotkey_id in self._ids:
            self._user32.UnregisterHotKey(None, hotkey_id)
        self._ids = []


def start_global_hotkeys(bridge: HotkeyBridge):
    """Start global hotkeys. Returns a handle with .stop(), or None if unavailable."""
    if sys.platform == "win32":
        try:
            return _WindowsHotkeys(bridge)
        except Exception:
            return None
    return _start_pynput(bridge)


def _start_pynput(bridge: HotkeyBridge):
    """Fallback for non-Windows (X11 etc.). May be blocked under Wayland."""
    try:
        from pynput import keyboard
    except Exception:
        return None

    def on_next():
        bridge.next_requested.emit()

    def on_back():
        bridge.back_requested.emit()

    try:
        listener = keyboard.GlobalHotKeys(
            {
                "<ctrl>+<alt>+d": on_next,
                "<ctrl>+<alt>+a": on_back,
            }
        )
        listener.start()
        return listener
    except Exception:
        return None
