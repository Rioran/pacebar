"""Load/save the last run as a deliberately simple JSON file."""

import json

from .paths import last_run_path
from .timing import Section


def save_sections(sections) -> None:
    """Persist sections in order. No lateness, no thresholds — kept minimal."""
    data = [{"minutes": int(section.minutes), "name": section.name} for section in sections]
    last_run_path().write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_sections():
    """Return the saved sections, or [] if the file is missing/unreadable."""
    path = last_run_path()
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return [Section(int(item["minutes"]), str(item["name"])) for item in data]
    except Exception:
        return []
