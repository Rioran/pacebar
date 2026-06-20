"""Application controller: wires the editor to a run, persists the run on start."""

from PySide6.QtWidgets import QApplication

from .editor import EditorWindow
from .overlay import RunController
from .persistence import save_sections


class App:
    def __init__(self):
        self.editor = EditorWindow()
        self.editor.start_requested.connect(self._start_run)
        self.run: RunController | None = None

    def show(self):
        self.editor.show()

    def _start_run(self, sections, lateness_seconds, yellow_percent, yellow_seconds):
        # Persist the schedule (order + minutes + names only) as the run begins.
        save_sections(sections)
        self.editor.hide()
        self.run = RunController(sections, lateness_seconds, yellow_percent, yellow_seconds)
        self.run.finished.connect(QApplication.instance().quit)
