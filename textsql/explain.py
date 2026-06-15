"""Business explanation grounded strictly in the returned rows.

The explanation may only cite numbers that actually appear in the result rows
(plus the row count). It must never invent figures — this is the anti-hallucination
guarantee that makes the engine trustworthy.
"""
from __future__ import annotations
from typing import Dict, List


def explain(question: str, rows: List[Dict]) -> str:
    """Return a short business explanation of `rows` answering `question`.

    Restates the question, then states the figures straight from the rows and the
    number of matching records. Grounding contract: every numeric token is either a
    value present in `rows` or the integer row count — no invented numbers.
    """
    question = question.strip()
    if not rows:
        return f'No rows matched "{question}", so there is no figure to report.'

    count = len(rows)
    noun = "record" if count == 1 else "records"
    facts = "; ".join(
        ", ".join(f"{column} = {value}" for column, value in row.items())
        for row in rows
    )
    return f'Answering "{question}": {facts} (grounded in {count} matching {noun}).'
