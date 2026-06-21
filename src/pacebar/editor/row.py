"""A single editable section row."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QToolButton, QVBoxLayout, QWidget

from ..timing import Section
from .fields import MinutesSpinBox, NameLineEdit

_MOVE_BUTTON_WIDTH = 26
_MOVE_BUTTON_HEIGHT = 13
_ROW_BUTTON_WIDTH = 30


class RowWidget(QWidget):
    """One section row: minutes, name, reorder, add and delete controls."""

    add_after_requested = Signal(object)
    delete_requested = Signal(object)
    move_up_requested = Signal(object)
    move_down_requested = Signal(object)
    focus_up_requested = Signal(object)
    focus_down_requested = Signal(object)

    def __init__(self, minutes: int = 1, name: str = ""):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.minutes = MinutesSpinBox(minutes)
        self.name = NameLineEdit(name)

        self.move_up_button = QToolButton()
        self.move_up_button.setText("▲")
        self.move_down_button = QToolButton()
        self.move_down_button.setText("▼")
        move_box = self._build_move_box()

        self.add_button = QPushButton("+")
        self.delete_button = QPushButton("✕")
        for button in (self.add_button, self.delete_button):
            button.setFixedWidth(_ROW_BUTTON_WIDTH)
            button.setFocusPolicy(Qt.NoFocus)

        layout.addWidget(self.minutes)
        layout.addWidget(self.name, 1)
        layout.addWidget(move_box)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)

        self._connect_signals()

    def _build_move_box(self) -> QWidget:
        """A visually-joined up/down control."""
        box = QWidget()
        box_layout = QVBoxLayout(box)
        box_layout.setContentsMargins(0, 0, 0, 0)
        box_layout.setSpacing(0)
        for button in (self.move_up_button, self.move_down_button):
            button.setAutoRaise(True)
            button.setFocusPolicy(Qt.NoFocus)
            button.setFixedSize(_MOVE_BUTTON_WIDTH, _MOVE_BUTTON_HEIGHT)
            box_layout.addWidget(button)
        return box

    def _connect_signals(self):
        # Tab / Shift+Tab cycle only between the two fields of this row.
        self.minutes.tab_pressed.connect(self.name.setFocus)
        self.name.tab_pressed.connect(self.minutes.setFocus)
        # Enter in either field appends a new row.
        self.minutes.enter_pressed.connect(lambda: self.add_after_requested.emit(self))
        self.name.enter_pressed.connect(lambda: self.add_after_requested.emit(self))
        # Up/Down in the name field move between existing rows.
        self.name.up_pressed.connect(lambda: self.focus_up_requested.emit(self))
        self.name.down_pressed.connect(lambda: self.focus_down_requested.emit(self))

        self.move_up_button.clicked.connect(lambda: self.move_up_requested.emit(self))
        self.move_down_button.clicked.connect(lambda: self.move_down_requested.emit(self))
        self.add_button.clicked.connect(lambda: self.add_after_requested.emit(self))
        self.delete_button.clicked.connect(lambda: self.delete_requested.emit(self))

    def section(self) -> Section:
        return Section(self.minutes.value(), self.name.text().strip())
