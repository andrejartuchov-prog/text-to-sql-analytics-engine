"""Load the YAML config (schema + KPIs + model id) into a Config object.

Config-driven: the demo schema, KPIs and model live in YAML, so adapting the
engine to a new dataset is a config change, not a code change.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict

import yaml

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
    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    schema = Schema(data.get("schema", {}))
    kpis = data.get("kpis", {})
    model = data.get("model", "")
    return Config(schema=schema, kpis=kpis, model=model)
