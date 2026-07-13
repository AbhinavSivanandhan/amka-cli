from datetime import UTC, datetime

from typer.testing import CliRunner

import amka.cli
from amka.cli import app

runner = CliRunner()


class FixedDateTime(datetime):
    @classmethod
    def now(cls) -> "FixedDateTime":
        return cls(2026, 1, 1, 7, 0, tzinfo=UTC)

    def astimezone(self, tz: object = None) -> "FixedDateTime":
        return self


def test_help_exits_successfully() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Create and manage local alarms" in result.output


def test_version_prints_package_version() -> None:
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert result.output == "amka 0.1.0\n"


def test_version_option_prints_package_version() -> None:
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.output == "amka 0.1.0\n"


def test_set_relative_alarm_succeeds_without_real_waiting(monkeypatch) -> None:
    waits: list[object] = []
    notifications: list[str | None] = []

    monkeypatch.setattr(amka.cli, "wait_until", waits.append)
    monkeypatch.setattr(
        amka.cli,
        "notify_terminal",
        lambda label, bell_count=3: notifications.append(label),
    )

    result = runner.invoke(app, ["set", "--in", "5s"])

    assert result.exit_code == 0
    assert waits
    assert notifications == [None]
    assert "Alarm scheduled for" in result.output
    assert "(in 5s)" in result.output


def test_set_relative_alarm_includes_label_in_confirmation_and_notification(monkeypatch) -> None:
    notifications: list[str | None] = []

    monkeypatch.setattr(amka.cli, "wait_until", lambda _target: None)
    monkeypatch.setattr(
        amka.cli,
        "notify_terminal",
        lambda label, bell_count=3: notifications.append(label),
    )

    result = runner.invoke(app, ["set", "--in", "5s", "--label", "Better demo"])

    assert result.exit_code == 0
    assert "Label: Better demo" in result.output
    assert notifications == ["Better demo"]


def test_invalid_duration_exits_non_zero_without_traceback(monkeypatch) -> None:
    monkeypatch.setattr(amka.cli, "wait_until", lambda _target: None)
    monkeypatch.setattr(amka.cli, "notify_terminal", lambda _label: None)

    result = runner.invoke(app, ["set", "--in", "bad"])

    assert result.exit_code != 0
    assert "Error:" in result.stderr
    assert "Traceback" not in result.output
    assert "Traceback" not in result.stderr


def test_invalid_duration_exits_one_and_uses_stderr(monkeypatch) -> None:
    monkeypatch.setattr(amka.cli, "wait_until", lambda _target: None)
    monkeypatch.setattr(amka.cli, "notify_terminal", lambda _label, bell_count=3: None)

    result = runner.invoke(app, ["set", "--in", "bad"])

    assert result.exit_code == 1
    assert "Error:" in result.stderr
    assert "Error:" not in result.stdout


def test_unknown_option_exits_two_without_traceback() -> None:
    result = runner.invoke(app, ["set", "--unknown"])

    assert result.exit_code == 2
    assert "Traceback" not in result.output
    assert "Traceback" not in result.stderr


def test_keyboard_interrupt_cancels_alarm(monkeypatch) -> None:
    def interrupt(_target: object) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr(amka.cli, "wait_until", interrupt)
    monkeypatch.setattr(amka.cli, "notify_terminal", lambda _label, bell_count=3: None)

    result = runner.invoke(app, ["set", "--in", "5s"])

    assert result.exit_code == 130
    assert "Alarm cancelled." in result.stderr


def test_set_absolute_alarm_succeeds_without_real_waiting(monkeypatch) -> None:
    waits: list[object] = []
    notifications: list[str | None] = []

    monkeypatch.setattr(amka.cli, "datetime", FixedDateTime)
    monkeypatch.setattr(amka.cli, "wait_until", waits.append)
    monkeypatch.setattr(
        amka.cli,
        "notify_terminal",
        lambda label, bell_count=3: notifications.append(label),
    )

    result = runner.invoke(app, ["set", "--at", "07:30"])

    assert result.exit_code == 0
    assert waits == [datetime(2026, 1, 1, 7, 30, tzinfo=UTC)]
    assert notifications == [None]
    assert "(at 07:30)" in result.output


def test_absolute_confirmation_contains_resolved_date_and_time(monkeypatch) -> None:
    monkeypatch.setattr(amka.cli, "datetime", FixedDateTime)
    monkeypatch.setattr(amka.cli, "wait_until", lambda _target: None)
    monkeypatch.setattr(amka.cli, "notify_terminal", lambda _label, bell_count=3: None)

    result = runner.invoke(app, ["set", "--at", "07:30"])

    assert result.exit_code == 0
    assert "2026-01-01 07:30:00" in result.output
    assert "UTC" in result.output


def test_absolute_label_reaches_confirmation_and_notification(monkeypatch) -> None:
    notifications: list[str | None] = []

    monkeypatch.setattr(amka.cli, "datetime", FixedDateTime)
    monkeypatch.setattr(amka.cli, "wait_until", lambda _target: None)
    monkeypatch.setattr(
        amka.cli,
        "notify_terminal",
        lambda label, bell_count=3: notifications.append(label),
    )

    result = runner.invoke(app, ["set", "--at", "07:30", "--label", "Wake up"])

    assert result.exit_code == 0
    assert "Label: Wake up" in result.output
    assert notifications == ["Wake up"]


def test_both_in_and_at_fail(monkeypatch) -> None:
    monkeypatch.setattr(amka.cli, "wait_until", lambda _target: None)
    monkeypatch.setattr(amka.cli, "notify_terminal", lambda _label, bell_count=3: None)

    result = runner.invoke(app, ["set", "--in", "5s", "--at", "07:30"])

    assert result.exit_code != 0
    assert "Use only one of --in or --at." in result.stderr


def test_neither_in_nor_at_fails(monkeypatch) -> None:
    monkeypatch.setattr(amka.cli, "wait_until", lambda _target: None)
    monkeypatch.setattr(amka.cli, "notify_terminal", lambda _label, bell_count=3: None)

    result = runner.invoke(app, ["set"])

    assert result.exit_code != 0
    assert "Provide exactly one of --in or --at." in result.stderr


def test_invalid_at_exits_non_zero_without_traceback(monkeypatch) -> None:
    monkeypatch.setattr(amka.cli, "datetime", FixedDateTime)
    monkeypatch.setattr(amka.cli, "wait_until", lambda _target: None)
    monkeypatch.setattr(amka.cli, "notify_terminal", lambda _label, bell_count=3: None)

    result = runner.invoke(app, ["set", "--at", "7:30"])

    assert result.exit_code != 0
    assert "Error:" in result.stderr
    assert "Traceback" not in result.output
    assert "Traceback" not in result.stderr


def test_quiet_suppresses_scheduling_confirmation(monkeypatch) -> None:
    monkeypatch.setattr(amka.cli, "wait_until", lambda _target: None)

    result = runner.invoke(app, ["set", "--in", "5s", "--quiet"])

    assert result.exit_code == 0
    assert "Alarm scheduled for" not in result.output


def test_quiet_still_emits_alarm(monkeypatch) -> None:
    monkeypatch.setattr(amka.cli, "wait_until", lambda _target: None)

    result = runner.invoke(app, ["set", "--in", "5s", "--quiet"])

    assert result.exit_code == 0
    assert "ALARM" in result.output


def test_quiet_still_includes_final_label(monkeypatch) -> None:
    monkeypatch.setattr(amka.cli, "wait_until", lambda _target: None)

    result = runner.invoke(app, ["set", "--in", "5s", "--label", "Quiet demo", "--quiet"])

    assert result.exit_code == 0
    assert "Label: Quiet demo" in result.output


def test_no_bell_emits_zero_bell_characters(monkeypatch) -> None:
    monkeypatch.setattr(amka.cli, "wait_until", lambda _target: None)

    result = runner.invoke(app, ["set", "--in", "5s", "--no-bell"])

    assert result.exit_code == 0
    assert "ALARM" in result.output
    assert result.output.count("\a") == 0


def test_default_behavior_emits_three_bell_characters(monkeypatch) -> None:
    monkeypatch.setattr(amka.cli, "wait_until", lambda _target: None)

    result = runner.invoke(app, ["set", "--in", "5s"])

    assert result.exit_code == 0
    assert result.output.count("\a") == 3
