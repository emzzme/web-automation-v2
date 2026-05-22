from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass(slots=True)
class ScpiConfig:
    timeout_ms: int = 5000
    retries: int = 3
    retry_sleep_s: float = 0.2
    read_termination: str = "\n"
    write_termination: str = "\n"


class ScpiTransport:
    def write(self, command: str) -> None:  # pragma: no cover
        raise NotImplementedError

    def query(self, command: str) -> str:  # pragma: no cover
        raise NotImplementedError

    def close(self) -> None:  # pragma: no cover
        raise NotImplementedError


class ScpiClient:
    def __init__(self, transport: ScpiTransport, cfg: ScpiConfig | None = None) -> None:
        self.transport = transport
        self.cfg = cfg or ScpiConfig()

    def query(self, command: str) -> str:
        last_exc: Exception | None = None
        for _ in range(self.cfg.retries):
            try:
                return self.transport.query(command)
            except Exception as exc:
                last_exc = exc
                time.sleep(self.cfg.retry_sleep_s)
        raise RuntimeError(f"SCPI query failed: {command}") from last_exc

    def write(self, command: str, wait_opc: bool = False) -> None:
        last_exc: Exception | None = None
        for _ in range(self.cfg.retries):
            try:
                self.transport.write(command)
                if wait_opc:
                    _ = self.transport.query("*OPC?")
                return
            except Exception as exc:
                last_exc = exc
                time.sleep(self.cfg.retry_sleep_s)
        raise RuntimeError(f"SCPI write failed: {command}") from last_exc

    def close(self) -> None:
        self.transport.close()


class MockScpiTransport(ScpiTransport):
    def __init__(self) -> None:
        self.commands: list[str] = []

    def write(self, command: str) -> None:
        self.commands.append(command)

    def query(self, command: str) -> str:
        self.commands.append(command)
        if command == "*IDN?":
            return "Rohde&Schwarz,ZNA26,123456,FW3.20"
        if command == "*OPC?":
            return "1"
        return "0"

    def close(self) -> None:
        return
