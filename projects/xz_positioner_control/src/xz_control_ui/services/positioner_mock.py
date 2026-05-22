from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AxisState:
    x_mm: float
    z_mm: float
    moving: bool


class MockPositioner:
    def __init__(self) -> None:
        self._x = 4.05
        self._z = 22.799

    def read_state(self) -> AxisState:
        return AxisState(x_mm=self._x, z_mm=self._z, moving=False)

    def jog(self, axis: str, delta_mm: float) -> AxisState:
        if axis == "x":
            self._x += delta_mm
        elif axis == "z":
            self._z += delta_mm
        return self.read_state()
