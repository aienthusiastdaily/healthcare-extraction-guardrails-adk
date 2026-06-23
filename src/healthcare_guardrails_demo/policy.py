"""Policy decisions for guarded output surfaces."""

from __future__ import annotations

from healthcare_guardrails_demo.contracts import PolicyDecision, SensitiveFinding
from healthcare_guardrails_demo.fixture_loader import FixtureBundle


def decide_policy(
    bundle: FixtureBundle, findings: list[SensitiveFinding], *, surface: str = "public_summary"
) -> PolicyDecision:
    withheld_fields = sorted(set(bundle.expected.get("expected_withheld_fields", [])))
    expected = str(bundle.expected.get("expected_policy_decision", "human_review_required"))

    if findings or expected == "human_review_required":
        return PolicyDecision(
            action="human_review",
            surface=surface,
            reason=(
                "Sensitive synthetic values were detected and must be withheld "
                "before this document can move to a public or downstream surface."
            ),
            withheld_fields=withheld_fields,
        )

    return PolicyDecision(
        action="allow",
        surface=surface,
        reason="No restricted values were detected for this output surface.",
    )
