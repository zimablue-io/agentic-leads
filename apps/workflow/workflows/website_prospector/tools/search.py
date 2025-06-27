"""Wrap the existing search tool so we don't duplicate code yet."""

from typing import List
from agents import Agent, Runner, function_tool, WebSearchTool
from pydantic import BaseModel

from workflows.website_prospector.types import (
    Prospect, SiteAnalysis, AudienceConfig, WorkflowState
)
from workflows.website_prospector.config.audience_configs import AUDIENCE_CONFIGS

class ProspectSearchResult(BaseModel):
    """Result from prospect search."""
    prospects: List[Prospect]
    search_query: str
    audience_used: str

@function_tool
async def search_prospects_for_audience(audience_name: str, location: str = "San Francisco") -> ProspectSearchResult:
    """Search for prospects based on audience configuration using the built-in WebSearchTool."""
    if audience_name not in AUDIENCE_CONFIGS:
        raise ValueError(f"Unknown audience: {audience_name}")
    
    config = AUDIENCE_CONFIGS[audience_name]
    
    # Build a query list from patterns & keywords
    queries: list[str] = []
    for pattern in config.search_patterns:
        for kw in config.keywords:
            queries.append(pattern.format(keyword=kw, location=location))

    # Use an ad-hoc agent equipped with the hosted WebSearchTool
    search_agent = Agent(
        name="Built-in Search Agent",
        instructions=(
            "You are a prospect discovery assistant.\n"
            "For each search query provided, call the WebSearchTool to retrieve results.\n"
            "Return ONLY a newline-separated list of full website URLs (no additional text)."
        ),
        tools=[WebSearchTool()],
    )

    prospects: list[Prospect] = []
    max_per_query = 5

    for q in queries:
        # Ask the agent for URLs
        prompt = (
            f"Search query: {q}\n"
            f"Please provide up to {max_per_query} distinct business website URLs only."
        )
        try:
            result = await Runner.run(search_agent, prompt, max_turns=3)
            urls = [line.strip() for line in str(result.final_output).splitlines() if line.strip().startswith("http")]
            for u in urls:
                prospects.append(
                    Prospect(
                        url=u,
                        business_name=u.split("//")[-1].split("/")[0],
                        industry=audience_name,
                        location=location,
                    )
                )
        except Exception:
            # Continue on any search error
            continue

    # Deduplicate by URL
    unique = {}
    for p in prospects:
        if str(p.url) not in unique:
            unique[str(p.url)] = p

    prospects_list = list(unique.values())[: config.max_prospects_per_run]

    return ProspectSearchResult(
        prospects=prospects_list,
        search_query=f"{audience_name} in {location}",
        audience_used=audience_name
    )
