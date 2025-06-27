"""Extract contact information from a prospect's website."""

import re
from playwright.async_api import async_playwright
from typing import List, Optional
from pathlib import Path

from agents import Agent, Runner, function_tool
from pydantic import BaseModel

from workflows.website_prospector.types import (
    Prospect, SiteAnalysis, AudienceConfig, WorkflowState
)
from workflows.website_prospector.config.audience_configs import AUDIENCE_CONFIGS
from workflows.website_prospector.tools.site_analyzer import SiteAnalyzer


class ContactInfo(BaseModel):
    """Contact information extracted from website."""
    emails: List[str] = []
    phones: List[str] = []
    contact_page_url: Optional[str] = None
    social_links: List[str] = []


@function_tool
async def extract_contact_info(prospect_url: str) -> ContactInfo:
    """Extract contact information from a prospect's website."""
    
    
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
