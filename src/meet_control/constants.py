"""Constants shared across modules.

Purely cosmetic, single-use dimensions live next to the code that uses them;
this file holds values that are shared or worth tuning in one place.
"""

# Identity and storage
APP_DISPLAY_NAME = "Meet Control"
LAST_RUN_FILENAME = "tc_last_run.json"

# Section / editor limits and defaults
MIN_SECTION_MINUTES = 1
MAX_SECTION_MINUTES = 999
MAX_LATENESS_MINUTES = 999
MAX_SECTION_NAME_LENGTH = 30
MAX_YELLOW_PERCENT = 100
MAX_YELLOW_SECONDS = 3600
DEFAULT_YELLOW_PERCENT = 10
DEFAULT_YELLOW_SECONDS = 30

# Overlay rendering
RENDER_INTERVAL_MS = 100  # ~10 Hz; the smallest shown unit is one second
OVERLAY_FONT_POINT_INCREASE = 2
OVERLAY_HEIGHT_FACTOR = 1.6

# Pastel status colors for the strip and minimized square
PASTEL_GREEN = "#cfe8cf"
PASTEL_YELLOW = "#f6efb4"
PASTEL_RED = "#f2c4c4"
