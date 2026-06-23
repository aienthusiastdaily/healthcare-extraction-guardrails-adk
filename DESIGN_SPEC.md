# DESIGN_SPEC: Healthcare Extraction Guardrails ADK Companion Repo

## Status

Draft seed for AGE-42. This file is the source design spec for the future public
companion repo:

```text
https://github.com/aienthusiastdaily/healthcare-extraction-guardrails-adk
```

It lives in this private landing-page branch until the public companion repo is
created.

## Purpose

Build a small, reproducible ADK companion repo that demonstrates why healthcare
document extraction needs controlled workflow boundaries.

The repo should compare:

1. A naive extraction flow that can leak fake PHI/PII-like values into an output
   surface.
2. A guarded flow that detects sensitive values, applies structured policy,
   withholds or redacts disallowed fields, routes uncertain cases to human
   review, and writes safe audit records.

This is a proof artifact for an AI Enthusiast Daily article. It is not a
production healthcare system and must not contain real PHI, real PII, real
client data, real patient records, or copied completed clinical text.

## Positioning Guardrails

Use:

- compliance-aware
- supports compliance controls
- PHI/PII containment
- human-review routing
- audit trace
- structured validation

Avoid:

- HIPAA compliant
- guaranteed compliance
- safe for real patient data
- certified healthcare workflow
- real patient examples

## Inputs

The repo consumes synthetic fixtures from:

```text
https://github.com/aienthusiastdaily/aienthusiastdaily-fixtures
```

Install dependency before PyPI publication:

```bash
uv add "aienthusiastdaily-fixtures @ git+https://github.com/aienthusiastdaily/aienthusiastdaily-fixtures.git@v0.1.0"
```

Generate a deterministic fixture set:

```bash
uv run aienthusiastdaily-fixtures generate \
  --template healthcare/prior_auth \
  --count 3 \
  --out fixtures/generated \
  --seed 42 \
  --variants text-layer,scanned
```

The first pass should use text-layer PDFs or extracted fixture text so the
guardrail loop is proven before OCR complexity is added. Scanned PDF/OCR support
can follow after the core contracts and tests exist.

## Expected Demo Commands

Target local commands:

```bash
uv sync
uv run healthcare-guardrails-demo generate-fixtures --seed 42
uv run healthcare-guardrails-demo run-naive --fixture fixtures/generated/manifest.json
uv run healthcare-guardrails-demo run-guarded --fixture fixtures/generated/manifest.json
uv run pytest
```

The exact CLI names may change during implementation, but the repo must keep one
documented command path for generating fixtures, running both flows, and running
tests.

## High-Level Architecture

```text
synthetic fixtures
  -> fixture loader
  -> naive flow
       -> unsafe summary/output sample
  -> guarded flow
       -> document evidence
       -> extraction contract
       -> sensitive finding detector
       -> validation
       -> policy decision
       -> safe operational output
       -> human-review route when needed
       -> audit event stream
```

The naive flow exists only to make the failure mode visible. The guarded flow is
the proof artifact.

## Proposed Repo Layout

```text
healthcare-extraction-guardrails-adk/
  README.md
  DESIGN_SPEC.md
  pyproject.toml
  fixtures/
    README.md
  outputs/
    README.md
  src/
    healthcare_guardrails_demo/
      __init__.py
      cli.py
      contracts.py
      fixture_loader.py
      text_extraction.py
      naive_flow.py
      guarded_flow.py
      sensitive_findings.py
      validation.py
      policy.py
      human_review.py
      audit.py
  tests/
    test_fixture_loading.py
    test_naive_flow_demonstrates_leak.py
    test_guarded_outputs_do_not_leak_sensitive_values.py
    test_policy_decisions.py
    test_human_review_routing.py
    test_audit_records.py
  examples/
    README.md
    naive_leak_output.json
    guarded_safe_output.json
    policy_decision.json
    audit_trace.json
```

## Contract Model

### DocumentEvidence

Records what document was processed and which evidence snippets support
extraction.

Fields:

- `fixture_id`
- `document_type`
- `source_path`
- `variant`
- `evidence_spans`
- `source_canaries`

### ExtractionResult

Contains allowed operational fields only.

Examples:

- `document_type`
- `requested_action`
- `service_category`
- `provider_category`
- `submission_channel`
- `date_bucket`
- `routing_hint`
- `evidence_refs`

### SensitiveFinding

Represents fake sensitive values detected in evidence.

Fields:

- `finding_type`
- `value`
- `canary_id`
- `evidence_ref`
- `severity`
- `expected_handling`

### ValidationError

Records missing, contradictory, or unsafe extraction states.

Fields:

- `field`
- `rule`
- `message`
- `evidence_ref`
- `remediation_hint`

### PolicyDecision

Determines how the workflow handles each output surface.

Allowed decisions:

- `allow`
- `redact`
- `withhold`
- `human_review`

### HumanReviewRoute

Keeps the handoff useful without exposing disallowed values.

Fields:

- `queue`
- `reason`
- `safe_summary`
- `withheld_fields`
- `evidence_refs`

### AuditEvent

Records what the workflow did without leaking the sensitive value into a public
or downstream surface.

Fields:

- `event_id`
- `step`
- `decision`
- `safe_message`
- `evidence_refs`
- `withheld_count`

### DemoRunReport

Points to all generated artifacts from a run.

Fields:

- `fixture_manifest`
- `naive_output_path`
- `guarded_output_path`
- `policy_output_path`
- `audit_trace_path`
- `leak_detected_in_naive_output`
- `leak_blocked_in_guarded_output`

## Sensitive-Value Policy

Disallowed in guarded public outputs:

- fake patient names
- fake dates of birth
- fake member IDs
- fake phone numbers
- fake addresses
- fake claim IDs when marked sensitive
- diagnosis-like text when marked sensitive
- fixture canaries such as `PHI_CANARY_PRIOR_AUTH_001`

Allowed when normalized and operationally useful:

- document type
- broad service category
- requested action category
- provider category
- routing queue
- validation status
- policy decision
- withheld field names
- evidence references that do not contain the sensitive value

## Tests

Required first-pass tests:

- generated fixture manifest can be loaded
- naive flow output contains at least one expected fake sensitive canary
- guarded public output contains no canaries
- guarded public output contains no disallowed fake sensitive values from the
  fixture expected contract
- policy decisions match expected handling from fixture contracts
- human-review route includes a safe reason and withheld field names
- audit events include decisions and counts without raw sensitive values

The leak tests should fail loudly if any guarded output surface includes a
canary or known fake sensitive value.

## Article Outputs

The repo should produce small, stable artifacts that can be copied into the
article or screenshotted:

- one naive leak JSON snippet
- one guarded safe JSON snippet
- one policy decision JSON snippet
- one audit trace JSON snippet
- one terminal command sequence
- one test output showing leak prevention checks passing

## Non-Goals

- Real PHI/PII ingestion.
- Real healthcare form reproduction.
- Compliance certification.
- Production deployment.
- Broad document-management features.
- Full OCR pipeline in the first pass.

## Acceptance Gate Before Implementation

Implementation should not begin until:

- this spec is reviewed against AGE-42
- the companion repo name is confirmed or updated
- the first fixture template for the demo is selected
- the public-safe data boundary is confirmed
- the initial test list is accepted
