from datetime import UTC, datetime, timedelta, timezone

import pytest

from amka.errors import InvalidScheduleError
from amka.timeparse import parse_duration, resolve_local_time


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("5s", timedelta(seconds=5)),
        ("10m", timedelta(minutes=10)),
        ("2h", timedelta(hours=2)),
        ("1h30m", timedelta(hours=1, minutes=30)),
        ("1h30m5s", timedelta(hours=1, minutes=30, seconds=5)),
        (" 5s ", timedelta(seconds=5)),
    ],
)
def test_parse_duration_valid_values(value: str, expected: timedelta) -> None:
    assert parse_duration(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "",
        "0s",
        "-1s",
        "1.5s",
        "1d",
        "1h 30m",
        "1sabc",
        "1h2h",
        "1s1m",
        "1h60m",
        "1m60s",
    ],
)
def test_parse_duration_rejects_invalid_values(value: str) -> None:
    with pytest.raises(InvalidScheduleError):
        parse_duration(value)


def test_later_time_today_resolves_to_today() -> None:
    now = datetime(2026, 1, 1, 7, 0, tzinfo=UTC)

    assert resolve_local_time("07:30", now=now) == datetime(2026, 1, 1, 7, 30, tzinfo=UTC)


def test_earlier_time_resolves_to_tomorrow() -> None:
    now = datetime(2026, 1, 1, 8, 0, tzinfo=UTC)

    assert resolve_local_time("07:30", now=now) == datetime(2026, 1, 2, 7, 30, tzinfo=UTC)


def test_equal_hour_and_minute_resolves_to_tomorrow() -> None:
    now = datetime(2026, 1, 1, 7, 30, tzinfo=UTC)

    assert resolve_local_time("07:30", now=now) == datetime(2026, 1, 2, 7, 30, tzinfo=UTC)


def test_midnight_rollover() -> None:
    now = datetime(2026, 1, 1, 23, 59, tzinfo=UTC)

    assert resolve_local_time("00:00", now=now) == datetime(2026, 1, 2, 0, 0, tzinfo=UTC)


def test_timezone_awareness_is_preserved() -> None:
    local_zone = timezone(timedelta(hours=5, minutes=30))
    now = datetime(2026, 1, 1, 7, 0, tzinfo=local_zone)

    resolved = resolve_local_time("07:30", now=now)

    assert resolved.tzinfo is local_zone
    assert resolved.utcoffset() == timedelta(hours=5, minutes=30)


def test_naive_now_is_rejected() -> None:
    with pytest.raises(InvalidScheduleError, match="timezone-aware"):
        resolve_local_time("07:30", now=datetime(2026, 1, 1, 7, 0))


@pytest.mark.parametrize(
    "value",
    [
        "",
        "7:30",
        "07:3",
        "24:00",
        "12:60",
        "07-30",
        " 07:30",
        "07:30 ",
        "07:30:15",
    ],
)
def test_resolve_local_time_rejects_invalid_values(value: str) -> None:
    now = datetime(2026, 1, 1, 7, 0, tzinfo=UTC)

    with pytest.raises(InvalidScheduleError):
        resolve_local_time(value, now=now)
