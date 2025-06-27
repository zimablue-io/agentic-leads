"""Queue-driven worker that executes the prospect workflow.

Run locally with:

    uv run python worker.py

The worker consumes messages from the `worker_jobs` pgmq queue in Supabase.
A message is expected to be JSON of the form:

    {
        "run_id": "<uuid of workflow_runs row>",
        "audience_name": "local_business",  # must exist in AUDIENCE_CONFIGS
        "location": "San Francisco",
        "max_prospects": 5
    }

The queue guarantees at-least-once delivery. The worker ACKs the message
only after the workflow completes without raising an exception.
"""
from __future__ import annotations

import asyncio
import os
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# -------------------------------------------------------------------
# Ensure env vars (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, OPENAI_API_KEY)
# are loaded from a local .env before any module accesses them.
# -------------------------------------------------------------------

# Try .env in current dir and two levels up (repo root)
_here = Path(__file__).resolve().parent
load_dotenv(_here / ".env", override=False)
load_dotenv(_here.parent.parent / ".env", override=False)

from supabase_io import JobConsumer
from db_workflow import run_workflow_to_db

# Default overrides
DEFAULT_AUDIENCE = os.getenv("DEFAULT_AUDIENCE", "local_business")
DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "San Francisco")
DEFAULT_MAX_PROSPECTS = int(os.getenv("MAX_PROSPECTS", "5"))


class ProspectWorker(JobConsumer):
    """Consumes jobs from pgmq and runs the workflow synchronously."""

    def handle_job(self, payload: Dict[str, Any]) -> None:  # noqa: D401
        audience_name = payload.get("audience_name", DEFAULT_AUDIENCE)
        location = payload.get("location", DEFAULT_LOCATION)
        max_prospects = int(payload.get("max_prospects", DEFAULT_MAX_PROSPECTS))

        print(
            f"[QUEUE] Received job – audience={audience_name} location={location} max={max_prospects}"
        )

        # Run the async workflow in the event loop and block until done
        asyncio.run(
            run_workflow_to_db(
                run_id=payload.get("run_id"),
                audience_name=audience_name,
                location=location,
                max_prospects=max_prospects,
            )
        )

        print("[QUEUE] Job completed successfully 🌟")


if __name__ == "__main__":
    print("📡 Prospect worker starting – waiting for jobs…")
    ProspectWorker().run_forever() 