# Amka Demo Guide

## Recording Preparation

```bash
source .venv/bin/activate
clear
```

- Use a terminal font large enough to read.
- Hide notifications and unrelated windows.
- Keep the repository already open.
- Check the microphone.
- Record at 1080p or higher.
- Use a terminal width around 100 columns.

## Five-Minute Sequence

### 0:00-0:35 — Frame The Problem

Narration: The specification was intentionally underspecified. The design target was a complete local alarm primitive, not maximum features. Foreground behavior avoids hidden files and background processes.

### 0:35-1:05 — Show The Repository

```bash
sed -n '1,220p' README.md
sed -n '1,220p' docs/ROADMAP.md
```

Narration: Development followed checkpoints. User stories remain synchronized with the implementation. Deferred scope is explicit.

### 1:05-1:35 — Discoverability

```bash
amka --help
amka set --help
amka --version
```

Narration: Amka uses conventional CLI behavior and includes scripting-friendly options.

### 1:35-2:20 — Relative Alarm

```bash
amka set --in 3s --label "Stand and stretch"
```

Narration: The command prints a resolved local timestamp, waits in the foreground, then shows a visible ASCII banner. Compatible terminals may add restrained emphasis, and bell output is bounded.

### 2:20-2:55 — Failure Behavior

```bash
amka set --in invalid
echo "exit=$?"
```

Narration: Expected errors go to stderr, stay concise, avoid tracebacks, and use exit code 1.

### 2:55-3:30 — Automation Behavior

```bash
amka set --in 1s --label "Pipeline-safe" --quiet --no-bell
amka set --in 1s --label "Redirected" --no-bell > /tmp/amka-demo.log
cat /tmp/amka-demo.log
```

Narration: Quiet mode suppresses confirmation while preserving the alarm. No-bell mode keeps redirected output clean.

### 3:30-4:05 — Absolute Local Time

```bash
TARGET_TIME="$(date -v+1M '+%H:%M')"
amka set --at "$TARGET_TIME" --label "Next local occurrence"
```

Cancel with `Ctrl+C` after confirmation.

Narration: Absolute alarms use timezone-aware next-occurrence semantics. Cancellation exits with code 130.

### 4:05-4:35 — Engineering Validation

```bash
./scripts/check.sh
```

Narration: The gate runs Ruff, mypy, pytest, and coverage. Tests are deterministic and avoid long sleeps.

### 4:35-5:00 — Close

Narration: V0 has focused scope, explicit tradeoffs, a conventional CLI contract, constrained AI use, and a reliable completed checkpoint rather than partially implemented features.

## Recording Safeguards

- Recalculate `TARGET_TIME` immediately before the absolute-time demo.
- Use `--no-bell` if recording software reacts poorly to BEL.
- Do not scroll through source code unless explaining a specific decision.
- Avoid showing tokens, credentials, email addresses, or unrelated terminal history.
- Keep the final video under six minutes.
