from dataclasses import dataclass, field


@dataclass(slots=True)
class AxisLimits:
    min_mm: float
    max_mm: float
    max_speed_mm_s: float


@dataclass(slots=True)
class SystemConfig:
    x_limits: AxisLimits = field(default_factory=lambda: AxisLimits(0.0, 4000.0, 400.0))
    z_limits: AxisLimits = field(default_factory=lambda: AxisLimits(0.0, 3000.0, 400.0))
    serial_port: str = "COM5"
    vna_ip: str = "10.0.21.151"
