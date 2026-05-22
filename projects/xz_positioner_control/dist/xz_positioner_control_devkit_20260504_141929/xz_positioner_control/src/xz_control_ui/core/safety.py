from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SafetyState(str, Enum):
    READY = "READY"
    ESTOP_LATCHED = "ESTOP_LATCHED"
    LIMIT_ACTIVE = "LIMIT_ACTIVE"
    FAULT = "FAULT"


@dataclass(slots=True)
class SafetyInputs:
    estop_pressed: bool = False
    x_limit: bool = False
    z_limit: bool = False


class SafetyController:
    def __init__(self) -> None:
        self.state = SafetyState.READY
        self._manual_reset_required = False

    def update(self, inputs: SafetyInputs) -> SafetyState:
        if inputs.estop_pressed:
            self.state = SafetyState.ESTOP_LATCHED
            self._manual_reset_required = True
            return self.state

        if inputs.x_limit or inputs.z_limit:
            if self.state != SafetyState.ESTOP_LATCHED:
                self.state = SafetyState.LIMIT_ACTIVE
            return self.state

        if self.state == SafetyState.LIMIT_ACTIVE:
            self.state = SafetyState.READY

        return self.state

    def can_motion_start(self) -> bool:
        return self.state == SafetyState.READY and not self._manual_reset_required

    def manual_reset(self, inputs: SafetyInputs) -> bool:
        if inputs.estop_pressed:
            return False
        self._manual_reset_required = False
        if self.state == SafetyState.ESTOP_LATCHED:
            self.state = SafetyState.READY
        return True
