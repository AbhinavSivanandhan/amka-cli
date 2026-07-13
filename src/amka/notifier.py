import sys
from typing import TextIO


def notify_terminal(
    label: str | None,
    *,
    stream: TextIO = sys.stdout,
    bell_count: int = 3,
) -> None:
    if bell_count < 0:
        raise ValueError("bell_count must be non-negative")

    stream.write("\nALARM\n")
    if label is not None:
        stream.write(f"Label: {label}\n")
    stream.write("\a" * bell_count)
    stream.flush()
