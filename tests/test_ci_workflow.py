from __future__ import annotations

from pathlib import Path

CI_WORKFLOW = Path(".github/workflows/ci.yml")


def test_ci_secret_scan_allows_public_env_template() -> None:
    workflow = CI_WORKFLOW.read_text(encoding="utf-8")

    assert 'file_name == ".env.temp"' in workflow
    assert "continue" in workflow
    assert r"OPENAI_API_KEY\s*=" in workflow
