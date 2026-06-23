import json
from pathlib import Path

from healthcare_guardrails_demo.fixture_loader import disallowed_values, load_fixture_bundle
from healthcare_guardrails_demo.guarded_flow import run_guarded_flow

SAMPLE_MANIFEST = Path("fixtures/sample/manifest.json")


def test_guarded_public_output_excludes_disallowed_values() -> None:
    bundle = load_fixture_bundle(SAMPLE_MANIFEST)
    output = run_guarded_flow(bundle)
    serialized = json.dumps(output, sort_keys=True)

    for value in disallowed_values(bundle):
        assert value not in serialized


def test_guarded_public_output_preserves_allowed_operational_fields() -> None:
    bundle = load_fixture_bundle(SAMPLE_MANIFEST)
    output = run_guarded_flow(bundle)

    allowed = output["extraction_result"]["allowed_fields"]
    assert allowed["requested_service"] == "MRI lumbar spine without contrast"
    assert allowed["routing_queue"] == "Prior authorization review"
    assert "member_id" not in allowed
