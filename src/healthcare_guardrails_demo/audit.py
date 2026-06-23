"""Safe audit event generation."""

from __future__ import annotations

from healthcare_guardrails_demo.contracts import AuditEvent, HumanReviewRoute, PolicyDecision


def build_audit_events(
    decision: PolicyDecision, review_route: HumanReviewRoute
) -> list[AuditEvent]:
    withheld_count = len(decision.withheld_fields)
    return [
        AuditEvent(
            event_id="audit-001",
            step="sensitive_value_detection",
            decision="detected_restricted_values",
            safe_message=f"Detected {withheld_count} restricted fields for policy review.",
            evidence_refs=review_route.evidence_refs,
            withheld_count=withheld_count,
        ),
        AuditEvent(
            event_id="audit-002",
            step="policy_decision",
            decision=decision.action,
            safe_message=decision.reason,
            evidence_refs=[],
            withheld_count=withheld_count,
        ),
        AuditEvent(
            event_id="audit-003",
            step="human_review_routing",
            decision="queued_for_review",
            safe_message=(
                f"Routed to {review_route.queue} with raw sensitive values withheld."
            ),
            evidence_refs=[],
            withheld_count=withheld_count,
        ),
    ]
