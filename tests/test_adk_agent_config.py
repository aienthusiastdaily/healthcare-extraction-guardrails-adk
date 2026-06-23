import importlib.util
import json
from pathlib import Path

from google.adk.models.lite_llm import LiteLlm


def _load_agent_module():
    agent_path = Path(__file__).parents[1] / "app" / "agent.py"
    spec = importlib.util.spec_from_file_location("healthcare_guardrails_adk_agent", agent_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_adk_agent_uses_openai_litellm_by_default() -> None:
    agent_module = _load_agent_module()

    assert isinstance(agent_module.root_agent.model, LiteLlm)
    assert agent_module.root_agent.model.model == agent_module.DEFAULT_OPENAI_LITELLM_MODEL
    assert agent_module.root_agent.model.model.startswith("openai/")


def test_agent_workflow_summary_matches_eval_expected_response() -> None:
    agent_module = _load_agent_module()
    eval_path = (
        Path(__file__).parents[1] / "tests" / "eval" / "evalsets" / "core_guardrails_eval.json"
    )
    eval_set = json.loads(eval_path.read_text(encoding="utf-8"))
    expected_text = eval_set["eval_cases"][0]["conversation"][0]["final_response"]["parts"][0][
        "text"
    ]

    assert agent_module.WORKFLOW_SUMMARY == expected_text
