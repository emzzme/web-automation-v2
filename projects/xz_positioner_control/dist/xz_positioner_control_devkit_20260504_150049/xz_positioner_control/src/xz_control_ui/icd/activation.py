from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(slots=True)
class RuntimeActivation:
    controller_transport: str
    controller_target: str
    vna_transport: str
    vna_target: str
    trigger_mode: str


def load_activation(path: Path) -> RuntimeActivation:
    data = json.loads(path.read_text(encoding="utf-8"))
    return RuntimeActivation(
        controller_transport=data["controller_transport"],
        controller_target=data["controller_target"],
        vna_transport=data["vna_transport"],
        vna_target=data["vna_target"],
        trigger_mode=data["trigger_mode"],
    )
