# Amka Roadmap

## V0 — Minimum Complete Alarm

Goal: provide a complete foreground alarm flow.

### [x] US-V0-01: Project foundation

As a contributor, I want a reproducible Python workspace so that I can build and validate Amka consistently.

Acceptance criteria:

- [x] Project installs in editable mode.
- [x] `amka --help` works.
- [x] `amka version` works.
- [x] Ruff, mypy, and pytest run successfully.
- [x] CI configuration exists.
- [x] Repository structure is ready for the first vertical slice.

### [x] US-V0-02: Relative alarm

As a terminal user, I want to set an alarm using a relative duration so that I receive an alert after a specified interval.

Acceptance criteria:

- [x] Support `amka set --in 5s`.
- [x] Support `s`, `m`, and `h` units.
- [x] Support combined values such as `1h30m`.
- [x] Reject zero, negative, malformed, and unsupported durations.
- [x] Display the resolved alarm time.
- [x] Wait without busy-looping.
- [x] Exit cleanly on `Ctrl+C`.

### [x] US-V0-03: Absolute local-time alarm

As a terminal user, I want to set an alarm using a local time so that it fires at the next occurrence of that time.

Acceptance criteria:

- [x] Support `amka set --at 07:30`.
- [x] Resolve to the next strictly future local occurrence.
- [x] Use timezone-aware datetimes.
- [x] Display the resolved date, time, and timezone.
- [x] Reject malformed input.

### [x] US-V0-04: Terminal notification

As a user, I want a visible and audible notification so that I notice when the alarm becomes due.

Acceptance criteria:

- [x] Print a visible alarm message.
- [x] Include the optional label.
- [x] Emit a bounded terminal bell.
- [x] Do not ring indefinitely.
- [x] Notification logic is independently testable.

### [x] US-V0-05: V0 verification

As a maintainer, I want deterministic tests and a runnable demo so that V0 can be tagged confidently.

Acceptance criteria:

- [x] Unit tests cover duration parsing and time resolution.
- [x] CLI tests cover help, version, valid input, and invalid input.
- [x] Tests do not rely on arbitrary long sleeps.
- [x] Quality checks pass.
- [x] End-to-end command works: `amka set --in 5s --label "Better demo"`

### [x] US-V0-06: CLI conventions and scripting ergonomics

As a terminal user, I want predictable output and exit behavior so that Amka works naturally in shell scripts and command pipelines.

Acceptance criteria:

- [x] `amka --version` prints the installed version and exits successfully.
- [x] Successful command output is written to stdout.
- [x] Expected errors are written to stderr.
- [x] Invalid schedules exit with code 1.
- [x] Command-line usage errors exit with code 2.
- [x] Interrupted alarms exit with code 130.
- [x] `--quiet` suppresses scheduling confirmation but preserves the final alarm notification.
- [x] `--no-bell` prevents terminal bell characters.
- [x] CLI behavior is documented in `docs/CLI.md`.

### [x] US-V0-07: Demo-ready notification and design record

As a reviewer, I want a visually clear alarm and concise engineering documentation so that I can understand and evaluate the product quickly.

Acceptance criteria:

- [x] Alarm output is visually prominent without relying on audio.
- [x] Plain output remains readable without ANSI support.
- [x] Compatible terminals receive restrained visual emphasis.
- [x] `NO_COLOR` and `TERM=dumb` are respected.
- [x] Design decisions and tradeoffs are documented.
- [x] A five-minute demo guide is available.

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
