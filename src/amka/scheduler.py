from collections.abc import Callable
from datetime import datetime
from time import sleep as system_sleep


def _local_now() -> datetime:
    return datetime.now().astimezone()


def wait_until(
    target: datetime,
    *,
    now: Callable[[], datetime] = _local_now,
    sleep: Callable[[float], None] = system_sleep,
) -> None:
    if target.tzinfo is None or target.utcoffset() is None:
        raise ValueError("target must be timezone-aware")

    remaining = (target - now()).total_seconds()
    if remaining > 0:
        sleep(remaining)
