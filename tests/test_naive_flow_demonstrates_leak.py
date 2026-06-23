import json
from pathlib import Path

from healthcare_guardrails_demo.fixture_loader import load_fixture_bundle
from healthcare_guardrails_demo.naive_flow import run_naive_flow

SAMPLE_MANIFEST = Path("fixtures/sample/manifest.json")


def test_naive_flow_demonstrates_fake_sensitive_value_leak() -> None:
    bundle = load_fixture_bundle(SAMPLE_MANIFEST)
    output = run_naive_flow(bundle)
    serialized = json.dumps(output, sort_keys=True)

    assert output["leak_detected"] is True
    assert "PHI_CANARY_PRIOR_AUTH_001" in serialized
    assert "FAKE-MEMBER-042" in serialized
