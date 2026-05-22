from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(slots=True)
class ActivationConfig:
    controller_transport: str
    controller_target: str
    vna_transport: str
    vna_target: str
    trigger_mode: str


def load_activation_config(path: Path) -> ActivationConfig:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return ActivationConfig(
        controller_transport=payload["controller_transport"],
        controller_target=payload["controller_target"],
        vna_transport=payload["vna_transport"],
        vna_target=payload["vna_target"],
        trigger_mode=payload["trigger_mode"],
    )
