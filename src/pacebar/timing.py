"""Pure timing model: stages, a global meeting clock and color state."""

from dataclasses import dataclass
from time import monotonic

GREEN = "green"
YELLOW = "yellow"
RED = "red"


@dataclass
class Section:
    minutes: int
    name: str

    @property
    def seconds(self) -> int:
        return self.minutes * 60


class TimerModel:
    """Drives the countdown using one global clock for the whole meeting.

    Two pieces of state are enough to place every stage on the same timeline:

    * ``_start`` — the monotonic instant the meeting began. It is shifted back by
      the initial lateness, so elapsed time starts at ``lateness`` and the first
      stage is already partway down (possibly negative).
    * ``_accumulated`` — the planned seconds of all *completed* stages.

    The remaining time of the current stage is therefore its planned cumulative
    end minus the real elapsed time. Switching stages never restarts the clock,
    so an overrun (or an early switch) carries straight over to the next stage.
    """

    def __init__(self, sections, lateness_seconds: int = 0):
        if not sections:
            raise ValueError("at least one section is required")
        self.sections = list(sections)
        self.index = 0
        self._start = monotonic() - lateness_seconds
        self._accumulated = 0.0

    @property
    def current(self) -> Section:
        return self.sections[self.index]

    @property
    def is_last(self) -> bool:
        return self.index >= len(self.sections) - 1

    @property
    def next_section(self):
        return None if self.is_last else self.sections[self.index + 1]

    def _elapsed(self) -> float:
        return monotonic() - self._start

    def remaining(self) -> float:
        # Planned cumulative end of the current stage, minus real elapsed time.
        return (self._accumulated + self.current.seconds) - self._elapsed()

    def advance(self) -> bool:
        """Move to the next stage. Returns False if already on the last one.

        The real clock keeps running: we only bank the current stage's *planned*
        duration, so any over/under-run rolls into the next stage automatically.
        """
        if self.is_last:
            return False
        self._accumulated += self.current.seconds
        self.index += 1
        return True

    def go_back(self) -> bool:
        """Roll back one stage — the exact inverse of advance().

        The global clock keeps running, so the previous stage resumes exactly
        where the timeline puts it: with the time it had left if you switched
        early, or already overdue if you had overrun it.
        """
        if self.index == 0:
            return False
        self.index -= 1
        self._accumulated -= self.current.seconds
        return True

    def color(self, yellow_percent: float, yellow_seconds: float) -> str:
        remaining = self.remaining()
        if remaining < 0:
            return RED
        # Yellow kicks in at whichever threshold is larger: percent or seconds.
        threshold = max(self.current.seconds * yellow_percent / 100.0, yellow_seconds)
        return YELLOW if remaining <= threshold else GREEN
