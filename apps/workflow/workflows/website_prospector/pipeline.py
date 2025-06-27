"""Coordinator pipeline for Website Prospector workflow."""

from __future__ import annotations

import asyncio
from typing import Any, List
from agents import Runner
from supabase_io import (
    create_workflow_run,
    insert_prospects,
    insert_site_analyses,
    insert_contacts,
    complete_workflow_run,
    fail_workflow_run,
)

from agentic_core.orchestrator import BaseWorkflow
from workflows.website_prospector.agents import analysis_agent, contact_agent, search_agent


class Workflow(BaseWorkflow):
    """Website Prospector implementation using the new BaseWorkflow."""

    name = "website_prospector"

    def __init__(
        self,
        run_id: str,
        audience_name: str,
        location: str = "San Francisco",
        max_prospects: int = 5,
        **ctx: Any,
    ) -> None:
        super().__init__(run_id, **ctx)
        self.audience_name = audience_name
        self.location = location
        self.max_prospects = max_prospects

    # --------------------------------------------------------- public API
    async def run(self) -> Any:  # noqa: D401
        """Execute prospect → analysis → contact extraction flow."""
        # Insert / mark workflow run in DB
        db_run_id = create_workflow_run(self.audience_name, self.location)

        try:
            # Step 1 – Search
            search_prompt = (
                f"Search for up to {self.max_prospects} prospects in the '{self.audience_name}' "
                f"audience located in {self.location}. Return ONLY website URLs."
            )
            prospects_result = await self.step(
                "search",
                Runner.run(search_agent, search_prompt, max_turns=3),
            )

            # Extract URL list from agent output
            urls: List[str] = [
                line.strip()
                for line in str(prospects_result.final_output).splitlines()
                if line.strip().startswith("http")
            ][: self.max_prospects]

            analyses: list[str] = []
            for url in urls:
                resp = await self.step(
                    "analysis",
                    Runner.run(
                        analysis_agent,
                        f"Please analyse the website at {url} and return a JSON object with key metrics.",
                        max_turns=3,
                    ),
                )
                analyses.append(str(resp.final_output))

            contacts: list[str] = []
            for url in urls:
                resp_c = await self.step(
                    "contacts",
                    Runner.run(
                        contact_agent,
                        f"Extract contact info for {url} and respond in JSON format.",
                        max_turns=3,
                    ),
                )
                contacts.append(str(resp_c.final_output))

            # Persist into DB
            insert_prospects(db_run_id, urls)
            insert_site_analyses(urls, analyses)
            insert_contacts(urls, contacts)
            complete_workflow_run(db_run_id)

            summary = {
                "prospects": urls,
                "analyses": analyses,
                "contacts": contacts,
            }
            return summary

        except Exception as exc:
            fail_workflow_run(db_run_id)
            raise 