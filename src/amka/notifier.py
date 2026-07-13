import sys
from os import environ
from typing import TextIO

MIN_INNER_WIDTH = 28
MAX_INNER_WIDTH = 60
ALARM_TEXT = "ALARM"
ANSI_ALARM_TEXT = "\033[1;31mALARM\033[0m"


def notify_terminal(
    label: str | None,
    *,
    stream: TextIO | None = None,
    bell_count: int = 3,
) -> None:
    output = sys.stdout if stream is None else stream
    if bell_count < 0:
        raise ValueError("bell_count must be non-negative")

    alarm_text = ANSI_ALARM_TEXT if _should_emphasize(output) else ALARM_TEXT
    inner_width = _inner_width(label)
    border = f"+{'-' * inner_width}+"

    output.write("\n")
    output.write(f"{border}\n")
    output.write(f"|{alarm_text.center(inner_width + len(alarm_text) - len(ALARM_TEXT))}|\n")
    output.write(f"{border}\n")
    if label is not None:
        output.write(f"|{_display_label(label, inner_width).ljust(inner_width)}|\n")
        output.write(f"{border}\n")
    output.write("\a" * bell_count)
    output.flush()


def _inner_width(label: str | None) -> int:
    if label is None:
        return MIN_INNER_WIDTH
    return min(MAX_INNER_WIDTH, max(MIN_INNER_WIDTH, len(_label_text(label))))


def _display_label(label: str, inner_width: int) -> str:
    text = _label_text(label)
    if len(text) <= inner_width:
        return text
    return f"{text[: inner_width - 3]}..."


def _label_text(label: str) -> str:
    return f"Label: {label}"


def _should_emphasize(stream: TextIO) -> bool:
    if "NO_COLOR" in environ or environ.get("TERM") == "dumb":
        return False
    try:
        return stream.isatty()
    except (AttributeError, OSError):
        return False
