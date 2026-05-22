from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AxisState:
    position_mm: float
    target_mm: float
    speed_mm_s: float
    moving: bool


@dataclass(slots=True)
class ScanRecipe:
    name: str = "Plane_XZ_Scan_5mm"
    x_start_mm: float = 0.0
    x_stop_mm: float = 4000.0
    x_step_mm: float = 100.0
    z_start_mm: float = 0.0
    z_stop_mm: float = 3000.0
    z_step_mm: float = 100.0
    snaking: bool = True


@dataclass(slots=True)
class SystemLimits:
    x_min_mm: float = 0.0
    x_max_mm: float = 4000.0
    z_min_mm: float = 0.0
    z_max_mm: float = 3000.0
    max_payload_kg: float = 5.0


@dataclass(slots=True)
class ScanProgress:
    total_points: int
    completed_points: int
    current_index: int
    state: str
