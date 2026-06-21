"""Run controller: owns the timer model, both windows, render loop and hotkeys."""

from PySide6.QtCore import QObject, QPoint, QTimer, Signal
from PySide6.QtGui import QCursor, QFontMetrics, QGuiApplication
from PySide6.QtWidgets import QApplication

from ..constants import (
    OVERLAY_FONT_POINT_INCREASE,
    OVERLAY_HEIGHT_FACTOR,
    PASTEL_GREEN,
    PASTEL_RED,
    PASTEL_YELLOW,
    RENDER_INTERVAL_MS,
)
from ..formatting import format_duration
from ..timing import GREEN, RED, YELLOW, TimerModel
from .bar import OverlayBar
from .hotkeys import HotkeyBridge, start_global_hotkeys
from .square import MiniSquare

_STATUS_COLORS = {GREEN: PASTEL_GREEN, YELLOW: PASTEL_YELLOW, RED: PASTEL_RED}

_SECONDS_PER_HOUR = 3600
_TIMER_WIDTH_PADDING = 6
_NAME_WIDTH_PADDING = 6
_NEXT_WIDTH_PADDING = 10
_SQUARE_TOP_MARGIN = 10


class RunController(QObject):
    """Owns the timer model, both windows, the render loop and global hotkeys."""

    finished = Signal()

    def __init__(self, sections, lateness_seconds, yellow_percent, yellow_seconds):
        super().__init__()
        self.model = TimerModel(sections, lateness_seconds)
        self.yellow_percent = yellow_percent
        self.yellow_seconds = yellow_seconds

        font = QApplication.font()
        if font.pointSize() > 0:
            font.setPointSize(font.pointSize() + OVERLAY_FONT_POINT_INCREASE)
        metrics = QFontMetrics(font)
        bar_height = int(metrics.height() * OVERLAY_HEIGHT_FACTOR)

        self.show_hours = max(s.seconds for s in sections) >= _SECONDS_PER_HOUR
        timer_width, name_width, next_width = self._measure_widths(metrics, sections)

        self.bar = OverlayBar(font, bar_height, timer_width, name_width, next_width)
        self.bar.adjustSize()
        self.bar.setFixedWidth(self.bar.width())
        self.square = MiniSquare(bar_height)
        self._square_shown = False
        self._square_home = QPoint()

        self._connect_windows()

        self._render_timer = QTimer(self)
        self._render_timer.timeout.connect(self.tick)
        self._render_timer.start(RENDER_INTERVAL_MS)

        self._place_bar()
        self.bar.show()
        self.tick()

        self._hotkey_bridge = HotkeyBridge()
        self._hotkey_bridge.next_requested.connect(self.on_next_button)
        self._hotkey_bridge.back_requested.connect(self.on_back)
        self._hotkey_listener = start_global_hotkeys(self._hotkey_bridge)

    # --- setup ----------------------------------------------------------

    def _measure_widths(self, metrics: QFontMetrics, sections):
        """Size every variable-width part to its worst case for this run."""
        worst_seconds = max(s.seconds for s in sections)
        worst_timer_text = "-" + format_duration(worst_seconds, self.show_hours)
        timer_width = metrics.horizontalAdvance(worst_timer_text) + _TIMER_WIDTH_PADDING

        longest_name = max((s.name for s in sections), key=len, default="")
        name_width = metrics.horizontalAdvance(longest_name) + _NAME_WIDTH_PADDING

        next_labels = ["→ " + s.name for s in sections] + ["→ End"]
        widest_next = max(metrics.horizontalAdvance(label) for label in next_labels)
        next_width = widest_next + _NEXT_WIDTH_PADDING
        return timer_width, name_width, next_width

    def _connect_windows(self):
        self.bar.back_clicked.connect(self.on_back)
        self.bar.next_clicked.connect(self.on_next_button)
        self.bar.minimize_clicked.connect(self.minimize)
        self.bar.cancel_clicked.connect(self.cancel)
        self.square.clicked.connect(self.restore)

    # --- placement ------------------------------------------------------

    def _place_bar(self):
        screen = QGuiApplication.screenAt(QCursor.pos()) or QGuiApplication.primaryScreen()
        geometry = screen.availableGeometry()
        left = geometry.x() + (geometry.width() - self.bar.width()) // 2
        self.bar.move(left, geometry.y())
        square_left = geometry.x() + (geometry.width() - self.square.width()) // 2
        self._square_home = QPoint(square_left, geometry.y() + _SQUARE_TOP_MARGIN)

    # --- render ---------------------------------------------------------

    def tick(self):
        remaining = self.model.remaining()
        self.bar.set_timer_text(format_duration(remaining, self.show_hours))
        self.bar.set_current(self.model.current.name)
        upcoming = self.model.next_section
        self.bar.set_next("→ " + (upcoming.name if upcoming else "End"))
        status = self.model.color(self.yellow_percent, self.yellow_seconds)
        color = _STATUS_COLORS[status]
        self.bar.set_color(color)
        self.square.set_color(color)

    # --- actions --------------------------------------------------------

    def on_next_button(self):
        # On the last section the button reads "End" and quits the program.
        if self.model.is_last:
            self.cancel()
        else:
            self.model.advance()
            self.tick()

    def on_back(self):
        if self.model.go_back():
            self.tick()

    def minimize(self):
        if not self._square_shown:
            self.square.move(self._square_home)
            self._square_shown = True
        self.bar.hide()
        self.square.show()

    def restore(self):
        self.square.hide()
        self._place_bar()
        self.bar.show()

    def cancel(self):
        self._render_timer.stop()
        self._stop_hotkeys()
        self.bar.close()
        self.square.close()
        self.finished.emit()

    def _stop_hotkeys(self):
        if self._hotkey_listener is not None:
            self._hotkey_listener.stop()
            self._hotkey_listener = None
