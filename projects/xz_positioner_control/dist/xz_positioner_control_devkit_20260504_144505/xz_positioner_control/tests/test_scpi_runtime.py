from xz_control_ui.services.scpi_client import MockScpiTransport, ScpiClient


def test_scpi_write_wait_opc_path() -> None:
    tr = MockScpiTransport()
    c = ScpiClient(tr)
    c.write("INIT:IMM", wait_opc=True)
    assert "INIT:IMM" in tr.commands
    assert "*OPC?" in tr.commands
