"""The minimized square: a draggable, color-only status indicator."""

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtWidgets import QWidget

_FRAMELESS_TOPMOST = Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
_DRAG_THRESHOLD_PX = 4


class MiniSquare(QWidget):
    """Small draggable square that signals status by color; a click restores."""

    clicked = Signal()

    def __init__(self, size: int):
        super().__init__(None, _FRAMELESS_TOPMOST)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedSize(size, size)
        self._press_position = None
        self._window_origin = QPoint()
        self._dragged = False

    def set_color(self, color: str):
        self.setStyleSheet(f"background:{color};")

    def mousePressEvent(self, event):
        self._press_position = event.globalPosition().toPoint()
        self._window_origin = self.pos()
        self._dragged = False

    def mouseMoveEvent(self, event):
        if self._press_position is None:
            return
        offset = event.globalPosition().toPoint() - self._press_position
        if offset.manhattanLength() > _DRAG_THRESHOLD_PX:
            self._dragged = True
        self.move(self._window_origin + offset)

    def mouseReleaseEvent(self, event):
        if self._press_position is not None and not self._dragged:
            self.clicked.emit()
        self._press_position = None
