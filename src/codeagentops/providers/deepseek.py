from __future__ import annotations

import time

import httpx

from codeagentops.config import Settings
from codeagentops.models import LLMResult, LLMUsage


class DeepSeekProvider:
    """Minimal DeepSeek Chat Completions client.

    DeepSeek exposes an OpenAI-compatible chat completions API.
    This provider intentionally supports only the MVP path: one model,
    one synchronous request, and usage metadata when returned.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self.base_url = "https://api.deepseek.com/chat/completions"

    def complete(self, messages: list[dict[str, str]], temperature: float = 0.1) -> LLMResult:
        headers = {
            "Authorization": f"Bearer {self.settings.deepseek_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.settings.deepseek_model,
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }
        start = time.perf_counter()
        with httpx.Client(timeout=self.settings.request_timeout_s) as client:
            response = client.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        latency_s = time.perf_counter() - start

        content = data["choices"][0]["message"]["content"]
        raw_usage = data.get("usage") or {}
        usage = LLMUsage(
            prompt_tokens=int(raw_usage.get("prompt_tokens") or 0),
            completion_tokens=int(raw_usage.get("completion_tokens") or 0),
            total_tokens=int(raw_usage.get("total_tokens") or 0),
        )
        usage.estimated_cost_usd = (
            usage.prompt_tokens / 1_000_000 * self.settings.input_cost_per_1m_tokens
            + usage.completion_tokens / 1_000_000 * self.settings.output_cost_per_1m_tokens
        )
        return LLMResult(content=content, latency_s=latency_s, usage=usage, model=self.settings.deepseek_model)
