from xz_control_ui.services.scpi_client import MockScpiTransport, ScpiClient


def test_scpi_opc_and_idn() -> None:
    tr = MockScpiTransport()
    cli = ScpiClient(tr)
    idn = cli.query("*IDN?")
    assert "ZNA" in idn

    cli.write("INIT:IMM", wait_opc=True)
    assert tr.commands[-1] == "*OPC?"
