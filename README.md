# Practice Lab 1 — Python Risk-Scoring Engine

A small command-line script that scores product-launch risks, assigns each a
readiness status, and prints a report sorted from most to least risky.

## Requirements

- Python 3.11+ (uses `list[dict[str, Any]]` style generics; standard library only)

## Usage

```bash
python risk-engine.py
```

This scores the sample risks in `RISKS`, prints the report as JSON, and runs a
few `assert` checks. Expected tail of the output:

```
Checks passed.
```

## Data model

Each risk is a `ProductRisk` dataclass:

| Field                   | Type    | Range / values | Meaning                                  |
| ----------------------- | ------- | -------------- | ---------------------------------------- |
| `product`               | `str`   | —              | Product name                             |
| `severity`              | `int`   | 1–5            | Impact if the risk materializes          |
| `probability`           | `float` | 0.0–1.0        | Likelihood the risk materializes         |
| `days_to_launch`        | `int`   | ≥ 0            | Days remaining until launch              |
| `documentation_complete`| `bool`  | —              | Whether launch documentation is finished |

## Scoring

`calculate_score(risk)` sums three parts and rounds to one decimal:

1. **Base score** — `severity * probability * 10` (0–50).
2. **Urgency points** — based on `days_to_launch`:
   - `< 30` days → `+20`
   - `30–59` days → `+10`
   - `>= 60` days → `+0`
3. **Documentation penalty** — `+15` if `documentation_complete` is `False`.

> Note: the urgency thresholds are inferred from the lab's verification check
> (Orion Display must score `75.0`). Adjust them if your worksheet specifies
> different cutoffs.

## Status bands

`assign_status(score)` maps the numeric score to a label:

| Score        | Status     |
| ------------ | ---------- |
| `>= 55`      | `Critical` |
| `30`–`54.9`  | `Watch`    |
| `< 30`       | `On Track` |

## Report

`build_report(risks)` returns a list of dicts — each risk's fields plus its
`score` and `status` — sorted by `score` descending.

### Sample output

| Product        | Score | Status   |
| -------------- | ----- | -------- |
| Orion Display  | 75.0  | Critical |
| Atlas Mobility | 39.0  | Watch    |
| Nova Audio     | 23.5  | On Track |

## Files

- `risk-engine.py` — data model, scoring logic, report builder, and inline checks.
