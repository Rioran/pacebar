"""Filesystem locations for persisted state."""

import sys
from pathlib import Path

from .constants import LAST_RUN_FILENAME


def state_directory() -> Path:
    """Folder of the running exe, so each copy keeps its own typical schedule.

    When running from source there is no exe, so fall back to the current dir.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path.cwd()


def last_run_path() -> Path:
    return state_directory() / LAST_RUN_FILENAME
