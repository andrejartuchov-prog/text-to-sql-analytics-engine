"""Load the YAML config (schema + KPIs + model id) into a Config object.

STUB — production code intentionally incomplete (RED). Executor implements.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict

from .schema import Schema


@dataclass
class Config:
    schema: Schema
    kpis: Dict[str, str] = field(default_factory=dict)
    model: str = ""


def load_config(path: str) -> Config:
    """Parse a YAML config file into Config(schema, kpis, model).

    Expected YAML shape:
        schema:
          <table>: [<col>, <col>, ...]
        kpis:
          <name>: <definition/sql>
        model: <model-id>
    """
    # STUB: return an empty config so tests are RED.
    return Config(schema=Schema({}), kpis={}, model="")
