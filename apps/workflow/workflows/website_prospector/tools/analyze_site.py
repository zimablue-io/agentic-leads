"""Analyze a prospect's website for improvement opportunities."""

from typing import List
from agents import Agent, function_tool
from pydantic import BaseModel

from workflows.website_prospector.types import (
    Prospect, SiteAnalysis 
)
from workflows.website_prospector.tools.site_analyzer import SiteAnalyzer


class AnalysisResult(BaseModel):
    """Result from site analysis."""
    analysis: SiteAnalysis
    improvement_suggestions: List[str]

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
 