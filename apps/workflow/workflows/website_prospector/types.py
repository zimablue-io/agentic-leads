"""Type definitions for the website prospector workflow."""

from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, HttpUrl, Field


class ProspectStatus(str, Enum):
    """Status of a prospect in the pipeline."""
    DISCOVERED = "discovered"
    ANALYZED = "analyzed"
    PITCHED = "pitched"
    RESPONDED = "responded"
    CLOSED = "closed"


class AudienceType(str, Enum):
    """Types of target audiences."""
    LOCAL_BUSINESS = "local_business"
    ECOMMERCE = "ecommerce"
    SAAS = "saas"


class Prospect(BaseModel):
    """A potential client prospect."""
    url: HttpUrl
    business_name: str
    industry: Optional[str] = None
    location: Optional[str] = None
    contact_email: Optional[str] = None
    phone: Optional[str] = None
    discovered_at: datetime = Field(default_factory=datetime.now)
    status: ProspectStatus = ProspectStatus.DISCOVERED


class SiteAnalysis(BaseModel):
    """Analysis results for a website."""
    url: HttpUrl
    outdated_score: float = Field(ge=0.0, le=1.0)
    mobile_score: float = Field(ge=0.0, le=1.0)
    performance_score: float = Field(ge=0.0, le=1.0)
    seo_score: float = Field(ge=0.0, le=1.0)
    security_score: float = Field(ge=0.0, le=1.0)
    overall_score: float = Field(ge=0.0, le=1.0)
    improvement_areas: List[str] = Field(default_factory=list)
    technical_issues: List[str] = Field(default_factory=list)
    screenshot_paths: List[str] = Field(default_factory=list)
    analyzed_at: datetime = Field(default_factory=datetime.now)


class ImprovementSuggestion(BaseModel):
    """A specific improvement suggestion."""
    category: str
    title: str
    description: str
    priority: str  # "high", "medium", "low"
    estimated_impact: str
    implementation_difficulty: str
    estimated_cost_range: tuple[int, int]


class Proposal(BaseModel):
    """Generated proposal for a prospect."""
    prospect_url: HttpUrl
    improvements: List[ImprovementSuggestion]
    executive_summary: str
    estimated_total_cost: tuple[int, int]
    estimated_timeline: str
    proposal_tone: str
    generated_at: datetime = Field(default_factory=datetime.now)


class AudienceConfig(BaseModel):
    """Configuration for a target audience."""
    description: str = ""
    audience_type: AudienceType
    search_patterns: List[str]
    keywords: List[str]  # services, products, or industries
    scoring_weights: Dict[str, float]
    improvement_focuses: List[str]
    budget_range: tuple[int, int]
    pitch_tone: str
    max_prospects_per_run: int = 50


class WorkflowState(BaseModel):
    """State of the prospecting workflow."""
    target_config: AudienceConfig
    prospects: List[Prospect] = Field(default_factory=list)
    analyzed_sites: List[tuple[Prospect, SiteAnalysis]] = Field(default_factory=list)
    generated_proposals: List[tuple[Prospect, Proposal]] = Field(default_factory=list)
    sent_pitches: List[Dict[str, Any]] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    run_id: str = Field(default_factory=lambda: f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
