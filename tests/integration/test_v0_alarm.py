from typer.testing import CliRunner

import amka.cli
from amka.cli import app

runner = CliRunner()


def test_v0_relative_alarm_flow(monkeypatch) -> None:
    monkeypatch.setattr(amka.cli, "wait_until", lambda _target: None)

    result = runner.invoke(app, ["set", "--in", "1s", "--label", "Integration demo"])

    assert result.exit_code == 0
    assert "Label: Integration demo" in result.output
    assert "in 1s" in result.output
    assert "ALARM" in result.output
    assert "Integration demo" in result.output
    assert result.output.count("\a") == 3
