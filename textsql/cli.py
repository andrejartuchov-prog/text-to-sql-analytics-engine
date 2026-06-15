"""Minimal CLI: ask a question against the demo database.

    python -m textsql.cli --config config.example.yaml --seed tests/fixtures/seed.sql \
        --question "What were total sales on 2026-06-14?"

STUB — production code intentionally incomplete (RED). Executor implements.
"""
from __future__ import annotations
import argparse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Text-to-SQL analytics engine (demo).")
    parser.add_argument("--config", required=True)
    parser.add_argument("--seed", required=True)
    parser.add_argument("--question", required=True)
    parser.parse_args(argv)
    # STUB: wire config -> ClaudeClient -> engine.answer and print sql/rows/explanation.
    raise NotImplementedError("CLI is implemented in make-green")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
