import json
from pathlib import Path

from healthcare_guardrails_demo.fixture_loader import disallowed_values, load_fixture_bundle

SAMPLE_MANIFEST = Path("fixtures/sample/manifest.json")
EXAMPLES = Path("examples")


def test_article_examples_show_naive_leak_and_guarded_containment() -> None:
    bundle = load_fixture_bundle(SAMPLE_MANIFEST)
    naive = json.loads((EXAMPLES / "naive_leak_output.json").read_text(encoding="utf-8"))
    guarded = json.loads((EXAMPLES / "guarded_safe_output.json").read_text(encoding="utf-8"))
    policy = json.loads((EXAMPLES / "policy_decision.json").read_text(encoding="utf-8"))
    audit = json.loads((EXAMPLES / "audit_trace.json").read_text(encoding="utf-8"))

    assert naive["leak_detected"] is True
    assert "PHI_CANARY_PRIOR_AUTH_001" in json.dumps(naive, sort_keys=True)
    assert guarded["leak_blocked"] is True
    assert policy["action"] == "human_review"
    assert audit[0]["step"] == "sensitive_value_detection"

    guarded_surfaces = json.dumps(
        {"guarded": guarded, "policy": policy, "audit": audit}, sort_keys=True
    )
    for value in disallowed_values(bundle):
        assert value not in guarded_surfaces
