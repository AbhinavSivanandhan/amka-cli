# Amka

Amka is a local-first Python CLI for scheduling prompt alarms.

“Amka” means wake up or alarm.

## Status

Amka is currently at V0 foundation: the repository structure, CLI entry point, package metadata, tests, and quality tooling are in place. Alarm behavior is not implemented yet.

## Local Development

On macOS with Python 3.12 available:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Verification

```bash
ruff format --check .
ruff check .
mypy src/amka
pytest --cov=amka --cov-report=term-missing
amka --help
amka version
```

See [docs/ROADMAP.md](docs/ROADMAP.md) for the checkpoint roadmap.
