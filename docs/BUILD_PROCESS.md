# Amka Build Process

## How I interpreted the task

The assignment was intentionally open-ended:

> Build an alarm clock as a Python CLI application. CLI only, no web UI, no React, no database. There is no detailed specification; decide what to build with the time available.

I treated this as a product and engineering judgment exercise rather than a feature-count exercise.

My goal was to:

* deliver one complete and reliable alarm flow
* keep V0 foreground-only and observable
* avoid hidden state, persistence, daemons, and unnecessary architecture
* support both people and shell automation
* make time behavior explicit and testable
* use AI as a constrained implementation agent rather than as the product decision-maker
* stop at a complete checkpoint instead of partially implementing broader features

## Product and technical decisions I considered

Before implementation, I considered several possible directions:

* a minimal single foreground timer
* multiple alarms with persistence
* a background or detached runner
* daemon and IPC-based process management
* JSON output for automation
* desktop or remote notifications
* recurrence and snoozing
* shell scripting behavior and exit-code conventions
* human-readable and machine-friendly output
* package naming, CLI naming, and PyPI distribution naming

The technology stack followed from the constraints and the size of the exercise:

* Python as the required implementation language
* Typer for a conventional declarative CLI
* standard-library timezone-aware datetimes for scheduling
* pytest for behavior verification
* Ruff for formatting and linting
* mypy for static checking
* coverage for a measurable quality gate
* GitHub Actions for repeatable CI

I kept the architecture functional and module-oriented. V0 needed only a few explicit boundaries—parsing, waiting, notification, and CLI orchestration—so I deliberately avoided service layers, framework abstractions, and future-facing architecture that the current product did not require.

For V0, I selected:

* foreground execution
* one-shot alarms
* relative scheduling with `--in`
* absolute next-occurrence local time with `--at`
* timezone-aware datetimes
* visible terminal notification
* bounded terminal bells
* predictable stdout, stderr, and exit codes
* `--quiet` and `--no-bell` for scripting
* no persistence, subprocesses, database, network access, or hidden files

## How I shaped the product

I made the main product decisions before implementation began.

I selected the name **Amka**, a concise word associated with waking or an alarm, while keeping the command language and all public documentation in English.

I pushed the product toward a declarative command grammar:

```bash
amka set --in 5m
amka set --at 07:30
```

The intent was that users should describe the outcome they want rather than manage implementation details. I chose `set` as the single V0 action, with `--in` expressing relative intent and `--at` expressing a future local clock time.

I also established early principles that influenced the UX:

* commands should be concise and predictable
* exactly one scheduling mode should be required
* successful output and failures should have clear contracts
* scripting behavior should be treated as a product requirement, not an afterthought
* foreground behavior should remain the default
* optional behavior should be explicit rather than hidden
* documentation and roadmap status should stay synchronized with implementation

I specifically raised the importance of bots, scripts, and automation as major consumers of CLI tools. That led to deliberate support for:

* stable exit codes
* stdout and stderr separation
* concise failures without tracebacks
* `--quiet`
* `--no-bell`
* redirected output
* conventional `--help` and `--version` behavior

I also chose to defer background execution after reviewing its implications. A managed background runner would require process ownership, persisted metadata, stale PID handling, cancellation semantics, and useful notification delivery. Rather than adding a fragile partial implementation, I placed it in a later optional roadmap story.

## Development sequence

1. Defined the product as a local, one-shot foreground alarm CLI.
2. Chose the package, module, command, and distribution naming strategy.
3. Created a user-story roadmap for V0 through V3.
4. Scaffolded the Python project and quality tooling.
5. Implemented relative-duration parsing.
6. Added efficient foreground waiting without busy-looping.
7. Added visible and audible terminal notification.
8. Added absolute local-time scheduling with next-occurrence semantics.
9. Added unit, CLI, and integration tests.
10. Added coverage, linting, type checking, and CI.
11. Fixed stdout binding so terminal output remained capturable and redirectable.
12. Added conventional exit codes and stdout/stderr behavior.
13. Added `--version`, `--quiet`, and `--no-bell`.
14. Added a compact ASCII alarm banner with restrained ANSI emphasis.
15. Added CLI, design, roadmap, demo, and build-process documentation.
16. Completed V0 with 82 tests and approximately 95% coverage.

## ChatGPT prompts and decisions

I used ChatGPT as the product and engineering design layer.

### 1. Product framing

I asked it to refine the underspecified requirement into the smallest complete product.

This produced:

* a foreground alarm
* explicit scheduling input
* no persistence
* no database
* no unnecessary abstractions

### 2. Architecture and roadmap

I asked for:

* a V0–V3 roadmap
* user stories
* acceptance criteria
* deferred features
* release checkpoints

I also required roadmap checkboxes to remain synchronized with validated implementation.

### 3. Naming and distribution

I explored package naming before scaffolding.

This separated:

* product name
* PyPI distribution name
* Python import package
* CLI executable
* GitHub repository name

I selected **Amka** as the product and CLI identity.

### 4. Workspace design

I asked for a compact Python workspace using:

* a `src` layout
* Typer
* Ruff
* mypy
* pytest
* coverage
* CI
* editable installation

### 5. Relative alarm design

I refined:

* duration grammar
* validation rules
* waiting semantics
* cancellation behavior
* notification behavior

### 6. Absolute-time design

I refined:

* strict `HH:MM`
* timezone-aware local time
* next strictly future occurrence
* mutual exclusivity of `--in` and `--at`

### 7. V0 verification

I asked for:

* focused integration coverage
* README synchronization
* a full quality gate
* manual smoke tests
* roadmap completion

### 8. CLI and automation ergonomics

I introduced the requirement that the tool should behave naturally in shell scripts and pipelines.

This led to:

* `amka --version`
* stdout and stderr separation
* exit codes `0`, `1`, `2`, and `130`
* `--quiet`
* `--no-bell`
* concise CLI reference documentation

### 9. Demo readiness

I asked for the alarm to remain noticeable even in a muted recording.

This led to:

* a compact ASCII notification banner
* optional TTY-only ANSI emphasis
* `NO_COLOR` support
* `TERM=dumb` support
* design documentation
* a five-minute demo guide

## Codex implementation prompts

I used Codex as a constrained implementation agent.

Each prompt specified:

* which files it could read
* which files it could edit
* exact behavior to implement
* exact validation commands
* when to stop

### 1. Project foundation

Codex created:

* package layout
* project metadata
* CLI entry point
* initial model and errors
* tests
* CI
* roadmap
* README and security files

### 2. Relative alarm and notification

Codex implemented:

* duration parsing
* wait helper
* terminal notifier
* `amka set --in`
* cancellation
* focused tests

### 3. Absolute local-time alarm

Codex implemented:

* `resolve_local_time`
* `amka set --at`
* strict scheduling-option validation
* timezone-aware next-occurrence logic
* CLI and unit tests

### 4. V0 verification

Codex added:

* an integration test
* a coverage threshold
* README updates
* the full validation gate

### 5. Notification capture fix

A test exposed that `sys.stdout` had been bound too early.

I reviewed the blocker and issued a narrow follow-up prompt to:

* resolve stdout at call time
* preserve redirection
* preserve CLI capture
* add focused regression coverage

### 6. CLI conventions

Codex added:

* `amka --version`
* stderr behavior
* the exit-code contract
* `--quiet`
* `--no-bell`
* CLI reference documentation

### 7. Demo-ready presentation

Codex added:

* a compact ASCII banner
* TTY-only ANSI emphasis
* `NO_COLOR`
* `TERM=dumb`
* design documentation
* a five-minute demo guide
* synchronized roadmap status

## Security, privacy, vulnerability, and distribution considerations

Security and privacy were addressed primarily through scope control and deliberate exclusion.

V0 performs:

* no network access
* no telemetry
* no persistence
* no shell execution
* no subprocess execution
* no arbitrary command execution
* no background process management
* no plugin loading
* no database access

This removed several common attack and privacy surfaces before they could arise.

I also considered how the tool might later be distributed through PyPI, Homebrew, or other package systems. That influenced several choices:

* no install-time scripts beyond standard packaging behavior
* no downloading of runtime assets
* no hidden configuration files
* no automatic service installation
* no privilege escalation
* no execution of user-provided commands
* no dependency-heavy notification framework
* no remote update mechanism

These decisions do not mean any distributed software can be described as vulnerability-free. They do mean V0 has a deliberately small attack surface and avoids many categories of supply-chain, command-injection, persistence, telemetry, and privilege-related risk.

Input and runtime behavior were also constrained:

* durations use a strict grammar
* local times use strict `HH:MM`
* labels are length-bounded
* long labels are display-truncated
* expected failures are handled without tracebacks
* waiting uses one sleep instead of a busy loop
* memory use remains constant
* ANSI output is restricted to compatible interactive terminals
* `NO_COLOR` and `TERM=dumb` are respected
* redirected output remains plain and predictable

This also improves extension safety. Future persistence, background execution, plugins, remote delivery, or package-manager integrations can be evaluated as explicit new threat surfaces rather than being embedded invisibly in V0.

## AI collaboration model

I intentionally separated responsibilities:

* I provided product direction, naming, scope, command principles, automation requirements, and review feedback.
* ChatGPT refined requirements, decomposed work, defined acceptance criteria, and reviewed blockers.
* Codex applied exact file changes and ran validation.
* I required file-level boundaries to keep implementation focused and token usage controlled.
* Failures were handled with narrow corrective prompts instead of broad rewrites.
* Roadmap items were marked complete only after validation passed.
* I retained the product, architecture, UX, command-language, and release decisions.

This made the AI usage visible, reviewable, and constrained.

## Tradeoffs and deferred work

The main V0 tradeoff is foreground execution. The alarm exists only for the lifetime of the running process.

I considered managed background execution, but deferred it because a reliable implementation requires:

* stable alarm IDs
* persisted schedules
* process ownership
* stale process cleanup
* safe cancellation
* useful notification delivery
* cross-platform lifecycle behavior

Other deferred capabilities include:

* persistent multiple alarms
* managed background execution
* recurrence
* snoozing
* JSON output
* remote notifications
* desktop notifications
* shell completion
* package-manager-specific manpages

The decision was to complete a reliable, explainable V0 rather than partially implement several fragile features.

## Final V0 result

Amka V0 provides:

* relative alarms
* next-occurrence local-time alarms
* timezone-aware scheduling
* foreground waiting
* clean cancellation
* visible ASCII notification
* optional terminal emphasis
* bounded bells
* quiet and no-bell modes
* predictable output and exit codes
* scripting-friendly behavior
* 82 passing tests
* approximately 95% coverage
* synchronized roadmap, CLI reference, design notes, demo guide, and build-process documentation

The final result reflects the central engineering decision I made for the exercise: prioritize a complete, observable, testable product with explicit tradeoffs over a larger but fragile feature set.
