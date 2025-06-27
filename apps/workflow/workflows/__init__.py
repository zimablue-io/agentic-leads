"""Registry and helpers for available agentic workflows."""

from importlib import import_module
from typing import Dict, Type

from agentic_core.orchestrator import BaseWorkflow

_WORKFLOW_REGISTRY: Dict[str, str] = {
    "website_prospector": "apps.workflow.workflows.website_prospector",  # module path
}


def get_workflow_class(name: str) -> Type[BaseWorkflow]:
    if name not in _WORKFLOW_REGISTRY:
        raise KeyError(f"Unknown workflow: {name}")
    module_path = _WORKFLOW_REGISTRY[name]
    mod = import_module(f"{module_path}.pipeline")
    return getattr(mod, "Workflow") 