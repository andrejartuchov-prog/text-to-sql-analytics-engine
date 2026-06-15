# Text-to-SQL Analytics Engine

Ask your retail data a question in plain English and get the right answer **and a
business explanation of it**. The engine turns a natural-language question into
**schema-aware SQL**, runs it read-only against your database, and explains the
result grounded strictly in the returned rows — it never invents numbers.

It's **config-driven**: the schema, KPIs and model live in a YAML file, so adapting
it to a new dataset is a config change, not a rewrite (same idea as a config-driven
scraper).

> Demo note: the production design targets **PostgreSQL**; this self-contained demo
> uses **SQLite** (stdlib) so the example below runs with zero external services.

## How it works

```
            ┌──────────────┐   schema-aware    ┌──────────────┐
 question ─▶│ prompt build │──────prompt──────▶│  LLM adapter │ (Claude; mocked in tests)
            └──────────────┘                   └──────┬───────┘
                                                      │ SQL
                                                      ▼
            ┌──────────────┐    safe SELECT    ┌──────────────┐
 answer  ◀──│  explanation │◀──────rows────────│   guardrail  │─▶ read-only execution
 + reason   │ (grounded)   │                   │ (read-only,  │   over the database
            └──────────────┘                   │  known tables)│
                                                └──────────────┘
```

- **prompt** — builds a schema-aware prompt (only your tables/columns) — pure function.
- **guardrail** — rejects anything that isn't a single read-only `SELECT` over known
  tables (no `INSERT/UPDATE/DELETE/DDL`, no multi-statements). Validated **before** exec.
- **execution** — runs the SQL read-only and returns rows.
- **explanation** — describes the result citing **only** numbers present in the rows
  (anti-hallucination), so the answer is trustworthy.

Every piece is a small, testable unit; the LLM call sits behind a thin adapter, so the
whole pipeline is **unit-tested offline against fixtures — no network, no live DB**.

## Install

```bash
python -m pip install -r requirements.txt
```

## Use

```bash
python -m textsql.cli \
  --config config.example.yaml \
  --seed tests/fixtures/seed.sql \
  --question "What were total sales on 2026-06-14?"
```

## Worked example

Question:

> What were total sales on 2026-06-14?

Generated SQL (schema-aware, read-only):

```sql
SELECT SUM(revenue) AS total_revenue
FROM sales
WHERE sale_date = '2026-06-14';
```

Result:

| total_revenue |
|---------------|
| 1500.0        |

Explanation:

> Total sales on 2026-06-14 were 1500.0 across the matching records.

## Tests

```bash
pytest
```

The test suite is the project's quality spec: NL→SQL prompt is schema-aware, the
guardrail blocks every non-read-only statement, ingestion is idempotent, query
execution is correct over a seeded fixture, and the explanation is grounded (no
invented numbers). All offline.
