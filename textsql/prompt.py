"""Build a schema-aware NL->SQL prompt (pure function).

STUB — production code intentionally incomplete (RED). Executor implements.
"""
from __future__ import annotations

from .schema import Schema


def build_prompt(question: str, schema: Schema) -> str:
    """Return a prompt that constrains the model to the known schema.

    Must be schema-aware: include every table and its columns so the model can
    only reference real tables/columns, and embed the user's question verbatim.
    Pure function — no I/O, deterministic for a given (question, schema).
    """
    # STUB: empty prompt so tests are RED.
    return ""
