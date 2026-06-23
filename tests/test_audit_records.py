import json
from pathlib import Path

from healthcare_guardrails_demo.fixture_loader import disallowed_values, load_fixture_bundle
from healthcare_guardrails_demo.guarded_flow import run_guarded_flow

SAMPLE_MANIFEST = Path("fixtures/sample/manifest.json")


def test_audit_records_explain_decisions_without_raw_sensitive_values() -> None:
    bundle = load_fixture_bundle(SAMPLE_MANIFEST)
    output = run_guarded_flow(bundle)
    events = output["audit_events"]
    serialized_events = json.dumps(events, sort_keys=True)

    assert [event["step"] for event in events] == [
        "sensitive_value_detection",
        "policy_decision",
        "human_review_routing",
    ]
    assert events[0]["withheld_count"] > 0
    for value in disallowed_values(bundle):
        assert value not in serialized_events
