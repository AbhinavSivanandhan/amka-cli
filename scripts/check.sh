#!/usr/bin/env bash
set -euo pipefail

ruff format --check .
ruff check .
mypy src/amka
pytest --cov=amka --cov-report=term-missing
