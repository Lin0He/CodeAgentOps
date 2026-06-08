from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    deepseek_api_key: str
    deepseek_model: str = "deepseek-chat"
    input_cost_per_1m_tokens: float = 0.27
    output_cost_per_1m_tokens: float = 1.10
    request_timeout_s: float = 120.0


@dataclass(frozen=True)
class RunConfig:
    tasks_dir: Path
    runs_dir: Path
    max_iterations: int = 3
    llm_timeout_s: float = 120.0
    pytest_timeout_s: float = 20.0
    forbid_test_edits: bool = True


def load_settings() -> Settings:
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is missing. Copy .env.example to .env and set it.")
    return Settings(
        deepseek_api_key=api_key,
        deepseek_model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        input_cost_per_1m_tokens=float(os.getenv("DEEPSEEK_INPUT_COST_PER_1M_TOKENS", "0.27")),
        output_cost_per_1m_tokens=float(os.getenv("DEEPSEEK_OUTPUT_COST_PER_1M_TOKENS", "1.10")),
    )
