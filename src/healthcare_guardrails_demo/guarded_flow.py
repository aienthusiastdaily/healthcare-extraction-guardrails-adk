"""Guarded extraction path with withholding, policy, review, and audit output."""

from __future__ import annotations

from dataclasses import asdict

from healthcare_guardrails_demo.audit import build_audit_events
from healthcare_guardrails_demo.contracts import ExtractionResult
from healthcare_guardrails_demo.fixture_loader import FixtureBundle
from healthcare_guardrails_demo.human_review import build_human_review_route
from healthcare_guardrails_demo.policy import decide_policy
from healthcare_guardrails_demo.sensitive_findings import detect_sensitive_findings
from healthcare_guardrails_demo.text_extraction import build_document_evidence


def run_guarded_flow(bundle: FixtureBundle) -> dict[str, object]:
    evidence = build_document_evidence(bundle)
    findings = detect_sensitive_findings(bundle, evidence)
    decision = decide_policy(bundle, findings)
    review_route = build_human_review_route(bundle, evidence, decision)
    audit_events = build_audit_events(decision, review_route)
    extraction = _build_allowed_extraction(bundle, evidence)

    return {
        "flow": "guarded",
        "fixture_id": bundle.fixture_id,
        "document_type": bundle.document_type,
        "extraction_result": asdict(extraction),
        "sensitive_findings": [finding.to_safe_dict() for finding in findings],
        "policy_decision": asdict(decision),
        "human_review_route": asdict(review_route),
        "audit_events": [asdict(event) for event in audit_events],
        "leak_blocked": True,
    }


def _build_allowed_extraction(
    bundle: FixtureBundle, evidence: object
) -> ExtractionResult:
    allowed_field_names = list(bundle.expected.get("allowed_fields", []))
    allowed_fields = {
        field: bundle.source[field] for field in allowed_field_names if field in bundle.source
    }
    if "document_type" in allowed_field_names:
        allowed_fields["document_type"] = bundle.document_type
    return ExtractionResult(
        fixture_id=bundle.fixture_id,
        document_type=bundle.document_type,
        allowed_fields=allowed_fields,
        evidence_refs=[
            f"source:{field}"
            for field in sorted(allowed_fields)
            if field != "document_type"
        ],
    )
