from __future__ import annotations

from pathlib import Path

from xz_control_ui.services.activation_config import ActivationConfig, load_activation_config
from xz_control_ui.services.adapters import AdapterBundle
from xz_control_ui.services.controller_adapters import (
    ControllerCommandMap,
    ControllerSerialAdapter,
    ControllerTcpAdapter,
)
from xz_control_ui.services.scpi_client import MockScpiTransport, ScpiConfig
from xz_control_ui.services.ttl_adapter import TtlDigitalIoAdapter
from xz_control_ui.services.vna_pyvisa_adapter import PyvisaScpiTransport, VnaPyvisaAdapter


def build_adapters_from_activation(config_path: Path, use_mock_vna: bool = True) -> AdapterBundle:
    cfg: ActivationConfig = load_activation_config(config_path)

    cmd_map = ControllerCommandMap()
    if cfg.controller_transport.upper() == "ETHERNET":
        controller = ControllerTcpAdapter(cfg.controller_target, cmd_map=cmd_map)
    else:
        controller = ControllerSerialAdapter(cfg.controller_target, cmd_map=cmd_map)

    if use_mock_vna:
        vna_transport = MockScpiTransport()
    else:
        # Example resource_name: TCPIP0::10.0.21.151::inst0::INSTR
        target = cfg.vna_target
        resource = target if "::" in target else f"TCPIP0::{target}::inst0::INSTR"
        vna_transport = PyvisaScpiTransport(resource_name=resource, cfg=ScpiConfig())

    vna = VnaPyvisaAdapter(vna_transport)
    ttl = TtlDigitalIoAdapter()

    return AdapterBundle(controller=controller, vna=vna, ttl=ttl)
