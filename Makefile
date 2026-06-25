ENV_FILE ?= .env
ENV_TEMPLATE ?= .env.temp
UV_ENV_FILES := --env-file $(ENV_TEMPLATE)
ifneq (,$(wildcard $(ENV_FILE)))
UV_ENV_FILES += --env-file $(ENV_FILE)
endif
UV_RUN := uv run $(UV_ENV_FILES)

.PHONY: test lint eval demo-naive demo-guarded

test:
	$(UV_RUN) pytest

lint:
	$(UV_RUN) ruff check .

eval:
	@$(UV_RUN) python -c 'import os, sys; ok = bool(os.getenv("OPENAI_API_KEY")); print("make eval requires OPENAI_API_KEY in the shell or local .env for the ADK LiteLLM OpenAI model.", file=sys.stderr) if not ok else None; sys.exit(0 if ok else 2)'
	@$(UV_RUN) python -c 'import os; print("Running ADK eval with " + os.getenv("OPENAI_ADK_MODEL", "openai/gpt-4o-mini") + " through LiteLLM.")'
	$(UV_RUN) adk eval ./app tests/eval/evalsets/core_guardrails_eval.json --config_file_path=tests/eval/eval_config.json --print_detailed_results
	$(UV_RUN) python scripts/assert_latest_adk_eval_result.py app/.adk/eval_history

demo-naive:
	$(UV_RUN) healthcare-guardrails-demo run-naive --fixture fixtures/sample/manifest.json

demo-guarded:
	$(UV_RUN) healthcare-guardrails-demo run-guarded --fixture fixtures/sample/manifest.json
