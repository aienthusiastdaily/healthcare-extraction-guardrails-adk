.PHONY: test lint eval demo-naive demo-guarded

test:
	uv run pytest

lint:
	uv run ruff check .

eval:
	@if [ -z "$$GOOGLE_API_KEY" ] && [ "$$GOOGLE_GENAI_USE_VERTEXAI" != "TRUE" ]; then \
		echo "make eval requires GOOGLE_API_KEY or GOOGLE_GENAI_USE_VERTEXAI=TRUE with Vertex AI config."; \
		exit 2; \
	fi
	uv run adk eval ./app tests/eval/evalsets/core_guardrails_eval.json --config_file_path=tests/eval/eval_config.json --print_detailed_results
	uv run python scripts/assert_latest_adk_eval_result.py app/.adk/eval_history

demo-naive:
	uv run healthcare-guardrails-demo run-naive --fixture fixtures/sample/manifest.json

demo-guarded:
	uv run healthcare-guardrails-demo run-guarded --fixture fixtures/sample/manifest.json
