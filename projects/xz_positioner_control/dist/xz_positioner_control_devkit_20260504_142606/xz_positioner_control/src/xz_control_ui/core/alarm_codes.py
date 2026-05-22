from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AlarmCode:
    code: str
    level: str
    message: str


ESTOP_LATCHED = AlarmCode("ALM-ESTOP-001", "CRITICAL", "Emergency stop latched")
LIMIT_ACTIVE = AlarmCode("ALM-LIMIT-001", "WARN", "Axis limit switch active")
WATCHDOG_TIMEOUT = AlarmCode("ALM-WDG-001", "CRITICAL", "Controller heartbeat timeout")
SCPI_TIMEOUT = AlarmCode("ALM-SCPI-001", "ERROR", "SCPI communication timeout/retry exhausted")
