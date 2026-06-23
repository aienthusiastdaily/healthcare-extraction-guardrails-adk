from pathlib import Path

from healthcare_guardrails_demo.fixture_loader import load_fixture_bundle
from healthcare_guardrails_demo.guarded_flow import run_guarded_flow

SAMPLE_MANIFEST = Path("fixtures/sample/manifest.json")


def test_policy_decision_matches_expected_human_review_route() -> None:
    bundle = load_fixture_bundle(SAMPLE_MANIFEST)
    output = run_guarded_flow(bundle)

    decision = output["policy_decision"]
    assert decision["action"] == "human_review"
    assert decision["surface"] == "public_summary"
    assert "member_id" in decision["withheld_fields"]
    assert "Sensitive synthetic values" in decision["reason"]
