"""Sensitive value detection for synthetic fixture evidence."""

from __future__ import annotations

from healthcare_guardrails_demo.contracts import DocumentEvidence, SensitiveFinding
from healthcare_guardrails_demo.fixture_loader import FixtureBundle


def detect_sensitive_findings(
    bundle: FixtureBundle, evidence: DocumentEvidence
) -> list[SensitiveFinding]:
    withheld_fields = set(bundle.expected.get("expected_withheld_fields", []))
    sensitive_fields = set(bundle.expected.get("sensitive_fields", []))
    findings: list[SensitiveFinding] = []

    for span in evidence.evidence_spans:
        if span.field in sensitive_fields or span.field in withheld_fields:
            findings.append(
                SensitiveFinding(
                    finding_type="sensitive_field",
                    field=span.field,
                    value=span.text,
                    evidence_ref=span.ref,
                    severity="restricted",
                    expected_handling="withheld"
                    if span.field in withheld_fields
                    else "review_required",
                )
            )

    for canary in evidence.source_canaries:
        if canary:
            findings.append(
                SensitiveFinding(
                    finding_type="canary",
                    field="canary",
                    value=canary,
                    evidence_ref="source:canary",
                    severity="restricted",
                    expected_handling="withheld",
                )
            )

    return _dedupe_findings(findings)


def _dedupe_findings(findings: list[SensitiveFinding]) -> list[SensitiveFinding]:
    seen: set[tuple[str, str, str]] = set()
    unique: list[SensitiveFinding] = []
    for finding in findings:
        key = (finding.finding_type, finding.field, finding.value)
        if key in seen:
            continue
        seen.add(key)
        unique.append(finding)
    return unique
