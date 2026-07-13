from datetime import datetime, timedelta

from amka.errors import InvalidScheduleError


def parse_duration(value: str) -> timedelta:
    text = value.strip()
    if not text:
        raise InvalidScheduleError("Duration is required, for example 5s.")
    if "-" in text:
        raise InvalidScheduleError("Duration must be positive.")
    if "." in text:
        raise InvalidScheduleError("Duration must use whole numbers.")
    if any(character.isspace() for character in text):
        raise InvalidScheduleError("Duration must not contain spaces.")

    units = {"h": 0, "m": 1, "s": 2}
    values: dict[str, int] = {}
    index = 0
    last_order = -1

    while index < len(text):
        start = index
        while index < len(text) and text[index].isdigit():
            index += 1
        if start == index:
            raise InvalidScheduleError("Duration must use values like 5s, 10m, or 1h30m.")
        if index >= len(text):
            raise InvalidScheduleError("Duration is missing a unit.")

        unit = text[index]
        index += 1

        if unit not in units:
            raise InvalidScheduleError("Duration unit must be h, m, or s.")
        if unit in values:
            raise InvalidScheduleError("Duration units must not be repeated.")
        if units[unit] <= last_order:
            raise InvalidScheduleError("Duration units must be ordered as h, then m, then s.")

        amount = int(text[start : index - 1])
        values[unit] = amount
        last_order = units[unit]

    if ("h" in values and values.get("m", 0) >= 60) or ("m" in values and values.get("s", 0) >= 60):
        raise InvalidScheduleError("Minutes and seconds must be less than 60 when combined.")

    duration = timedelta(
        hours=values.get("h", 0),
        minutes=values.get("m", 0),
        seconds=values.get("s", 0),
    )
    if duration.total_seconds() <= 0:
        raise InvalidScheduleError("Duration must be greater than zero.")

    return duration


def resolve_local_time(value: str, *, now: datetime) -> datetime:
    if now.tzinfo is None or now.utcoffset() is None:
        raise InvalidScheduleError("Current time must be timezone-aware.")
    if len(value) != 5 or value[2] != ":" or not value[:2].isdigit() or not value[3:].isdigit():
        raise InvalidScheduleError("Time must use HH:MM, for example 07:30.")

    hour = int(value[:2])
    minute = int(value[3:])
    if hour > 23:
        raise InvalidScheduleError("Hour must be between 00 and 23.")
    if minute > 59:
        raise InvalidScheduleError("Minute must be between 00 and 59.")

    candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if candidate <= now:
        candidate += timedelta(days=1)

    return candidate
