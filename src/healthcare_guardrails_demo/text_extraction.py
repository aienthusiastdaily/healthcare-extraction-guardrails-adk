"""Evidence construction for generated synthetic fixture records."""

from __future__ import annotations

from healthcare_guardrails_demo.contracts import DocumentEvidence, EvidenceSpan
from healthcare_guardrails_demo.fixture_loader import FixtureBundle


def build_document_evidence(bundle: FixtureBundle) -> DocumentEvidence:
    spans = [
        EvidenceSpan(ref=f"source:{field}", field=field, text=value)
        for field, value in sorted(bundle.source.items())
    ]
    variants = bundle.fixture.get("variants", {})
    variant = (
        "text_layer_pdf"
        if isinstance(variants, dict) and "text_layer_pdf" in variants
        else "source"
    )
    return DocumentEvidence(
        fixture_id=bundle.fixture_id,
        document_type=bundle.document_type,
        source_path=bundle.source_path.relative_to(bundle.root).as_posix(),
        variant=variant,
        evidence_spans=spans,
        source_canaries=[str(value) for value in bundle.expected.get("sensitive_canaries", [])],
    )
