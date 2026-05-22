from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Callable


@dataclass(slots=True)
class Command:
    name: str
    fn: Callable[[], None]


class CommandQueue:
    def __init__(self, maxlen: int = 200) -> None:
        self._q: deque[Command] = deque(maxlen=maxlen)
        self._busy = False

    def push(self, name: str, fn: Callable[[], None]) -> None:
        self._q.append(Command(name=name, fn=fn))

    def run_next(self) -> str | None:
        if self._busy or not self._q:
            return None
        self._busy = True
        cmd = self._q.popleft()
        try:
            cmd.fn()
            return cmd.name
        finally:
            self._busy = False

    def clear(self) -> None:
        self._q.clear()

    @property
    def length(self) -> int:
        return len(self._q)
