"""Schema model: tables -> columns, derived from the YAML config.

The schema is the single source of truth the NL->SQL layer is constrained to:
the prompt advertises only these tables/columns and the guardrail rejects any
SQL referencing a table outside it.
"""
from __future__ import annotations
from typing import Dict, List


class Schema:
    def __init__(self, tables: Dict[str, List[str]]):
        # Preserve declaration order (dict is ordered) so columns() is stable.
        self._tables: Dict[str, List[str]] = {t: list(cols) for t, cols in tables.items()}

    def table_names(self) -> List[str]:
        return list(self._tables)

    def columns(self, table: str) -> List[str]:
        return list(self._tables.get(table, []))

    def has_table(self, table: str) -> bool:
        return table in self._tables

    def has_column(self, table: str, column: str) -> bool:
        return column in self._tables.get(table, [])

    def render(self) -> str:
        """Human-readable schema block for the LLM prompt (table(col, col, ...))."""
        return "\n".join(
            f"{table}({', '.join(cols)})" for table, cols in self._tables.items()
        )
