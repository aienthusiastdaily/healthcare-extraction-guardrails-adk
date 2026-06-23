"""Naive extraction path that intentionally leaks synthetic sensitive values."""

from __future__ import annotations

from healthcare_guardrails_demo.fixture_loader import FixtureBundle, disallowed_values


def run_naive_flow(bundle: FixtureBundle) -> dict[str, object]:
    leaked_values = disallowed_values(bundle)
    unsafe_summary = (
        f"{bundle.document_type} for {bundle.source.get('patient_name', 'unknown patient')} "
        f"uses member ID {bundle.source.get('member_id', 'unknown member')} and canary "
        f"{bundle.source.get('canary', 'missing canary')}. Requested service: "
        f"{bundle.source.get('requested_service', 'unknown service')}."
    )
    return {
        "flow": "naive",
        "fixture_id": bundle.fixture_id,
        "document_type": bundle.document_type,
        "unsafe_summary": unsafe_summary,
        "leaked_values": leaked_values,
        "leak_detected": bool(leaked_values),
    }
