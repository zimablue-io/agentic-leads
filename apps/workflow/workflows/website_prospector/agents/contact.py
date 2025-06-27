"""Contact agent for the website prospector."""

from agents import Agent

from workflows.website_prospector.tools.contact import extract_contact_info

# Define the agent
contact_agent = Agent(
    name="Contact Extraction Agent",
    instructions="""You are a contact information specialist. Your job is to extract 
    relevant contact details from prospect websites so we can reach out to them. 
    Use the extract_contact_info tool to gather emails, phones, and contact pages.""",
    tools=[extract_contact_info]
)