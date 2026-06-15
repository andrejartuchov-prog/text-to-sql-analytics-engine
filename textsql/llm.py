"""LLM adapter boundary: NL prompt -> SQL string.

The real client calls Claude; tests inject a mock implementing the same tiny
interface, so all engine logic is verified offline with no network.

STUB — production code intentionally incomplete (RED). Executor implements ClaudeClient.
"""
from __future__ import annotations
from typing import Protocol


class LLMClient(Protocol):
    def generate_sql(self, prompt: str) -> str:
        """Given a schema-aware prompt, return a single SQL SELECT statement."""
        ...


class ClaudeClient:
    """Real adapter over the Anthropic SDK. Default model: latest Claude.

    Model id is supplied from config (e.g. ``claude-opus-4-8``). The network call
    lives only here, behind the LLMClient interface, so the rest of the engine is
    offline-testable.
    """

    def __init__(self, model: str, api_key: str | None = None):
        self.model = model
        self._api_key = api_key

    def generate_sql(self, prompt: str) -> str:
        # STUB: real implementation calls the Anthropic Messages API and returns
        # the SQL from the model response. Not exercised by the offline test suite.
        raise NotImplementedError("ClaudeClient.generate_sql is implemented in make-green")
