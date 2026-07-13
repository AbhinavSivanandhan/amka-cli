from datetime import UTC, datetime

import pytest

from amka.models import Alarm


def aware_datetime() -> datetime:
    return datetime(2026, 1, 1, 7, 30, tzinfo=UTC)


def make_alarm(**overrides: object) -> Alarm:
    values: dict[str, object] = {
        "id": "alm_123",
        "scheduled_for": aware_datetime(),
        "created_at": aware_datetime(),
        "updated_at": aware_datetime(),
    }
    values.update(overrides)
    return Alarm(**values)  # type: ignore[arg-type]


def test_alarm_accepts_timezone_aware_datetimes() -> None:
    alarm = make_alarm()

    assert alarm.scheduled_for == aware_datetime()


def test_naive_scheduled_for_is_rejected() -> None:
    with pytest.raises(ValueError, match="scheduled_for must be timezone-aware"):
        make_alarm(scheduled_for=datetime(2026, 1, 1, 7, 30))


def test_naive_created_at_is_rejected() -> None:
    with pytest.raises(ValueError, match="created_at must be timezone-aware"):
        make_alarm(created_at=datetime(2026, 1, 1, 7, 30))


def test_naive_updated_at_is_rejected() -> None:
    with pytest.raises(ValueError, match="updated_at must be timezone-aware"):
        make_alarm(updated_at=datetime(2026, 1, 1, 7, 30))


def test_invalid_id_is_rejected() -> None:
    with pytest.raises(ValueError, match="id must start with 'alm_'"):
        make_alarm(id="bad_123")


def test_version_zero_is_rejected() -> None:
    with pytest.raises(ValueError, match="version must be at least 1"):
        make_alarm(version=0)


def test_negative_snooze_count_is_rejected() -> None:
    with pytest.raises(ValueError, match="snooze_count must be non-negative"):
        make_alarm(snooze_count=-1)


def test_label_over_200_characters_is_rejected() -> None:
    with pytest.raises(ValueError, match="label must not exceed 200 characters"):
        make_alarm(label="x" * 201)
