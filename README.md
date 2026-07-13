# Amka

Amka is a foreground Python CLI alarm clock.

“Amka” means wake up or alarm.

V0 supports relative alarms and next-occurrence local-time alarms.

Amka treats an alarm as a small temporal contract: resolve explicit human intent into one future instant, wait without unnecessary resource use, notify clearly, and terminate with predictable output and exit behavior. V0 deliberately avoids persistence, background processes, and hidden state so behavior remains observable and testable.

## Installation

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Usage

```bash
amka set --in 5s --label "Take a break"
amka set --at 07:30 --label "Wake up"
amka version
```

`--in` supports `h`, `m`, and `s`, including combined durations such as `1h30m`.
`--at` uses 24-hour `HH:MM` and resolves to the next future local occurrence.
Exactly one of `--in` or `--at` is required. `Ctrl+C` cancels cleanly.
`--quiet` suppresses scheduling confirmation. `--no-bell` is useful when redirecting output.

See [docs/CLI.md](docs/CLI.md) for the CLI reference.

## Documentation

- [CLI reference](docs/CLI.md)
- [Design notes](docs/DESIGN.md)
- [Roadmap](docs/ROADMAP.md)
- [Demo guide](docs/DEMO.md)

## Verification

```bash
./scripts/check.sh
```

## Scope

V0 is intentionally foreground-only and does not yet include persistence, multiple managed alarms, a background service, recurrence, or remote notifications.

See [docs/ROADMAP.md](docs/ROADMAP.md) for the roadmap.
