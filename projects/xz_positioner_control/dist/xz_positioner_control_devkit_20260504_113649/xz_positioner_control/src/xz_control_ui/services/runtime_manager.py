from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from xz_control_ui.services.adapter_factory import build_adapters_from_activation
from xz_control_ui.services.adapters import AdapterBundle


@dataclass(slots=True)
class RuntimeStatus:
    mode: str
    connected: bool
    detail: str


class RuntimeManager:
    def __init__(self, activation_path: Path) -> None:
        self.activation_path = activation_path
        self.bundle: AdapterBundle | None = None
        self.mode = "DEMO"

    def set_mode(self, mode: str, use_mock_vna: bool = True) -> RuntimeStatus:
        self.mode = mode.upper()
        if self.mode == "DEMO":
            self.bundle = None
            return RuntimeStatus(mode=self.mode, connected=True, detail="Demo mode active")

        try:
            self.bundle = build_adapters_from_activation(self.activation_path, use_mock_vna=use_mock_vna)
            c_ok = self.bundle.controller.connect()
            v_ok = self.bundle.vna.connect()
            connected = bool(c_ok and v_ok)
            return RuntimeStatus(
                mode=self.mode,
                connected=connected,
                detail="Hardware adapters loaded" if connected else "Adapter connect failed",
            )
        except Exception as exc:
            self.bundle = None
            return RuntimeStatus(mode=self.mode, connected=False, detail=f"Adapter error: {exc}")

    def dry_run(self) -> RuntimeStatus:
        if self.bundle is None:
            return RuntimeStatus(mode=self.mode, connected=False, detail="No hardware bundle loaded")

        try:
            x = self.bundle.controller.read_axis("x")
            self.bundle.ttl.pulse_trigger()
            inputs = self.bundle.ttl.read_inputs()
            _ = self.bundle.vna.acquire_trace_db()
            detail = f"X={x.position_mm:.2f}mm, TTL inputs keys={len(inputs)}"
            return RuntimeStatus(mode=self.mode, connected=True, detail=detail)
        except Exception as exc:
            return RuntimeStatus(mode=self.mode, connected=False, detail=f"Dry-run failed: {exc}")

    def component_status(self) -> dict[str, bool]:
        if self.bundle is None:
            return {"controller": False, "vna": False, "ttl": False}

        controller_ok = False
        vna_ok = False
        ttl_ok = False
        try:
            controller_ok = bool(self.bundle.controller.connect())
        except Exception:
            controller_ok = False
        try:
            vna_ok = bool(self.bundle.vna.connect())
        except Exception:
            vna_ok = False
        try:
            _ = self.bundle.ttl.read_inputs()
            ttl_ok = True
        except Exception:
            ttl_ok = False
        return {"controller": controller_ok, "vna": vna_ok, "ttl": ttl_ok}
