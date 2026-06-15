"""LLM adapter boundary: NL prompt -> SQL string.

The real client calls Claude; tests inject a mock implementing the same tiny
interface, so all engine logic is verified offline with no network.
"""
from __future__ import annotations
import re
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
        # Lazy import: the offline test suite uses a mock and never loads the SDK.
        import anthropic

        client = anthropic.Anthropic(api_key=self._api_key)
        message = client.messages.create(
            model=self.model,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(
            block.text for block in message.content if getattr(block, "type", None) == "text"
        )
        return _strip_sql(text)


def _strip_sql(text: str) -> str:
    """Pull a bare SQL statement out of the model reply (drop ```sql fences)."""
    fenced = re.search(r"```(?:sql)?\s*(.+?)```", text, re.IGNORECASE | re.DOTALL)
    return (fenced.group(1) if fenced else text).strip()
