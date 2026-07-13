from io import StringIO

import pytest

from amka.notifier import notify_terminal


class TtyStringIO(StringIO):
    def __init__(self, *, is_tty: bool) -> None:
        super().__init__()
        self._is_tty = is_tty

    def isatty(self) -> bool:
        return self._is_tty


def test_visible_alarm_heading() -> None:
    stream = StringIO()

    notify_terminal(None, stream=stream)

    assert "ALARM" in stream.getvalue()


def test_label_included_when_provided() -> None:
    stream = StringIO()

    notify_terminal("Better demo", stream=stream)

    assert "Better demo" in stream.getvalue()


def test_label_omitted_when_absent() -> None:
    stream = StringIO()

    notify_terminal(None, stream=stream)

    assert "Better demo" not in stream.getvalue()


def test_exactly_three_bells_by_default() -> None:
    stream = StringIO()

    notify_terminal(None, stream=stream)

    assert stream.getvalue().count("\a") == 3


def test_configurable_bounded_bell_count() -> None:
    stream = StringIO()

    notify_terminal(None, stream=stream, bell_count=1)

    assert stream.getvalue().count("\a") == 1


def test_negative_bell_count_rejected() -> None:
    with pytest.raises(ValueError, match="bell_count must be non-negative"):
        notify_terminal(None, stream=StringIO(), bell_count=-1)


def test_default_stream_resolved_at_call_time(monkeypatch) -> None:
    stream = StringIO()
    monkeypatch.setattr("sys.stdout", stream)

    notify_terminal(None)

    assert "ALARM" in stream.getvalue()


def test_banner_uses_matching_top_and_bottom_borders() -> None:
    stream = StringIO()

    notify_terminal("Better demo", stream=stream)

    lines = stream.getvalue().splitlines()
    assert lines[1] == lines[5]


def test_label_appears_inside_banner() -> None:
    stream = StringIO()

    notify_terminal("Better demo", stream=stream)

    assert "|Label: Better demo" in stream.getvalue()


def test_label_row_omitted_when_label_absent() -> None:
    stream = StringIO()

    notify_terminal(None, stream=stream)

    lines = stream.getvalue().splitlines()
    assert lines[4] == "\a\a\a"


def test_long_labels_are_truncated_to_maximum_banner_width() -> None:
    stream = StringIO()

    notify_terminal("x" * 80, stream=stream)

    label_line = stream.getvalue().splitlines()[4]
    assert len(label_line) == 62


def test_truncated_labels_end_with_ascii_ellipsis() -> None:
    stream = StringIO()

    notify_terminal("x" * 80, stream=stream)

    assert stream.getvalue().splitlines()[4].rstrip("|").endswith("...")


def test_default_non_tty_output_contains_no_ansi_escape_sequences() -> None:
    stream = TtyStringIO(is_tty=False)

    notify_terminal(None, stream=stream)

    assert "\033[" not in stream.getvalue()


def test_tty_output_uses_ansi_emphasis(monkeypatch) -> None:
    stream = TtyStringIO(is_tty=True)
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")

    notify_terminal(None, stream=stream)

    assert "\033[1;31mALARM\033[0m" in stream.getvalue()


def test_no_color_disables_ansi_emphasis(monkeypatch) -> None:
    stream = TtyStringIO(is_tty=True)
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setenv("TERM", "xterm-256color")

    notify_terminal(None, stream=stream)

    assert "\033[" not in stream.getvalue()


def test_term_dumb_disables_ansi_emphasis(monkeypatch) -> None:
    stream = TtyStringIO(is_tty=True)
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("TERM", "dumb")

    notify_terminal(None, stream=stream)

    assert "\033[" not in stream.getvalue()


def test_bell_count_zero_emits_no_bells() -> None:
    stream = StringIO()

    notify_terminal(None, stream=stream, bell_count=0)

    assert stream.getvalue().count("\a") == 0
