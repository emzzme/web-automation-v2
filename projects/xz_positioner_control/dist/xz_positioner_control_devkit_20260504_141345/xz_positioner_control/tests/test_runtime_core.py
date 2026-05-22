import time

from xz_control_ui.services.command_queue import CommandQueue
from xz_control_ui.services.watchdog import Watchdog


def test_command_queue_runs_in_order() -> None:
    q = CommandQueue()
    out: list[str] = []
    q.push("a", lambda: out.append("a"))
    q.push("b", lambda: out.append("b"))
    assert q.run_next() == "a"
    assert q.run_next() == "b"
    assert out == ["a", "b"]


def test_watchdog_timeout() -> None:
    w = Watchdog(timeout_s=0.01)
    time.sleep(0.02)
    assert w.is_timed_out()
    w.beat()
    assert not w.is_timed_out()
