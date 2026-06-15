"""Build a schema-aware NL->SQL prompt (pure function).

The prompt advertises only the configured tables/columns so the model is
constrained to the known schema, and embeds the user's question verbatim.
"""
from __future__ import annotations

from .schema import Schema


def build_prompt(question: str, schema: Schema) -> str:
    """Return a prompt that constrains the model to the known schema.

    Schema-aware: lists every table and its columns so the model can only
    reference real tables/columns, and embeds the user's question verbatim.
    Pure function — no I/O, deterministic for a given (question, schema).
    """
    return (
        "You translate a business question into a single read-only SQL SELECT "
        "for SQLite. Use only the tables and columns below; reference nothing else.\n"
        "\n"
        "Schema:\n"
        f"{schema.render()}\n"
        "\n"
        "Rules: output exactly one SELECT statement, no writes or DDL, no "
        "multiple statements.\n"
        "\n"
        f"Question: {question}\n"
        "SQL:"
    )
