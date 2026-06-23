"""ADK-facing agent for the healthcare guardrails demo."""

from __future__ import annotations

import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types as genai_types

DEFAULT_OPENAI_LITELLM_MODEL = "openai/gpt-4o-mini"
WORKFLOW_SUMMARY = (
    "The workflow loads a synthetic fixture manifest, runs a naive flow to show "
    "a fake sensitive-value leak, detects synthetic sensitive findings, "
    "withholds disallowed fields from guarded output, routes restricted cases "
    "to human review, and writes safe audit events."
)


def describe_guardrail_workflow() -> dict[str, object]:
    """Describe the deterministic guardrail workflow implemented by this repo."""

    return {
        "status": "success",
        "workflow": [
            "load fixture manifest and expected contract",
            "run naive flow to demonstrate a fake sensitive-value leak",
            "detect synthetic sensitive findings",
            "withhold disallowed fields from guarded public output",
            "route restricted cases to human review",
            "write safe audit events without raw sensitive values",
        ],
    }


root_agent = Agent(
    name="healthcare_extraction_guardrails",
    model=LiteLlm(model=os.getenv("OPENAI_ADK_MODEL", DEFAULT_OPENAI_LITELLM_MODEL)),
    description="Explains and runs a healthcare document extraction guardrails proof.",
    instruction=(
        "You help inspect a public-safe healthcare extraction guardrails demo. "
        "Use the available tool to explain the deterministic workflow. "
        "Do not claim HIPAA compliance or legal certification. "
        "Use language such as compliance-aware, supports compliance controls, "
        "PHI/PII containment, human-review routing, and audit trace. "
        "When asked to describe the workflow, call describe_guardrail_workflow "
        f"first, then reply with exactly this sentence and no extra text: {WORKFLOW_SUMMARY}"
    ),
    generate_content_config=genai_types.GenerateContentConfig(temperature=0),
    tools=[describe_guardrail_workflow],
)
