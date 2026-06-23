from pathlib import Path

from healthcare_guardrails_demo.fixture_loader import disallowed_values, load_fixture_bundle

SAMPLE_MANIFEST = Path("fixtures/sample/manifest.json")


def test_sample_fixture_manifest_loads() -> None:
    bundle = load_fixture_bundle(SAMPLE_MANIFEST)

    assert bundle.fixture_id == "prior_auth_001"
    assert bundle.document_type == "prior_authorization_request"
    assert bundle.source["patient_name"] == "Morgan Testpatient"
    assert bundle.expected["expected_policy_decision"] == "human_review_required"


def test_disallowed_values_include_canaries_and_withheld_source_values() -> None:
    bundle = load_fixture_bundle(SAMPLE_MANIFEST)

    values = disallowed_values(bundle)

    assert "PHI_CANARY_PRIOR_AUTH_001" in values
    assert "Morgan Testpatient" in values
    assert "FAKE-MEMBER-042" in values
