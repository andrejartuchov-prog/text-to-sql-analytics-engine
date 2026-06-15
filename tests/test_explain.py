"""The business explanation is grounded strictly in the returned rows.

This is the anti-hallucination guarantee: every number in the explanation must
come from the result rows (or the row count / the question), never be invented.
"""
import re

from textsql.explain import explain


def _numbers(text):
    return set(re.findall(r"\d+(?:\.\d+)?", text))


def _grounded_numbers(rows, question):
    allowed = {str(len(rows))}
    for row in rows:
        for value in row.values():
            if isinstance(value, (int, float)):
                allowed.add(str(value))
                if isinstance(value, float) and value.is_integer():
                    allowed.add(str(int(value)))
    return allowed | _numbers(question)


def test_cites_the_actual_figure():
    rows = [{"total_revenue": 1500.0}]
    out = explain("What were total sales on 2026-06-14?", rows)
    assert "1500" in out


def test_no_invented_numbers():
    rows = [{"total_revenue": 1500.0}]
    question = "What were total sales?"
    out = explain(question, rows)
    invented = [n for n in _numbers(out) if n not in _grounded_numbers(rows, question)]
    assert not invented, f"explanation invented numbers absent from rows: {invented}"


def test_empty_result_has_no_invented_numbers():
    question = "Which products are out of stock?"
    out = explain(question, [])
    invented = [n for n in _numbers(out) if n not in _grounded_numbers([], question)]
    assert not invented, f"explanation invented numbers for an empty result: {invented}"
    assert out.strip(), "explanation should still say something for an empty result"
