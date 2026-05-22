from __future__ import annotations

import time


class Watchdog:
    def __init__(self, timeout_s: float = 2.0) -> None:
        self.timeout_s = timeout_s
        self._last_beat = time.monotonic()

    def beat(self) -> None:
        self._last_beat = time.monotonic()

    def is_timed_out(self) -> bool:
        return (time.monotonic() - self._last_beat) > self.timeout_s
