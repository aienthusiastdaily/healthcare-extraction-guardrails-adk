"""ADK-facing agent for the healthcare guardrails demo."""

from __future__ import annotations

from google.adk.agents import Agent


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
    model="gemini-3-flash-preview",
    description="Explains and runs a healthcare document extraction guardrails proof.",
    instruction=(
        "You help inspect a public-safe healthcare extraction guardrails demo. "
        "Use the available tool to explain the deterministic workflow. "
        "Do not claim HIPAA compliance or legal certification. "
        "Use language such as compliance-aware, supports compliance controls, "
        "PHI/PII containment, human-review routing, and audit trace."
    ),
    tools=[describe_guardrail_workflow],
)
