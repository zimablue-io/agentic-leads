"""Deterministic (non-LLM) variant of the prospecting workflow that writes results
straight into Supabase tables.

This bypasses the Agents orchestration and calls the existing tool functions
programmatically so we have structured data for each step.
"""
from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Dict, Any

from website_prospector.config.audience_configs import AUDIENCE_CONFIGS
from website_prospector.models.types import Prospect

from supabase_io import supabase
from main import (
    search_prospects_for_audience,
    analyze_prospect_website,
    extract_contact_info,
)


def _insert(table: str, payload: Dict[str, Any]):
    resp = supabase.table(table).insert(payload).execute()
    if getattr(resp, "error", None):
        raise RuntimeError(resp.error)
    return resp.data[0]


async def run_workflow_to_db(
    *,
    run_id: str,
    audience_name: str,
    location: str,
    max_prospects: int = 5,
):
    if audience_name not in AUDIENCE_CONFIGS:
        raise ValueError(f"Unknown audience: {audience_name}")

    # Update run status → running
    supabase.table("workflow_runs").update({"status": "running", "started_at": datetime.utcnow().isoformat()}).eq("id", run_id).execute()

    # 1. Search prospects
    search_result = await search_prospects_for_audience(audience_name, location)

    for prospect in search_result.prospects[:max_prospects]:
        # Insert prospect row
        prospect_row = _insert(
            "prospects",
            {
                "workflow_run_id": run_id,
                "url": str(prospect.url),
                "source_query": search_result.search_query,
                "created_at": datetime.utcnow().isoformat(),
            },
        )
        prospect_id = prospect_row["id"] if isinstance(prospect_row, dict) else prospect_row[0]["id"]

        # 2. Analyze website
        analysis_result = await analyze_prospect_website(str(prospect.url))
        _insert(
            "site_analyses",
            {
                "prospect_id": prospect_id,
                "scores_json": analysis_result.analysis.model_dump(),
                "tech_issues_json": analysis_result.analysis.technical_issues,
                "analyzed_at": datetime.utcnow().isoformat(),
            },
        )

        # 3. Extract contacts
        contact_info = await extract_contact_info(str(prospect.url))
        for email in contact_info.emails:
            _insert(
                "contacts",
                {
                    "prospect_id": prospect_id,
                    "type": "email",
                    "value": email,
                },
            )
        for phone in contact_info.phones:
            _insert(
                "contacts",
                {
                    "prospect_id": prospect_id,
                    "type": "phone",
                    "value": phone,
                },
            )
        for link in contact_info.social_links:
            _insert(
                "contacts",
                {
                    "prospect_id": prospect_id,
                    "type": "social",
                    "value": link,
                },
            )

    # Mark run completed
    supabase.table("workflow_runs").update({"status": "completed", "finished_at": datetime.utcnow().isoformat()}).eq("id", run_id).execute() 