"""Utilities to run agentic workflows without hitting external LLMs.

Set the env-var ``AGENTIC_OFFLINE=1`` or pass ``--offline`` to the CLI runner
and call ``apply_offline_patches()`` before invoking Agents SDK.
"""

from __future__ import annotations

import asyncio
import os
import random
from typing import Any

from agents import Runner


class _MockRunResult:  # Minimal shim of agents.run.RunResult
    def __init__(self, final_output: Any):
        self.final_output = final_output


def _gen_mock_urls(n: int = 5) -> str:
    base_domains = ["example", "acme", "foobar", "loremipsum", "mocksite"]
    random.shuffle(base_domains)
    lines = [f"https://{d}.com" for d in base_domains[:n]]
    return "\n".join(lines)


async def _mock_run(agent, prompt: str, *args, **kwargs):  # type: ignore[override]
    """Very naive stub that inspects prompt to decide what to return."""
    prompt_lower = prompt.lower()
    if "analyse" in prompt_lower or "analyze" in prompt_lower:
        mock_json = {
            "overall_score": round(random.uniform(0.4, 0.8), 2),
            "mobile_score": 0.7,
            "performance_score": 0.6,
        }
        return _MockRunResult(str(mock_json))
    if "extract contact" in prompt_lower:
        return _MockRunResult('{"emails": ["info@example.com"], "phones": ["+123456789"]}')
    # default: prospect search
    return _MockRunResult(_gen_mock_urls())


def apply_offline_patches() -> None:
    """Monkey-patch Runner.run to avoid real network calls."""

    # Only patch once.
    if getattr(Runner.run, "_is_patched", False):
        return

    async def patched_run(*args, **kwargs):  # type: ignore[override]
        return await _mock_run(*args, **kwargs)

    patched_run._is_patched = True  # type: ignore[attr-defined]
    Runner.run = patched_run  # type: ignore[assignment]


# Convenience to auto-apply based on env-var at import-time
if os.getenv("AGENTIC_OFFLINE") == "1":
    apply_offline_patches()
