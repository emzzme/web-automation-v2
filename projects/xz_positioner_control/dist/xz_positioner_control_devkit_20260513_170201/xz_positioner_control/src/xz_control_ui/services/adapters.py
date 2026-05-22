from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from xz_control_ui.core.models import AxisState


class ControllerAdapter(Protocol):
    def connect(self) -> bool: ...
    def move_abs(self, axis: str, target_mm: float) -> None: ...
    def stop(self) -> None: ...
    def read_axis(self, axis: str) -> AxisState: ...


class VnaAdapter(Protocol):
    def connect(self) -> bool: ...
    def configure_s21(self, start_ghz: float, stop_ghz: float, points: int) -> None: ...
    def acquire_trace_db(self) -> list[float]: ...


class TtlAdapter(Protocol):
    def pulse_trigger(self) -> None: ...
    def read_inputs(self) -> dict[str, bool]: ...


@dataclass(slots=True)
class AdapterBundle:
    controller: ControllerAdapter
    vna: VnaAdapter
    ttl: TtlAdapter
