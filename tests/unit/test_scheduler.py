from datetime import UTC, datetime, timedelta

import pytest

from amka.scheduler import wait_until


def test_positive_remaining_time_calls_sleep_once_with_correct_seconds() -> None:
    current = datetime(2026, 1, 1, 7, 30, tzinfo=UTC)
    target = current + timedelta(seconds=5)
    calls: list[float] = []

    wait_until(target, now=lambda: current, sleep=calls.append)

    assert calls == [5.0]


def test_already_due_target_does_not_call_sleep() -> None:
    current = datetime(2026, 1, 1, 7, 30, tzinfo=UTC)
    calls: list[float] = []

    wait_until(current, now=lambda: current, sleep=calls.append)

    assert calls == []


def test_naive_target_is_rejected() -> None:
    with pytest.raises(ValueError, match="target must be timezone-aware"):
        wait_until(datetime(2026, 1, 1, 7, 30))


def test_keyboard_interrupt_from_sleep_propagates() -> None:
    current = datetime(2026, 1, 1, 7, 30, tzinfo=UTC)
    target = current + timedelta(seconds=5)

    def interrupt(_seconds: float) -> None:
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        wait_until(target, now=lambda: current, sleep=interrupt)
