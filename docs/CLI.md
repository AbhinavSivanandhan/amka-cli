# Amka CLI

## Synopsis

```text
amka [OPTIONS] COMMAND [ARGS]...
amka set (--in DURATION | --at HH:MM) [--label TEXT] [--quiet] [--no-bell]
```

## Commands

- `amka set`: set a foreground alarm.
- `amka version`: print the installed version.

## Global Options

- `--help`: show help and exit.
- `--version`: print the installed version and exit.

## Set Options

- `--in`: relative duration, such as `5s`.
- `--at`: local time in 24-hour `HH:MM`.
- `--label`: optional alarm label.
- `--quiet`: suppress scheduling confirmation.
- `--no-bell`: prevent terminal bell characters.
- `--help`: show help for `amka set`.

## Duration Grammar

Durations use `s`, `m`, and `h`.

Examples:

```text
5s
10m
1h30m
```

Units must appear in descending order: `h`, then `m`, then `s`. Minutes and seconds must be below 60 when combined with larger units.

## Output Contract

Scheduling confirmation goes to stdout. The final alarm notification goes to stdout.

Expected errors go to stderr. `--quiet` suppresses confirmation only. `--no-bell` removes BEL characters.

## Exit Codes

| Code | Meaning                                       |
| ---: | --------------------------------------------- |
|    0 | Success                                       |
|    1 | Invalid schedule or expected Amka input error |
|    2 | Command-line usage error                      |
|  130 | Interrupted with Ctrl+C                       |

## Shell Examples

```bash
amka set --in 5m --label "Break"
amka set --at 07:30 --label "Wake up"
amka set --in 10s --quiet
amka set --in 10s --no-bell >alarm.log
amka --version
```
