"""Search agent for the website prospector."""

from agents import Agent

from workflows.website_prospector.tools.search import search_prospects_for_audience

# Define the agent
search_agent = Agent(
    name="Prospect Search Agent",
    instructions="""You are a prospect discovery specialist. Your job is to find potential 
    clients who have outdated websites that could benefit from redesign services. 
    Use the search_prospects_for_audience tool to find prospects based on the specified audience type.""",
    tools=[search_prospects_for_audience]
)