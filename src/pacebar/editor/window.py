"""The setup window: a toolbar plus one editable row per section."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from ..constants import (
    APP_DISPLAY_NAME,
    DEFAULT_YELLOW_PERCENT,
    DEFAULT_YELLOW_SECONDS,
    MAX_LATENESS_MINUTES,
    MAX_YELLOW_PERCENT,
    MAX_YELLOW_SECONDS,
)
from ..persistence import load_sections
from .row import RowWidget

_WINDOW_DEFAULT_SIZE = (560, 440)
_SECONDS_PER_MINUTE = 60


class EditorWindow(QWidget):
    """Top-level setup window."""

    # sections, lateness_seconds, yellow_percent, yellow_seconds
    start_requested = Signal(object, int, int, int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_DISPLAY_NAME)
        self.rows: list[RowWidget] = []

        root_layout = QVBoxLayout(self)
        root_layout.addLayout(self._build_toolbar())
        root_layout.addWidget(self._build_rows_area(), 1)

        self._load_initial_rows()
        self.resize(*_WINDOW_DEFAULT_SIZE)

    # --- construction ---------------------------------------------------

    def _build_toolbar(self) -> QHBoxLayout:
        toolbar = QHBoxLayout()

        self.start_button = QPushButton("▶ Start")
        self.start_button.clicked.connect(self._on_start)
        self.lateness = QSpinBox()
        self.lateness.setRange(0, MAX_LATENESS_MINUTES)
        self.lateness.setSuffix(" min late")
        self.reset_button = QPushButton("⟳ Reset")
        self.reset_button.clicked.connect(self.reset)

        toolbar.addWidget(self.start_button)
        toolbar.addWidget(self.lateness)
        toolbar.addWidget(self.reset_button)
        toolbar.addStretch(1)

        toolbar.addWidget(QLabel("Yellow at"))
        self.yellow_percent = QSpinBox()
        self.yellow_percent.setRange(0, MAX_YELLOW_PERCENT)
        self.yellow_percent.setValue(DEFAULT_YELLOW_PERCENT)
        self.yellow_percent.setSuffix(" %")
        self.yellow_seconds = QSpinBox()
        self.yellow_seconds.setRange(0, MAX_YELLOW_SECONDS)
        self.yellow_seconds.setValue(DEFAULT_YELLOW_SECONDS)
        self.yellow_seconds.setSuffix(" s")
        toolbar.addWidget(self.yellow_percent)
        toolbar.addWidget(QLabel("or"))
        toolbar.addWidget(self.yellow_seconds)
        return toolbar

    def _build_rows_area(self) -> QScrollArea:
        self.rows_container = QWidget()
        self.rows_layout = QVBoxLayout(self.rows_container)
        self.rows_layout.setContentsMargins(0, 0, 0, 0)
        self.rows_layout.setSpacing(4)
        self.rows_layout.addStretch(1)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.rows_container)
        scroll_area.setFrameShape(QFrame.NoFrame)
        return scroll_area

    # --- row management -------------------------------------------------

    def _make_row(self, minutes: int, name: str) -> RowWidget:
        row = RowWidget(minutes, name)
        row.add_after_requested.connect(self._add_after)
        row.delete_requested.connect(self._delete)
        row.move_up_requested.connect(self._move_up)
        row.move_down_requested.connect(self._move_down)
        row.focus_up_requested.connect(self._focus_up)
        row.focus_down_requested.connect(self._focus_down)
        return row

    def _insert_row(self, index: int, minutes: int = 1, name: str = "") -> RowWidget:
        row = self._make_row(minutes, name)
        self.rows.insert(index, row)
        self.rows_layout.insertWidget(index, row)  # trailing stretch stays last
        return row

    def _add_after(self, row: RowWidget):
        index = self.rows.index(row) + 1
        new_row = self._insert_row(index)
        new_row.minutes.setFocus()

    def _delete(self, row: RowWidget):
        self.rows.remove(row)
        row.setParent(None)
        row.deleteLater()
        if not self.rows:
            self._insert_row(0)

    def _move_up(self, row: RowWidget):
        index = self.rows.index(row)
        if index > 0:
            self._swap(index, index - 1)

    def _move_down(self, row: RowWidget):
        index = self.rows.index(row)
        if index < len(self.rows) - 1:
            self._swap(index, index + 1)

    def _swap(self, first: int, second: int):
        self.rows[first], self.rows[second] = self.rows[second], self.rows[first]
        for row in self.rows:
            self.rows_layout.removeWidget(row)
        for position, row in enumerate(self.rows):
            self.rows_layout.insertWidget(position, row)

    def _focus_up(self, row: RowWidget):
        index = self.rows.index(row)
        if index > 0:
            self.rows[index - 1].name.setFocus()

    def _focus_down(self, row: RowWidget):
        index = self.rows.index(row)
        if index < len(self.rows) - 1:
            self.rows[index + 1].name.setFocus()

    def _load_initial_rows(self):
        saved_sections = load_sections()
        if saved_sections:
            for section in saved_sections:
                self._insert_row(len(self.rows), section.minutes, section.name)
        else:
            self._insert_row(0)

    # --- actions --------------------------------------------------------

    def reset(self):
        for row in list(self.rows):
            row.setParent(None)
            row.deleteLater()
        self.rows.clear()
        self._insert_row(0)

    def _on_start(self):
        sections = [row.section() for row in self.rows]
        sections = [section for section in sections if section.name]
        if not sections:
            return
        lateness_seconds = self.lateness.value() * _SECONDS_PER_MINUTE
        self.start_requested.emit(
            sections,
            lateness_seconds,
            self.yellow_percent.value(),
            self.yellow_seconds.value(),
        )
