from __future__ import annotations

from dataclasses import dataclass
from math import sin

from xz_control_ui.services.scpi_client import ScpiClient, ScpiConfig, ScpiTransport


class PyvisaScpiTransport(ScpiTransport):
    def __init__(self, resource_name: str, cfg: ScpiConfig | None = None) -> None:
        self.resource_name = resource_name
        self.cfg = cfg or ScpiConfig()
        self._inst = None

    def connect(self) -> bool:
        import pyvisa  # lazy import for environments without VISA runtime

        rm = pyvisa.ResourceManager()
        self._inst = rm.open_resource(self.resource_name)
        self._inst.timeout = self.cfg.timeout_ms
        self._inst.read_termination = self.cfg.read_termination
        self._inst.write_termination = self.cfg.write_termination
        return True

    def write(self, command: str) -> None:
        if self._inst is None:
            raise RuntimeError("VISA transport not connected")
        self._inst.write(command)

    def query(self, command: str) -> str:
        if self._inst is None:
            raise RuntimeError("VISA transport not connected")
        return str(self._inst.query(command)).strip()

    def close(self) -> None:
        if self._inst is not None:
            self._inst.close()
            self._inst = None


@dataclass(slots=True)
class VnaSweepConfig:
    start_ghz: float = 16.0
    stop_ghz: float = 26.0
    points: int = 101


class VnaPyvisaAdapter:
    def __init__(self, transport: ScpiTransport) -> None:
        self.transport = transport
        self.scpi = ScpiClient(transport)
        self.sweep = VnaSweepConfig()

    def connect(self) -> bool:
        connect_fn = getattr(self.transport, "connect", None)
        if callable(connect_fn):
            return bool(connect_fn())
        return True

    def configure_s21(self, start_ghz: float, stop_ghz: float, points: int) -> None:
        self.sweep = VnaSweepConfig(start_ghz=start_ghz, stop_ghz=stop_ghz, points=points)
        self.scpi.write(f"SENS:FREQ:STAR {start_ghz}GHZ")
        self.scpi.write(f"SENS:FREQ:STOP {stop_ghz}GHZ")
        self.scpi.write(f"SENS:SWE:POIN {points}")
        self.scpi.write("CALC:PAR:DEF 'Trc1','S21'")

    def acquire_trace_db(self) -> list[float]:
        # Skeleton: real firmware response parsing ICD/SCPI document ile netlestirilecek.
        start = self.sweep.start_ghz
        stop = self.sweep.stop_ghz
        pts = max(2, self.sweep.points)
        span = stop - start
        vals: list[float] = []
        for i in range(pts):
            x = start + (span * i / (pts - 1))
            vals.append(-20.0 + 12.0 * sin((x - start) / max(0.01, span) * 3.14159))
        return vals
