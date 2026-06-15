"""End-to-end orchestration: question -> SQL -> guarded execution -> explanation.

STUB — production code intentionally incomplete (RED). Executor implements.
"""
from __future__ import annotations
import sqlite3
from dataclasses import dataclass, field
from typing import Dict, List

from .schema import Schema
from .prompt import build_prompt
from .guardrail import validate_sql
from .db import run_query
from .explain import explain
from .llm import LLMClient


@dataclass
class Answer:
    sql: str = ""
    rows: List[Dict] = field(default_factory=list)
    explanation: str = ""


def answer(question: str, *, schema: Schema, conn: sqlite3.Connection, llm: LLMClient) -> Answer:
    """Run the full pipeline for one question and return the Answer.

    Steps: build_prompt -> llm.generate_sql -> validate_sql (raises on unsafe)
    -> run_query -> explain. The generated SQL is validated BEFORE execution.
    """
    # STUB: empty answer -> the end-to-end tests are RED.
    return Answer()
