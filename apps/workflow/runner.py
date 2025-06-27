"""Generic CLI runner for agentic workflows.

Usage:
    uv run apps/workflow/runner.py website_prospector --audience local_business --location Johannesburg --max 2
"""

from __future__ import annotations

import argparse
import asyncio
import uuid
import sys
from pathlib import Path

# Ensure project root is on PYTHONPATH so that `apps.*` absolute imports work
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agentic_core.logging import configure_logging
from agentic_core.orchestrator import BaseWorkflow
from workflows import get_workflow_class


async def _main() -> None:
    parser = argparse.ArgumentParser(description="Run an Agentic workflow")
    parser.add_argument("workflow", help="Workflow name (e.g. website_prospector)")
    parser.add_argument("--audience", default="local_business")
    parser.add_argument("--location", default="San Francisco")
    parser.add_argument("--max", type=int, default=5, dest="max_prospects")
    parser.add_argument("--offline", action="store_true", help="Run without hitting external LLM APIs")
    args = parser.parse_args()

    if args.offline:
        from agentic_core.offline import apply_offline_patches

        apply_offline_patches()

    configure_logging()

    run_id = str(uuid.uuid4())

    WorkflowCls = get_workflow_class(args.workflow)
    wf: BaseWorkflow = WorkflowCls(run_id=run_id, audience_name=args.audience, location=args.location, max_prospects=args.max_prospects)

    result = await wf.run()
    print("\n=== WORKFLOW SUMMARY ===")
    print(result)


if __name__ == "__main__":
    asyncio.run(_main()) 