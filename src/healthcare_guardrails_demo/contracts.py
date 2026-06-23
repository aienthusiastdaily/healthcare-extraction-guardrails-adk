"""Structured contracts for the healthcare guardrails demo."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal

PolicyAction = Literal["allow", "redact", "withhold", "human_review"]


@dataclass(frozen=True)
class EvidenceSpan:
    ref: str
    field: str
    text: str


@dataclass(frozen=True)
class DocumentEvidence:
    fixture_id: str
    document_type: str
    source_path: str
    variant: str
    evidence_spans: list[EvidenceSpan]
    source_canaries: list[str]

    def safe_refs(self) -> list[str]:
        return [span.ref for span in self.evidence_spans]


@dataclass(frozen=True)
class ExtractionResult:
    fixture_id: str
    document_type: str
    allowed_fields: dict[str, str]
    evidence_refs: list[str]


@dataclass(frozen=True)
class SensitiveFinding:
    finding_type: str
    field: str
    value: str
    evidence_ref: str
    severity: str
    expected_handling: str

    def to_safe_dict(self) -> dict[str, str]:
        return {
            "finding_type": self.finding_type,
            "field": self.field,
            "evidence_ref": self.evidence_ref,
            "severity": self.severity,
            "expected_handling": self.expected_handling,
        }


@dataclass(frozen=True)
class ValidationError:
    field: str
    rule: str
    message: str
    evidence_ref: str
    remediation_hint: str


@dataclass(frozen=True)
class PolicyDecision:
    action: PolicyAction
    surface: str
    reason: str
    withheld_fields: list[str] = field(default_factory=list)
    redacted_fields: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class HumanReviewRoute:
    queue: str
    reason: str
    safe_summary: str
    withheld_fields: list[str]
    evidence_refs: list[str]


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    step: str
    decision: str
    safe_message: str
    evidence_refs: list[str] = field(default_factory=list)
    withheld_count: int = 0


@dataclass(frozen=True)
class DemoRunReport:
    fixture_manifest: str
    naive_output_path: str | None = None
    guarded_output_path: str | None = None
    policy_output_path: str | None = None
    audit_trace_path: str | None = None
    leak_detected_in_naive_output: bool = False
    leak_blocked_in_guarded_output: bool = False


def dataclass_to_dict(value: object) -> object:
    """Convert nested dataclasses into plain JSON-serializable structures."""

    return asdict(value)
