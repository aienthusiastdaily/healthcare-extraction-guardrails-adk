import json
from pathlib import Path

from healthcare_guardrails_demo.fixture_loader import disallowed_values, load_fixture_bundle
from healthcare_guardrails_demo.guarded_flow import run_guarded_flow

SAMPLE_MANIFEST = Path("fixtures/sample/manifest.json")


def test_human_review_route_is_safe_and_actionable() -> None:
    bundle = load_fixture_bundle(SAMPLE_MANIFEST)
    output = run_guarded_flow(bundle)
    route = output["human_review_route"]
    serialized_route = json.dumps(route, sort_keys=True)

    assert route["queue"] == "Prior authorization review"
    assert "member_id" in route["withheld_fields"]
    assert "restricted fields were withheld" in route["safe_summary"]
    for value in disallowed_values(bundle):
        assert value not in serialized_route
