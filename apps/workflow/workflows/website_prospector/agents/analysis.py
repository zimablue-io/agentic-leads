"""Analysis agent for the website prospector."""

from agents import Agent

from workflows.website_prospector.tools.analyze_site import analyze_prospect_website

# Define the agent
analysis_agent = Agent(
    name="Website Analysis Agent", 
    instructions="""You are a website analysis expert. Your job is to thoroughly analyze 
    prospect websites to identify improvement opportunities. Use the analyze_prospect_website 
    tool to get detailed analysis and suggestions.""",
    tools=[analyze_prospect_website]
)
