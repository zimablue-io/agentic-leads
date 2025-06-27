"""Pre-configured audience targeting configurations."""

from workflows.website_prospector.types import AudienceConfig, AudienceType

AUDIENCE_CONFIGS = {
    "local_business": AudienceConfig(
        description="Local service-based businesses (e.g. plumbers, dentists) in a specific city.",
        audience_type=AudienceType.LOCAL_BUSINESS,
        search_patterns=[
            "{keyword} {location}",
            "{keyword} near me {location}",
            "best {keyword} {location}",
            "{location} {keyword} services"
        ],
        keywords=[
            "plumber", "electrician", "dentist", "lawyer", "accountant", 
            "real estate agent", "contractor", "auto repair", "veterinarian",
            "restaurant", "hair salon", "fitness gym", "chiropractor"
        ],
        scoring_weights={
            "mobile_responsiveness": 0.3,
            "local_seo": 0.25,
            "contact_visibility": 0.2,
            "modern_design": 0.15,
            "page_speed": 0.1
        },
        improvement_focuses=[
            "mobile_optimization", "local_seo", "contact_forms", 
            "google_business_profile", "online_reviews", "call_to_action"
        ],
        budget_range=(1000, 5000),
        pitch_tone="friendly_local",
        max_prospects_per_run=25
    ),
    
    "ecommerce": AudienceConfig(
        description="Small to mid-size e-commerce stores selling physical products online.",
        audience_type=AudienceType.ECOMMERCE,
        search_patterns=[
            "buy {keyword} online",
            "{keyword} online store",
            "{keyword} shop",
            "{keyword} ecommerce"
        ],
        keywords=[
            "jewelry", "clothing", "electronics", "home goods", "books",
            "sporting goods", "beauty products", "pet supplies", "toys"
        ],
        scoring_weights={
            "conversion_optimization": 0.3,
            "page_speed": 0.25,
            "mobile_commerce": 0.2,
            "security": 0.15,
            "modern_design": 0.1
        },
        improvement_focuses=[
            "conversion_rate", "checkout_optimization", "product_pages",
            "payment_security", "mobile_shopping", "search_functionality"
        ],
        budget_range=(3000, 15000),
        pitch_tone="roi_focused",
        max_prospects_per_run=20
    ),
    
    "saas": AudienceConfig(
        description="B2B SaaS companies offering subscription-based software/services.",
        audience_type=AudienceType.SAAS,
        search_patterns=[
            "{keyword} software",
            "{keyword} platform",
            "{keyword} solution",
            "{keyword} tools"
        ],
        keywords=[
            "project management", "crm", "accounting", "hr", "marketing",
            "analytics", "communication", "design", "development"
        ],
        scoring_weights={
            "user_experience": 0.3,
            "conversion_funnel": 0.25,
            "technical_performance": 0.2,
            "modern_design": 0.15,
            "security": 0.1
        },
        improvement_focuses=[
            "signup_flow", "feature_presentation", "social_proof",
            "pricing_clarity", "demo_requests", "user_onboarding"
        ],
        budget_range=(5000, 25000),
        pitch_tone="technical_professional",
        max_prospects_per_run=15
    )
}