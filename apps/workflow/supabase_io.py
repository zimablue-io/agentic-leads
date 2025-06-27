"""Supabase helper utilities for the workflow worker.

This module centralises all direct calls to Supabase/Postgres so the rest of the
workflow code remains decoupled from the underlying database client.
"""
from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, Optional

from supabase import create_client, Client  # type: ignore

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise RuntimeError("Supabase credentials not configured in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

QUEUE_NAME = "worker_jobs"


def _dequeue_job(visibility_timeout: int = 300) -> Optional[Dict[str, Any]]:
    """Pop a single job off the pgmq queue.

    Returns the job payload dict if a message exists; otherwise None.
    """
    # pgmq.read takes queue_name, vt, limit
    response = supabase.schema("pgmq_public").rpc(
        "pop",
        {
            "queue_name": QUEUE_NAME,
            "vt": visibility_timeout,
        },
    ).execute()
    data = response.data if hasattr(response, "data") else response
    if data and len(data) > 0:
        return data[0]
    return None


def _ack_job(msg_id: int) -> None:
    """Delete a message from the queue after successful processing."""
    supabase.schema("pgmq_public").rpc(
        "delete",
        {
            "queue_name": QUEUE_NAME,
            "msg_id": msg_id,
        },
    ).execute()


class JobConsumer:
    """A simple synchronous job consumer loop."""

    def __init__(self, sleep: float = 2.0):
        self.sleep = sleep

    def run_forever(self) -> None:
        while True:
            job = _dequeue_job()
            if job is None:
                time.sleep(self.sleep)
                continue

            msg_id = job["msg_id"]
            payload: Dict[str, Any] = json.loads(job["message"])
            try:
                self.handle_job(payload)
            except Exception as exc:  # pylint: disable=broad-except
                print(f"Job {msg_id} failed: {exc}")
                # Let message return to queue after vt.
            else:
                _ack_job(msg_id)

    # ------------------------------------------------------------------
    # Override this method in subclasses
    # ------------------------------------------------------------------
    def handle_job(self, payload: Dict[str, Any]) -> None:  # noqa: D401
        """Process a single job payload. Override in subclass."""
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Persistence helpers used by workflows
# ---------------------------------------------------------------------------


def create_workflow_run(audience_name: str, location: str | None = None) -> str:
    """Insert a row into ``workflow_runs`` and return its ID."""
    # Fetch audience id by name
    aud_resp = (
        supabase.table("audiences")
        .select("id")
        .eq("name", audience_name)
        .single()
        .execute()
    )
    aud_id = aud_resp.data["id"] if hasattr(aud_resp, "data") else aud_resp["id"]

    run_resp = (
        supabase.table("workflow_runs")
        .insert({
            "audience_id": aud_id,
            "location": location,
            "status": "running",
        })
        .execute()
    )
    run_id = run_resp.data[0]["id"] if hasattr(run_resp, "data") else run_resp[0]["id"]
    return run_id


def complete_workflow_run(run_id: str) -> None:
    supabase.table("workflow_runs").update({"status": "completed"}).eq("id", run_id).execute()


def fail_workflow_run(run_id: str) -> None:
    supabase.table("workflow_runs").update({"status": "failed"}).eq("id", run_id).execute()


def insert_prospects(run_id: str, urls: list[str]):
    records = [{"workflow_run_id": run_id, "url": u} for u in urls]
    if records:
        supabase.table("prospects").insert(records).execute()


def insert_site_analyses(prospect_urls: list[str], analyses_json: list[str]):
    # expects parallel lists same length
    records = []
    for url, body in zip(prospect_urls, analyses_json, strict=False):
        # Find prospect id by url
        p_resp = supabase.table("prospects").select("id").eq("url", url).single().execute()
        if not p_resp.data:
            continue
        records.append({"prospect_id": p_resp.data["id"], "scores_json": body})
    if records:
        supabase.table("site_analyses").insert(records).execute()


def insert_contacts(prospect_urls: list[str], contacts_json: list[str]):
    for url, body in zip(prospect_urls, contacts_json, strict=False):
        p_resp = supabase.table("prospects").select("id").eq("url", url).single().execute()
        if not p_resp.data:
            continue
        # crude: store full JSON into contacts as a single row type jsonb maybe; else skip
        supabase.table("contacts").insert({"prospect_id": p_resp.data["id"], "type": "json", "value": body}).execute() 