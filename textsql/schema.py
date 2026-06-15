"""Schema model: tables -> columns, derived from the YAML config.

STUB — make-green-from-existing-red: production code starts here intentionally
incomplete so the PO-authored tests are RED. The executor implements this; the
test files are immutable.
"""
from __future__ import annotations
from typing import Dict, List


class Schema:
    def __init__(self, tables: Dict[str, List[str]]):
        # STUB: real implementation stores tables; here left empty so tests are RED.
        self._tables: Dict[str, List[str]] = {}

    def table_names(self) -> List[str]:
        return []

    def columns(self, table: str) -> List[str]:
        return []

    def has_table(self, table: str) -> bool:
        return False

    def has_column(self, table: str, column: str) -> bool:
        return False

    def render(self) -> str:
        """Human-readable schema block for the LLM prompt (table(col, col, ...))."""
        return ""
