"""SQL guardrail: only read-only SELECT against known tables is allowed.

STUB — production code intentionally incomplete (RED). Executor implements.
"""
from __future__ import annotations

from .schema import Schema


class UnsafeSQLError(Exception):
    """Raised for non-read-only SQL: writes, DDL, or multiple statements."""


class SchemaError(Exception):
    """Raised when SQL references a table not present in the configured schema."""


def validate_sql(sql: str, schema: Schema) -> None:
    """Validate that `sql` is a single read-only SELECT over known tables.

    Rules:
      - Exactly one statement (reject `;`-separated multi-statements).
      - Statement is a SELECT (reject INSERT/UPDATE/DELETE/DROP/ALTER/CREATE/...).
      - Every table referenced (FROM/JOIN) exists in `schema` (else SchemaError).
    Returns None when valid; raises UnsafeSQLError / SchemaError otherwise.
    """
    # STUB: never raises -> the "rejects ..." tests are RED.
    return None
