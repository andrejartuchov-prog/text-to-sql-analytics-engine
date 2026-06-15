"""Minimal CLI: ask a question against the demo database.

    python -m textsql.cli --config config.example.yaml --seed tests/fixtures/seed.sql \
        --question "What were total sales on 2026-06-14?"
"""
from __future__ import annotations
import argparse
import pathlib

from .config import load_config
from .db import connect_seeded
from .engine import answer
from .llm import ClaudeClient


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Text-to-SQL analytics engine (demo).")
    parser.add_argument("--config", required=True)
    parser.add_argument("--seed", required=True)
    parser.add_argument("--question", required=True)
    args = parser.parse_args(argv)

    config = load_config(args.config)
    conn = connect_seeded(pathlib.Path(args.seed).read_text())
    llm = ClaudeClient(model=config.model)

    result = answer(args.question, schema=config.schema, conn=conn, llm=llm)

    print(f"SQL: {result.sql}")
    print(f"Rows: {result.rows}")
    print(f"Explanation: {result.explanation}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
