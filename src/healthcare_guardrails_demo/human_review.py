"""Human-review routing without leaking raw sensitive values."""

from __future__ import annotations

from healthcare_guardrails_demo.contracts import DocumentEvidence, HumanReviewRoute, PolicyDecision
from healthcare_guardrails_demo.fixture_loader import FixtureBundle


def build_human_review_route(
    bundle: FixtureBundle, evidence: DocumentEvidence, decision: PolicyDecision
) -> HumanReviewRoute:
    queue = bundle.source.get("routing_queue", "document exception review")
    return HumanReviewRoute(
        queue=queue,
        reason=decision.reason,
        safe_summary=(
            f"{bundle.document_type} fixture {bundle.fixture_id} requires review "
            f"because {len(decision.withheld_fields)} restricted fields were withheld."
        ),
        withheld_fields=decision.withheld_fields,
        evidence_refs=evidence.safe_refs(),
    )
