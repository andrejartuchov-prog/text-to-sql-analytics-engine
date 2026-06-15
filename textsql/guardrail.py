"""SQL guardrail: only read-only SELECT against known tables is allowed.

Validated BEFORE execution so an unsafe statement (write, DDL, multi-statement,
or one touching an unknown table) never reaches the database.
"""
from __future__ import annotations
import re

from .schema import Schema


class UnsafeSQLError(Exception):
    """Raised for non-read-only SQL: writes, DDL, or multiple statements."""


class SchemaError(Exception):
    """Raised when SQL references a table not present in the configured schema."""


# Tables are introduced by FROM/JOIN; the captured token is the real table name
# (any alias follows as a separate token and is ignored).
_TABLE_REF = re.compile(r"\b(?:FROM|JOIN)\s+([A-Za-z_][A-Za-z0-9_]*)", re.IGNORECASE)


def validate_sql(sql: str, schema: Schema) -> None:
    """Validate that `sql` is a single read-only SELECT over known tables.

    Rules:
      - Exactly one statement (reject `;`-separated multi-statements).
      - Statement is a SELECT (reject INSERT/UPDATE/DELETE/DROP/ALTER/CREATE/...).
      - Every table referenced (FROM/JOIN) exists in `schema` (else SchemaError).
    Returns None when valid; raises UnsafeSQLError / SchemaError otherwise.
    """
    statements = [s for s in (part.strip() for part in sql.split(";")) if s]
    if len(statements) != 1:
        raise UnsafeSQLError(f"expected a single statement, got {len(statements)}")

    statement = statements[0]
    if not re.match(r"(?is)^\s*SELECT\b", statement):
        raise UnsafeSQLError("only read-only SELECT statements are allowed")

    for table in _TABLE_REF.findall(statement):
        if not schema.has_table(table):
            raise SchemaError(f"unknown table: {table}")
