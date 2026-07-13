# Amka Roadmap

## V0 — Minimum Complete Alarm

Goal: provide a complete foreground alarm flow.

### US-V0-01: Project foundation

As a contributor, I want a reproducible Python workspace so that I can build and validate Amka consistently.

Acceptance criteria:

- Project installs in editable mode.
- `amka --help` works.
- `amka version` works.
- Ruff, mypy, and pytest run successfully.
- CI configuration exists.
- Repository structure is ready for the first vertical slice.

### US-V0-02: Relative alarm

As a terminal user, I want to set an alarm using a relative duration so that I receive an alert after a specified interval.

Acceptance criteria:

- Support `amka set --in 5s`.
- Support `s`, `m`, and `h` units.
- Support combined values such as `1h30m`.
- Reject zero, negative, malformed, and unsupported durations.
- Display the resolved alarm time.
- Wait without busy-looping.
- Exit cleanly on `Ctrl+C`.

### US-V0-03: Absolute local-time alarm

As a terminal user, I want to set an alarm using a local time so that it fires at the next occurrence of that time.

Acceptance criteria:

- Support `amka set --at 07:30`.
- Resolve to the next strictly future local occurrence.
- Use timezone-aware datetimes.
- Display the resolved date, time, and timezone.
- Reject malformed input.

### US-V0-04: Terminal notification

As a user, I want a visible and audible notification so that I notice when the alarm becomes due.

Acceptance criteria:

- Print a visible alarm message.
- Include the optional label.
- Emit a bounded terminal bell.
- Do not ring indefinitely.
- Notification logic is independently testable.

### US-V0-05: V0 verification

As a maintainer, I want deterministic tests and a runnable demo so that V0 can be tagged confidently.

Acceptance criteria:

- Unit tests cover duration parsing and time resolution.
- CLI tests cover help, version, valid input, and invalid input.
- Tests do not rely on arbitrary long sleeps.
- Quality checks pass.
- End-to-end command works: `amka set --in 5s --label "Better demo"`

## V1 — Persistent Multi-Alarm CLI

Goal: evolve Amka from a foreground alarm into a reusable resource-oriented CLI.

- US-V1-01: Create alarms with stable IDs.
- US-V1-02: Persist alarms in versioned JSON.
- US-V1-03: List alarms deterministically.
- US-V1-04: Inspect one alarm by ID.
- US-V1-05: Cancel a scheduled alarm.
- US-V1-06: Run and process the next due alarm.
- US-V1-07: Use atomic file replacement.
- US-V1-08: Add repository and CLI integration tests.

## V2 — Reliability and Automation

Goal: improve correctness for automation and multiple due alarms.

- US-V2-01: Process simultaneous alarms independently.
- US-V2-02: Recover overdue alarms.
- US-V2-03: Isolate notification failures.
- US-V2-04: Support stable JSON output.
- US-V2-05: Separate stdout and stderr.
- US-V2-06: Add structured errors and exit codes.
- US-V2-07: Inject clock, waiting, repository, and notifier boundaries.
- US-V2-08: Remove real waiting from scheduler unit tests.

## V3 — Optional Product Polish

Goal: add only high-value capabilities after V0-V2 are stable.

- US-V3-01: Update scheduled alarms.
- US-V3-02: Snooze fired alarms.
- US-V3-03: Add optimistic entity versions.
- US-V3-04: Validate persisted storage.
- US-V3-05: Add dry-run support where useful.

## Deferred

- recurring alarms
- background daemon installation
- local IPC
- distributed scheduling
- multiple independent writers
- database persistence
- desktop notifications
- email
- webhooks
- arbitrary command execution
- generic plugin discovery
- exactly-once delivery

> Each checkpoint must remain independently runnable, tested, and demoable. Stop at the last complete checkpoint rather than partially implementing the next one.
