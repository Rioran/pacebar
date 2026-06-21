"""The flat top strip shown while a meeting runs."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

_FRAMELESS_TOPMOST = Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool


class OverlayBar(QWidget):
    """The flat top strip. Every variable-width part is pinned so width is stable."""

    back_clicked = Signal()
    next_clicked = Signal()
    minimize_clicked = Signal()
    cancel_clicked = Signal()

    def __init__(
        self,
        font: QFont,
        height: int,
        timer_width: int,
        name_width: int,
        next_width: int,
    ):
        super().__init__(None, _FRAMELESS_TOPMOST)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(height)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(10)

        self.back_button = self._make_flat_button("◀", font)
        self.timer_label = QLabel()
        self.timer_label.setFont(font)
        self.timer_label.setFixedWidth(timer_width)
        self.current_label = QLabel()
        self.current_label.setFont(font)
        self.current_label.setFixedWidth(name_width)
        self.next_button = self._make_flat_button("", font)
        self.next_button.setFixedWidth(next_width)
        self.minimize_button = self._make_flat_button("▢", font)
        self.cancel_button = self._make_flat_button("✕", font)

        layout.addWidget(self.back_button)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.current_label)
        layout.addWidget(self.next_button)
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.cancel_button)

        self.back_button.clicked.connect(self.back_clicked)
        self.next_button.clicked.connect(self.next_clicked)
        self.minimize_button.clicked.connect(self.minimize_clicked)
        self.cancel_button.clicked.connect(self.cancel_clicked)

    def _make_flat_button(self, text: str, font: QFont) -> QPushButton:
        button = QPushButton(text)
        button.setFont(font)
        button.setFlat(True)
        button.setCursor(Qt.PointingHandCursor)
        button.setFocusPolicy(Qt.NoFocus)
        button.setStyleSheet(
            "QPushButton{border:none;background:transparent;padding:0 4px;text-align:left;}"
            "QPushButton:hover{background:rgba(0,0,0,0.08);}"
        )
        return button

    def set_color(self, color: str):
        self.setStyleSheet(f"OverlayBar{{background:{color};}}")

    def set_timer_text(self, text: str):
        self.timer_label.setText(text)

    def set_current(self, name: str):
        self.current_label.setText(name)

    def set_next(self, label: str):
        self.next_button.setText(label)
