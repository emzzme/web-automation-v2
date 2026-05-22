from __future__ import annotations

import math
import random
from dataclasses import dataclass

from xz_control_ui.core.alarm_codes import ESTOP_LATCHED, LIMIT_ACTIVE, WATCHDOG_TIMEOUT
from xz_control_ui.core.models import AxisState, ScanProgress, ScanRecipe
from xz_control_ui.core.safety import SafetyController, SafetyInputs, SafetyState
from xz_control_ui.services.command_queue import CommandQueue
from xz_control_ui.services.watchdog import Watchdog


@dataclass(slots=True)
class Telemetry:
    x_axis: AxisState
    z_axis: AxisState
    s21_trace_db: list[float]
    s21_time_db: list[float]
    heatmap_db: list[list[float]]
    alarms: list[str]
    mode: str
    ttl_count: int
    progress: ScanProgress
    safety_state: str


class DemoSystem:
    def __init__(self) -> None:
        self.x = AxisState(position_mm=0.0, target_mm=0.0, speed_mm_s=150.0, moving=False)
        self.z = AxisState(position_mm=0.0, target_mm=0.0, speed_mm_s=150.0, moving=False)
        self.mode = "READY"
        self.alarms: list[str] = []
        self.ttl_count = 0
        self.recipe = ScanRecipe()
        self.safety = SafetyController()
        self.safety_inputs = SafetyInputs()
        self.queue = CommandQueue()
        self.watchdog = Watchdog(timeout_s=3.0)
        self.scan_points: list[tuple[float, float]] = []
        self.scan_active = False
        self.scan_paused = False
        self.scan_index = 0
        self.trace_freq_ghz = [16.0 + i * 0.1 for i in range(101)]
        self.vna_model = "R&S ZNL14"
        self.vna_start_ghz = 16.0
        self.vna_stop_ghz = 26.0
        self.vna_points = 101
        self.vna_ifbw_hz = 1000.0
        self.vna_power_dbm = -10.0
        self.time_axis = list(range(-60, 1))
        self.time_values = [-25.0 + random.uniform(-0.4, 0.4) for _ in self.time_axis]

    def set_vna_settings(
        self,
        model: str,
        start_ghz: float,
        stop_ghz: float,
        points: int,
        ifbw_hz: float,
        power_dbm: float,
    ) -> None:
        model = model.strip() or "R&S ZNL14"
        limits = {
            "R&S ZNL14": (0.005, 14.0, 1.0, 500000.0, -40.0, 10.0),
            "Keysight N9917B": (0.03, 18.0, 10.0, 100000.0, -40.0, 8.0),
        }
        fmin, fmax, ifbw_min, ifbw_max, pmin, pmax = limits.get(model, limits["R&S ZNL14"])

        s = max(fmin, min(start_ghz, fmax))
        e = max(fmin, min(stop_ghz, fmax))
        if e <= s:
            e = min(fmax, s + 0.1)
        n = max(11, min(points, 4001))
        bw = max(ifbw_min, min(ifbw_hz, ifbw_max))
        pwr = max(pmin, min(power_dbm, pmax))

        self.vna_model = model
        self.vna_start_ghz = s
        self.vna_stop_ghz = e
        self.vna_points = n
        self.vna_ifbw_hz = bw
        self.vna_power_dbm = pwr
        step = (self.vna_stop_ghz - self.vna_start_ghz) / (self.vna_points - 1)
        self.trace_freq_ghz = [self.vna_start_ghz + i * step for i in range(self.vna_points)]

    def set_speed(self, axis: str, speed_mm_s: float) -> None:
        speed_mm_s = max(10.0, min(speed_mm_s, 400.0))
        if axis == "x":
            self.x.speed_mm_s = speed_mm_s
        else:
            self.z.speed_mm_s = speed_mm_s
        self.watchdog.beat()

    def move_abs(self, axis: str, target_mm: float) -> None:
        if not self.safety.can_motion_start():
            self.mode = "SAFE_LOCK"
            return
        if axis == "x":
            self.x.target_mm = target_mm
            self.x.moving = True
        else:
            self.z.target_mm = target_mm
            self.z.moving = True
        self.mode = "MOVING"
        self.watchdog.beat()

    def jog(self, axis: str, delta_mm: float) -> None:
        if axis == "x":
            self.move_abs("x", self.x.target_mm + delta_mm)
        else:
            self.move_abs("z", self.z.target_mm + delta_mm)

    def stop(self) -> None:
        self.x.target_mm = self.x.position_mm
        self.z.target_mm = self.z.position_mm
        self.x.moving = False
        self.z.moving = False
        self.scan_active = False
        self.scan_paused = False
        self.mode = "STOPPED"
        self.watchdog.beat()

    def estop_press(self) -> None:
        self.safety_inputs.estop_pressed = True
        self.safety.update(self.safety_inputs)
        self.stop()
        self.mode = "ESTOP_LATCHED"
        self._append_alarm(ESTOP_LATCHED.message)

    def estop_reset(self) -> None:
        self.safety_inputs.estop_pressed = False
        if self.safety.manual_reset(self.safety_inputs):
            self.mode = "READY"

    def set_limit_state(self, x_limit: bool, z_limit: bool) -> None:
        self.safety_inputs.x_limit = x_limit
        self.safety_inputs.z_limit = z_limit
        state = self.safety.update(self.safety_inputs)
        if state in (SafetyState.LIMIT_ACTIVE, SafetyState.ESTOP_LATCHED):
            self.stop()
            self.mode = state.value
            self._append_alarm(LIMIT_ACTIVE.message)

    def home(self) -> None:
        self.enqueue("home_x", lambda: self.move_abs("x", 0.0))
        self.enqueue("home_z", lambda: self.move_abs("z", 0.0))

    def park(self) -> None:
        self.enqueue("park_x", lambda: self.move_abs("x", 100.0))
        self.enqueue("park_z", lambda: self.move_abs("z", 100.0))

    def apply_recipe(self, recipe: ScanRecipe) -> None:
        self.recipe = recipe
        self.scan_points = self._build_points(recipe)
        self.scan_index = 0
        self.watchdog.beat()

    def enqueue(self, name: str, fn) -> None:
        self.queue.push(name=name, fn=fn)

    def start_scan(self) -> None:
        if not self.safety.can_motion_start():
            self.mode = "SAFE_LOCK"
            return
        self.scan_points = self._build_points(self.recipe)
        self.scan_active = True
        self.scan_paused = False
        self.scan_index = 0
        self.mode = "SCANNING"
        if self.scan_points:
            tx, tz = self.scan_points[0]
            self.move_abs("x", tx)
            self.move_abs("z", tz)

    def pause_scan(self) -> None:
        if self.scan_active:
            self.scan_paused = True
            self.mode = "PAUSED"

    def resume_scan(self) -> None:
        if self.scan_active and self.scan_paused:
            self.scan_paused = False
            self.mode = "SCANNING"

    def abort_scan(self) -> None:
        self.scan_active = False
        self.scan_paused = False
        self.mode = "ABORTED"

    def tick(self, dt_s: float = 0.25) -> Telemetry:
        _ = self.queue.run_next()
        s = self.safety.update(self.safety_inputs)
        if s in (SafetyState.LIMIT_ACTIVE, SafetyState.ESTOP_LATCHED):
            self.stop()
            self.mode = s.value
        if self.watchdog.is_timed_out():
            self.mode = "FAULT"
            self._append_alarm(WATCHDOG_TIMEOUT.message)
            self.watchdog.beat()

        self._tick_axis(self.x, dt_s)
        self._tick_axis(self.z, dt_s)

        if self.scan_active and not self.scan_paused:
            self._tick_scan()

        trace = self._trace()
        self.time_values = self.time_values[1:] + [self.time_values[-1] + random.uniform(-0.6, 0.6)]
        heatmap = self._heatmap()

        progress = ScanProgress(
            total_points=max(len(self.scan_points), 1),
            completed_points=self.scan_index,
            current_index=self.scan_index,
            state=self.mode,
        )
        return Telemetry(
            x_axis=self.x,
            z_axis=self.z,
            s21_trace_db=trace,
            s21_time_db=self.time_values,
            heatmap_db=heatmap,
            alarms=list(self.alarms),
            mode=self.mode,
            ttl_count=self.ttl_count,
            progress=progress,
            safety_state=self.safety.state.value,
        )

    def _append_alarm(self, msg: str) -> None:
        if not self.alarms or self.alarms[-1] != msg:
            self.alarms.append(msg)
            self.alarms = self.alarms[-50:]

    def _tick_axis(self, axis: AxisState, dt_s: float) -> None:
        diff = axis.target_mm - axis.position_mm
        if abs(diff) < 0.5:
            axis.position_mm = axis.target_mm
            axis.moving = False
            return

        axis.moving = True
        step = axis.speed_mm_s * dt_s
        if abs(diff) <= step:
            axis.position_mm = axis.target_mm
            axis.moving = False
        else:
            axis.position_mm += step if diff > 0 else -step

    def _tick_scan(self) -> None:
        if self.scan_index >= len(self.scan_points):
            self.scan_active = False
            self.mode = "READY"
            return

        tx, tz = self.scan_points[self.scan_index]

        x_done = (not self.x.moving) and abs(self.x.position_mm - tx) < 0.5
        z_done = (not self.z.moving) and abs(self.z.position_mm - tz) < 0.5
        if x_done and z_done:
            self.ttl_count += 1
            self.scan_index += 1
            if self.scan_index >= len(self.scan_points):
                self.scan_active = False
                self.mode = "READY"
                return
            tx, tz = self.scan_points[self.scan_index]

        if abs(self.x.target_mm - tx) >= 0.5:
            self.move_abs("x", tx)
        if abs(self.z.target_mm - tz) >= 0.5:
            self.move_abs("z", tz)

    def _build_points(self, recipe: ScanRecipe) -> list[tuple[float, float]]:
        x_vals = self._axis_points(recipe.x_start_mm, recipe.x_stop_mm, recipe.x_step_mm)
        z_vals = self._axis_points(recipe.z_start_mm, recipe.z_stop_mm, recipe.z_step_mm)

        points: list[tuple[float, float]] = []
        for i, z in enumerate(z_vals):
            row = x_vals if (i % 2 == 0 or not recipe.snaking) else list(reversed(x_vals))
            for x in row:
                points.append((x, z))
        return points

    @staticmethod
    def _axis_points(start_mm: float, stop_mm: float, step_mm: float) -> list[float]:
        if step_mm <= 0:
            return [start_mm]
        count = int(max(1, math.floor((stop_mm - start_mm) / step_mm) + 1))
        return [start_mm + i * step_mm for i in range(count)]

    def _trace(self) -> list[float]:
        vals: list[float] = []
        center = (self.vna_start_ghz + self.vna_stop_ghz) / 2.0
        span = max(0.2, self.vna_stop_ghz - self.vna_start_ghz)
        for f in self.trace_freq_ghz:
            peak = -8.0 - abs(f - center) * (8.0 / span)
            vals.append(peak + random.uniform(-1.1, 1.1))
        return vals

    def _heatmap(self) -> list[list[float]]:
        size = 41
        out: list[list[float]] = []
        x_shift = (self.x.position_mm / 1000.0) % 5.0
        z_shift = (self.z.position_mm / 1000.0) % 5.0
        for zi in range(size):
            row: list[float] = []
            for xi in range(size):
                d = ((xi - 20 - x_shift) ** 2 + (zi - 20 - z_shift) ** 2) ** 0.5
                row.append(35.0 - d * 2.2 + random.uniform(-1.3, 1.3))
            out.append(row)
        return out
