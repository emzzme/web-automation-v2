from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from xz_control_ui.services.demo_system import DemoSystem


def main() -> int:
    s = DemoSystem()
    s.start_scan()
    for _ in range(120):
        t = s.tick(0.25)

    assert len(t.s21_trace_db) == 101
    assert len(t.heatmap_db) == 41
    assert len(t.heatmap_db[0]) == 41
    assert t.progress.total_points >= 1
    print("SMOKE OK", t.mode, t.progress.completed_points, t.progress.total_points)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
