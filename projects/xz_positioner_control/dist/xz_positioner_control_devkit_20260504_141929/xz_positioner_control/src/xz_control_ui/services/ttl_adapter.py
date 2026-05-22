from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TtlPinMap:
    trigger_out_pin: str = "DO0"
    estop_in_pin: str = "DI0"
    x_limit_in_pin: str = "DI1"
    z_limit_in_pin: str = "DI2"


class TtlDigitalIoAdapter:
    def __init__(self, pin_map: TtlPinMap | None = None) -> None:
        self.pin_map = pin_map or TtlPinMap()
        self.trigger_count = 0
        self.inputs = {
            "estop_chain": False,
            "x_limit": False,
            "z_limit": False,
            "x_home": False,
            "z_home": False,
        }

    def pulse_trigger(self) -> None:
        self.trigger_count += 1

    def read_inputs(self) -> dict[str, bool]:
        return dict(self.inputs)

    def set_input(self, name: str, value: bool) -> None:
        if name in self.inputs:
            self.inputs[name] = value
