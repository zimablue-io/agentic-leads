"""Main workflow orchestrator for the website prospecting agents."""

import asyncio
import os
from typing import List, Optional
from pathlib import Path

from agents import Agent, Runner, function_tool
from pydantic import BaseModel

from website_prospector.models.types import (
    Prospect, SiteAnalysis, AudienceConfig, WorkflowState
)
from website_prospector.config.audience_configs import AUDIENCE_CONFIGS
from website_prospector.tools.site_analyzer import SiteAnalyzer

from dotenv import load_dotenv

# Load environment variables from .env (searching parent directories)
load_dotenv(dotenv_path=Path(__file__).resolve().parent / '.env', override=False)

# Use the hosted WebSearchTool built into the Agents SDK
from agents import WebSearchTool

class ProspectSearchResult(BaseModel):
    """Result from prospect search."""
    prospects: List[Prospect]
    search_query: str
    audience_used: str


class AnalysisResult(BaseModel):
    """Result from site analysis."""
    analysis: SiteAnalysis
    improvement_suggestions: List[str]


class ContactInfo(BaseModel):
    """Contact information extracted from website."""
    emails: List[str] = []
    phones: List[str] = []
    contact_page_url: Optional[str] = None
    social_links: List[str] = []


# Tool implementations
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


@function_tool
async def analyze_prospect_website(prospect_url: str) -> AnalysisResult:
    """Analyze a prospect's website for improvement opportunities."""
    # Create a Prospect object for analysis
    prospect = Prospect(url=prospect_url, business_name="Unknown")
    
    # Default scoring weights
    scoring_weights = {
        'mobile_responsiveness': 0.25,
        'performance': 0.25,
        'seo': 0.20,
        'security': 0.15,
        'outdated': 0.15
    }
    
    analyzer = SiteAnalyzer()
    analysis = await analyzer.analyze_site(prospect, scoring_weights)
    
    if not analysis:
        raise ValueError(f"Failed to analyze website: {prospect_url}")
    
    # Generate improvement suggestions based on analysis
    suggestions = []
    if analysis.mobile_score < 0.7:
        suggestions.append("Implement responsive design for mobile devices")
    if analysis.performance_score < 0.7:
        suggestions.append("Optimize page load speeds and reduce resource sizes")
    if analysis.seo_score < 0.7:
        suggestions.append("Improve SEO with better meta tags and content structure")
    if analysis.security_score < 0.7:
        suggestions.append("Upgrade to HTTPS and implement security headers")
    if analysis.outdated_score < 0.7:
        suggestions.append("Modernize design and update content")
    
    return AnalysisResult(
        analysis=analysis,
        improvement_suggestions=suggestions
    )


@function_tool
async def extract_contact_info(prospect_url: str) -> ContactInfo:
    """Extract contact information from a prospect's website."""
    import re
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(prospect_url, wait_until='networkidle', timeout=30000)
            content = await page.content()
            
            # Extract emails
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = list(set(re.findall(email_pattern, content)))
            
            # Extract phone numbers (basic pattern)
            phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
            phones = list(set([f"({match[0]}) {match[1]}-{match[2]}" for match in re.findall(phone_pattern, content)]))
            
            # Look for contact page
            contact_links = await page.query_selector_all('a[href*="contact"]')
            contact_page_url = None
            if contact_links:
                href = await contact_links[0].get_attribute('href')
                if href:
                    from urllib.parse import urljoin
                    contact_page_url = urljoin(prospect_url, href)
            
            # Look for social media links
            social_patterns = ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com']
            social_links = []
            for pattern in social_patterns:
                social_elements = await page.query_selector_all(f'a[href*="{pattern}"]')
                for element in social_elements:
                    href = await element.get_attribute('href')
                    if href and href not in social_links:
                        social_links.append(href)
            
            return ContactInfo(
                emails=emails[:5],  # Limit to 5 emails
                phones=phones[:3],  # Limit to 3 phones
                contact_page_url=contact_page_url,
                social_links=social_links[:5]  # Limit to 5 social links
            )
            
        finally:
            await browser.close()


# Define the agents
search_agent = Agent(
    name="Prospect Search Agent",
    instructions="""You are a prospect discovery specialist. Your job is to find potential 
    clients who have outdated websites that could benefit from redesign services. 
    Use the search_prospects_for_audience tool to find prospects based on the specified audience type.""",
    tools=[search_prospects_for_audience]
)

analysis_agent = Agent(
    name="Website Analysis Agent", 
    instructions="""You are a website analysis expert. Your job is to thoroughly analyze 
    prospect websites to identify improvement opportunities. Use the analyze_prospect_website 
    tool to get detailed analysis and suggestions.""",
    tools=[analyze_prospect_website]
)

contact_agent = Agent(
    name="Contact Extraction Agent",
    instructions="""You are a contact information specialist. Your job is to extract 
    relevant contact details from prospect websites so we can reach out to them. 
    Use the extract_contact_info tool to gather emails, phones, and contact pages.""",
    tools=[extract_contact_info]
)

coordinator_agent = Agent(
    name="Workflow Coordinator",
    instructions="""You are the main coordinator for the website prospecting workflow. 
    You orchestrate the entire process:
    1. First, hand off to the search agent to find prospects
    2. Then, hand off to the analysis agent to analyze their websites  
    3. Finally, hand off to the contact agent to extract contact information
    
    Coordinate the workflow and provide a summary of the results.""",
    handoffs=[search_agent, analysis_agent, contact_agent]
)


async def run_prospect_workflow(audience_name: str, location: str = "San Francisco", max_prospects: int = 3):
    """Run the complete prospect discovery and analysis workflow."""
    
    print(f"🚀 Starting prospect workflow for {audience_name} in {location}")
    print(f"📊 Max prospects to process: {max_prospects}")
    print("-" * 60)
    
    # Check if audience exists
    if audience_name not in AUDIENCE_CONFIGS:
        available = ", ".join(AUDIENCE_CONFIGS.keys())
        print(f"❌ Unknown audience: {audience_name}")
        print(f"Available audiences: {available}")
        return
    
    workflow_prompt = f"""
    Please execute the complete prospect discovery workflow:
    
    1. Search for {max_prospects} prospects in the "{audience_name}" audience located in {location}
    2. Analyze each prospect's website for improvement opportunities
    3. Extract contact information for each prospect
    
    Provide a comprehensive summary of findings including:
    - Number of prospects found
    - Key improvement opportunities identified
    - Contact information gathered
    - Recommendations for outreach
    """
    
    try:
        result = await Runner.run(coordinator_agent, workflow_prompt)
        print("✅ Workflow completed successfully!")
        print("\n" + "="*60)
        print("📋 WORKFLOW RESULTS:")
        print("="*60)
        print(result.final_output)
        
    except Exception as e:
        print(f"❌ Workflow failed: {e}")
        raise


async def main():
    """Main entry point for testing the workflow."""
    
    # Set up environment
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set your OPENAI_API_KEY environment variable")
        return
    
    print("🏢 Available audiences:")
    for name, config in AUDIENCE_CONFIGS.items():
        print(f"  • {name}: {config.description}")
    
    print("\n" + "="*60)
    print("🧪 RUNNING BASIC POC TEST")
    print("="*60)
    
    # Run a test workflow with local businesses
    await run_prospect_workflow(
        audience_name="local_business",
        location="Johannesburg", 
        max_prospects=1  # Start small for testing
    )


if __name__ == "__main__":
    asyncio.run(main()) 