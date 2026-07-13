from io import StringIO

import pytest

from amka.notifier import notify_terminal


def test_visible_alarm_heading() -> None:
    stream = StringIO()

    notify_terminal(None, stream=stream)

    assert "ALARM" in stream.getvalue()


def test_label_included_when_provided() -> None:
    stream = StringIO()

    notify_terminal("Better demo", stream=stream)

    assert "Label: Better demo" in stream.getvalue()


def test_label_omitted_when_absent() -> None:
    stream = StringIO()

    notify_terminal(None, stream=stream)

    assert "Label:" not in stream.getvalue()


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
