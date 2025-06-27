"""Shared orchestration primitives for async agent workflows."""

from __future__ import annotations

import asyncio
import time
import logging
from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Coroutine, Dict, Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class WorkflowStepError(RuntimeError):
    """Raised when a workflow step fails."""


class BaseWorkflow(ABC):
    """A minimal async workflow base-class.

    Sub-classes should implement ``async run()`` and call ``await self.step(...)``
    for each logical phase so we get automatic timing, tracing, and error
    propagation.
    """

    # Name is used for queue routing & registry lookup
    name: str = "base"

    def __init__(self, run_id: str, *, trace: Optional[Callable[[Dict[str, Any]], None]] = None, **context: Any):
        self.run_id = run_id
        self.ctx: Dict[str, Any] = context
        self._trace = trace or (lambda payload: None)

    # ---------------------------------------------------------------------
    # Public API – subclasses must override ``run``
    # ---------------------------------------------------------------------

    @abstractmethod
    async def run(self) -> Any:  # noqa: D401 – imperative mood is fine
        """Execute the workflow – must be implemented by subclass."""

    # ------------------------------------------------------------------
    # Helper for consistent step logging / tracing
    # ------------------------------------------------------------------

    async def step(self, name: str, coro: Awaitable[Any]) -> Any:  # noqa: D401
        start = time.perf_counter()
        self._publish_status(name, "running")

        try:
            result = await coro
        except Exception as exc:  # noqa: BLE001 – propagate after logging
            duration = time.perf_counter() - start
            logger.exception("step_failed", extra={"run_id": self.run_id, "step": name, "duration": duration})
            self._publish_status(name, "failed", error=str(exc), duration=duration)
            raise WorkflowStepError(name) from exc
        else:
            duration = time.perf_counter() - start
            logger.info("step_completed", extra={"run_id": self.run_id, "step": name, "duration": duration})
            self._publish_status(name, "completed", duration=duration)
            return result

    # ------------------------------------------------------------------
    # Internal utilities
    # ------------------------------------------------------------------

    def _publish_status(self, step: str, state: str, **payload: Any) -> None:
        """Send status dict to tracer (used for Supabase realtime / OpenAI trace)."""
        message = {
            "run_id": self.run_id,
            "workflow": self.name,
            "step": step,
            "state": state,
            **payload,
        }
        # Hook for DB updates / websocket push – injected by queue runner
        self._trace(message) 