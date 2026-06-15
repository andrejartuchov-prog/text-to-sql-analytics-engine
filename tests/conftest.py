"""Shared fixtures for the offline test suite.

These test files are the PO-authored quality spec and are IMMUTABLE during
make-green: the executor brings the production code to GREEN without touching them.
"""
import pathlib
import pytest

from textsql.config import load_config

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def config():
    return load_config(str(ROOT / "config.example.yaml"))


@pytest.fixture
def schema(config):
    return config.schema


@pytest.fixture
def seed_sql():
    return (FIXTURES / "seed.sql").read_text()


@pytest.fixture
def conn(seed_sql):
    from textsql.db import connect_seeded
    c = connect_seeded(seed_sql)
    try:
        yield c
    finally:
        c.close()


class FixedLLM:
    """Test double for the LLM adapter: returns a canned SQL for any prompt and
    records the prompt it was given (so engine wiring is verified offline)."""

    def __init__(self, sql: str):
        self.sql = sql
        self.last_prompt = None

    def generate_sql(self, prompt: str) -> str:
        self.last_prompt = prompt
        return self.sql
