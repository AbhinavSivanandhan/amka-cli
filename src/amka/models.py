from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class AlarmStatus(StrEnum):
    SCHEDULED = "scheduled"
    FIRED = "fired"
    CANCELLED = "cancelled"
    NOTIFICATION_FAILED = "notification_failed"


@dataclass(frozen=True, slots=True)
class Alarm:
    id: str
    scheduled_for: datetime
    created_at: datetime
    updated_at: datetime
    status: AlarmStatus = AlarmStatus.SCHEDULED
    label: str | None = None
    version: int = 1
    snooze_count: int = 0

    def __post_init__(self) -> None:
        self._require_aware_datetime(self.scheduled_for, "scheduled_for")
        self._require_aware_datetime(self.created_at, "created_at")
        self._require_aware_datetime(self.updated_at, "updated_at")

        if not self.id.startswith("alm_"):
            raise ValueError("id must start with 'alm_'")
        if self.version < 1:
            raise ValueError("version must be at least 1")
        if self.snooze_count < 0:
            raise ValueError("snooze_count must be non-negative")
        if self.label is not None and len(self.label) > 200:
            raise ValueError("label must not exceed 200 characters")

    @staticmethod
    def _require_aware_datetime(value: datetime, field_name: str) -> None:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(f"{field_name} must be timezone-aware")
