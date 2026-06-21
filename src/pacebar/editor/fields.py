"""Input widgets for a section row: the minutes spin box and the name field."""

from PySide6.QtCore import QEvent, Qt, QTimer, Signal
from PySide6.QtWidgets import QLineEdit, QSpinBox

from ..constants import (
    MAX_SECTION_MINUTES,
    MAX_SECTION_NAME_LENGTH,
    MIN_SECTION_MINUTES,
    PASTEL_RED,
)

_TAB_KEYS = (Qt.Key_Tab, Qt.Key_Backtab)
_ENTER_KEYS = (Qt.Key_Return, Qt.Key_Enter)
_MINUTES_FIELD_WIDTH = 95
_NAME_OVERFLOW_BLINK_MS = 120


class MinutesSpinBox(QSpinBox):
    """Whole-minutes spin box that keeps Tab and Enter inside the current row."""

    tab_pressed = Signal()
    enter_pressed = Signal()

    def __init__(self, value: int = MIN_SECTION_MINUTES):
        super().__init__()
        self.setRange(MIN_SECTION_MINUTES, MAX_SECTION_MINUTES)
        self.setValue(max(MIN_SECTION_MINUTES, value))
        self.setSuffix(" min")
        self.setFixedWidth(_MINUTES_FIELD_WIDTH)

    def event(self, event):
        # Tab is consumed by the focus framework before keyPressEvent, so we
        # intercept it here in event() instead.
        if event.type() == QEvent.KeyPress:
            if event.key() in _TAB_KEYS:
                self.tab_pressed.emit()
                return True
            if event.key() in _ENTER_KEYS:
                self.enter_pressed.emit()
                return True
        return super().event(event)


class NameLineEdit(QLineEdit):
    """Section name field: caps at MAX_SECTION_NAME_LENGTH and blinks when full."""

    tab_pressed = Signal()
    enter_pressed = Signal()
    up_pressed = Signal()
    down_pressed = Signal()

    def __init__(self, text: str = ""):
        super().__init__(text)
        self.setMaxLength(MAX_SECTION_NAME_LENGTH)
        self.setPlaceholderText("Section name")
        self._default_style = self.styleSheet()

    def event(self, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key in _TAB_KEYS:
                self.tab_pressed.emit()
                return True
            if key in _ENTER_KEYS:
                self.enter_pressed.emit()
                return True
            # Up/Down jump between rows (the spin box keeps arrows for its value).
            if key == Qt.Key_Up:
                self.up_pressed.emit()
                return True
            if key == Qt.Key_Down:
                self.down_pressed.emit()
                return True
            if self._is_overflow_keystroke(event):
                self._blink()
                return True
        return super().event(event)

    def _is_overflow_keystroke(self, event) -> bool:
        text = event.text()
        return bool(
            text
            and text.isprintable()
            and len(self.text()) >= MAX_SECTION_NAME_LENGTH
            and not self.hasSelectedText()
        )

    def _blink(self):
        self.setStyleSheet(f"background:{PASTEL_RED};")
        QTimer.singleShot(_NAME_OVERFLOW_BLINK_MS, lambda: self.setStyleSheet(self._default_style))
