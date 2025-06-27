"""Website Prospector workflow package (refactored)."""

from workflows.website_prospector.pipeline import Workflow as WebsiteProspectorWorkflow  # noqa: F401

def get_workflow(*args, **kwargs):  # type: ignore[override]
    """Factory used by the runner registry."""
    return WebsiteProspectorWorkflow(*args, **kwargs) 