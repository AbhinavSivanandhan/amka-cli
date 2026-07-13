# Amka Design

## Problem Framing

The underspecified task was interpreted as a local, one-shot, foreground alarm tool that is complete and reliable within a small implementation window. V0 focuses on turning explicit terminal input into one future notification without hidden state or background machinery.

## Product Principles

- Foreground by default.
- Explicit time input.
- No hidden persistence.
- Predictable output and exit codes.
- Useful to humans and shell automation.
- Graceful degradation across terminals.

## Command Design

`set` is the single action because V0 creates one foreground alarm and waits for it to fire. `--in` expresses relative intent, such as `5s` or `1h30m`. `--at` expresses the next local-time occurrence of a clock time, such as `07:30`.

Exactly one scheduling mode is required so commands stay unambiguous. `--quiet` changes confirmation verbosity without hiding the final alarm. `--no-bell` supports redirected output and noninteractive use while keeping the visual notification.

## Time Semantics

Amka uses timezone-aware datetimes. `--at HH:MM` resolves to the next strictly future local occurrence in the current local timezone. If today’s matching clock time is already due, tomorrow is used.

Foreground waiting uses one bounded sleep for the remaining duration. `Ctrl+C` cancels cleanly and exits with code 130.

## Output Contract

Normal output goes to stdout. Expected errors go to stderr. Exit codes are 0 for success, 1 for invalid schedules or expected Amka input errors, 2 for command-line usage errors, and 130 for interruption.

The ASCII alarm banner works without color. ANSI emphasis is only used on compatible interactive terminals, and `NO_COLOR` is respected.

## Security, Privacy, And Performance

V0 performs no network access, telemetry, persistence, shell execution, subprocesses, or arbitrary command execution. Memory use is constant. Waiting does not busy-loop. Labels are bounded by the CLI and display-truncated in the notification banner.

## AI-Assisted Implementation

AI was used as a constrained implementation agent. Requirements and checkpoints were defined first. File-level edit boundaries were specified. Tests and validation commands were explicit. Agent output was reviewed. Blockers were corrected through narrow follow-up tasks. The human retained product and architecture decisions.

## Tradeoffs And Deferred Work

Foreground execution limits alarms to the process lifetime. Terminal bells vary by terminal. Persistence, multiple alarms, managed background execution, recurrence, and remote delivery remain deferred. Completeness and predictability were prioritized over feature count.
