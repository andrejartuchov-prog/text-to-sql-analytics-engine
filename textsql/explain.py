"""Business explanation grounded strictly in the returned rows.

The explanation may only cite numbers that actually appear in the result rows
(plus the row count). It must never invent figures — this is the anti-hallucination
guarantee that makes the engine trustworthy.

STUB — production code intentionally incomplete (RED). Executor implements.
"""
from __future__ import annotations
from typing import Dict, List


def explain(question: str, rows: List[Dict]) -> str:
    """Return a short NL explanation of `rows` answering `question`.

    Grounding contract: every numeric token in the returned string must be a value
    present in `rows` (or the integer row count). No invented numbers.
    """
    # STUB: empty explanation -> grounding/content tests are RED.
    return ""
