# Healthcare Extraction Guardrails ADK Demo

Public-safe companion repo seed for the AI Enthusiast Daily article on
compliance-aware healthcare document extraction workflows.

This demo compares two paths over synthetic healthcare-like fixtures:

1. A naive extraction flow that leaks fake PHI/PII-like values into an output
   surface.
2. A guarded flow that detects sensitive values, withholds or redacts disallowed
   fields, routes the case to human review, and writes safe audit records.

No real PHI, real PII, real patient records, or real client data belong in this
repo.

Public repository:

```text
https://github.com/aienthusiastdaily/healthcare-extraction-guardrails-adk
```

## Install

```bash
uv sync
```

## Environment

The repo includes `.env.temp`, a public-safe template loaded by the Makefile for
all script targets. Copy it to `.env` for local credentials:

```bash
cp .env.temp .env
```

Set `OPENAI_API_KEY` in `.env` before running ADK evals. `.env` is ignored by
Git, while `.env.temp` keeps the expected variable names and safe defaults in
the public repo.

Before the fixture package is published to PyPI, the project depends on the
tagged GitHub package:

```bash
uv add "aienthusiastdaily-fixtures @ git+https://github.com/aienthusiastdaily/aienthusiastdaily-fixtures.git@v0.1.0"
```

## Generate Fixtures

```bash
uv run healthcare-guardrails-demo generate-fixtures --seed 42
```

The command writes a deterministic fixture set under `fixtures/generated/`.

## Run The Demo

Run the intentionally unsafe flow:

```bash
uv run healthcare-guardrails-demo run-naive --fixture fixtures/generated/manifest.json
```

Run the guarded flow:

```bash
uv run healthcare-guardrails-demo run-guarded --fixture fixtures/generated/manifest.json
```

For local development without generated PDFs, use the committed sample manifest:

```bash
uv run healthcare-guardrails-demo run-naive --fixture fixtures/sample/manifest.json
uv run healthcare-guardrails-demo run-guarded --fixture fixtures/sample/manifest.json
```

## Test

```bash
make test
```

The tests assert that:

- the sample fixture manifest loads
- the naive flow leaks a fake canary
- guarded public output contains allowed operational fields
- guarded public output contains no canaries or withheld fake sensitive values
- policy, human-review, and audit outputs explain the containment decision

## Public Export

This repo is prepared as an allowlisted public snapshot from the private AI
Enthusiast Daily planning repo. From the private source checkout, the public
candidate can be produced with:

```bash
uv run python scripts/public_export.py sync \
  ../healthcare-extraction-guardrails-adk \
  --config companion-repo/healthcare-extraction-guardrails/public_export.toml \
  --source-root companion-repo/healthcare-extraction-guardrails \
  --apply
```

The export config excludes local environments, caches, generated check outputs,
and ADK eval history.

## Evaluate

ADK eval cases live under `tests/eval/`.

```bash
make eval
```

The first eval is intentionally small. It asks the ADK-facing agent to describe
the guardrail workflow and expects the `describe_guardrail_workflow` tool to be
used. The ADK-facing agent runs OpenAI through LiteLLM and defaults to
`openai/gpt-4o-mini`. Provide `OPENAI_API_KEY` in the shell or local `.env`
before running evals. To override the model, set `OPENAI_ADK_MODEL` to another
OpenAI LiteLLM model name.

The Make target fails fast when credentials are missing and checks ADK's
generated eval result JSON so failed cases do not appear green just because the
CLI process exited successfully.

## ADK Shape

The first implementation keeps the proof loop deterministic so tests can run
without model credentials. `app/agent.py` defines the ADK-facing root agent and
tool used by the initial ADK eval once `google-adk`, LiteLLM, and OpenAI model
credentials are available.
