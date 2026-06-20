"""Entry point: `python -m meet_control` / the `meet-control` script / the exe."""

import sys

from PySide6.QtWidgets import QApplication

from .app import App
from .constants import APP_DISPLAY_NAME


def main() -> int:
    qt_application = QApplication(sys.argv)
    qt_application.setApplicationName(APP_DISPLAY_NAME)
    app = App()
    app.show()
    return qt_application.exec()


if __name__ == "__main__":
    sys.exit(main())
