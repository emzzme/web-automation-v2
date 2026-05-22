from __future__ import annotations

from dataclasses import dataclass

from xz_control_ui.core.models import AxisState


@dataclass(slots=True)
class ControllerCommandMap:
    move_abs_template: str = "MOVE {axis} {target_mm:.3f}"
    stop_cmd: str = "STOP"
    read_axis_template: str = "READ {axis}"


class ControllerTcpAdapter:
    def __init__(self, host_port: str, cmd_map: ControllerCommandMap | None = None) -> None:
        self.host_port = host_port
        self.cmd_map = cmd_map or ControllerCommandMap()
        self.connected = False
        self._x = AxisState(position_mm=0.0, target_mm=0.0, speed_mm_s=100.0, moving=False)
        self._z = AxisState(position_mm=0.0, target_mm=0.0, speed_mm_s=100.0, moving=False)

    def connect(self) -> bool:
        self.connected = True
        return self.connected

    def move_abs(self, axis: str, target_mm: float) -> None:
        _ = self.cmd_map.move_abs_template.format(axis=axis.upper(), target_mm=target_mm)
        if axis.lower() == "x":
            self._x.target_mm = target_mm
            self._x.position_mm = target_mm
        else:
            self._z.target_mm = target_mm
            self._z.position_mm = target_mm

    def stop(self) -> None:
        _ = self.cmd_map.stop_cmd
        self._x.moving = False
        self._z.moving = False

    def read_axis(self, axis: str) -> AxisState:
        _ = self.cmd_map.read_axis_template.format(axis=axis.upper())
        return self._x if axis.lower() == "x" else self._z


class ControllerSerialAdapter(ControllerTcpAdapter):
    def __init__(self, com_port: str, cmd_map: ControllerCommandMap | None = None) -> None:
        super().__init__(host_port=com_port, cmd_map=cmd_map)
