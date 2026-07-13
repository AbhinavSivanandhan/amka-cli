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

## Examples

### Relative Alarm

```bash
amka set --in 5s --label "Stand and stretch"
```

### Combined Duration

```bash
amka set --in 1h30m --label "Deep work complete"
```

### Absolute Local Time

```bash
amka set --at 07:30 --label "Wake up"
```

### Quiet Mode

```bash
amka set --in 10s --label "Pipeline-safe" --quiet
```

`--quiet` suppresses the scheduling confirmation but preserves the final alarm.

### No-Bell Mode

```bash
amka set --in 10s --label "Redirected alarm" --no-bell
```

`--no-bell` preserves the visible banner while omitting terminal BEL characters.

### Redirected Output

```bash
amka set --in 2s --label "Logged alarm" --no-bell > alarm.log
cat alarm.log
```

### Version And Help

```bash
amka --version
amka --help
amka set --help
```

### Failure Behavior

```bash
amka set --in invalid
echo "exit=$?"
```

Expected schedule errors go to stderr and exit with code 1.

### Cancellation

```bash
amka set --in 10m --label "Cancelable alarm"
```

`Ctrl+C` cancels cleanly and exits with code 130.

## Documentation

- [CLI reference](docs/CLI.md)
- [Design notes](docs/DESIGN.md)
- [Roadmap](docs/ROADMAP.md)
- [Demo guide](docs/DEMO.md)
- [Build process](docs/BUILD_PROCESS.md)
- [Security](docs/SECURITY.md)

## Verification

```bash
./scripts/check.sh
```

## Scope

V0 is intentionally foreground-only and does not yet include persistence, multiple managed alarms, a background service, recurrence, or remote notifications.

See [docs/ROADMAP.md](docs/ROADMAP.md) for the roadmap.
