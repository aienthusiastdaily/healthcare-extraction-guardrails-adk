# Examples

Article-ready snippets generated from the deterministic CLI demo.

The first examples show:

- one naive output that visibly leaks a fake canary
- one guarded output that preserves operational fields without raw sensitive
  values
- one policy decision
- one audit trace

Regenerate them with:

```bash
uv run healthcare-guardrails-demo run-naive \
  --fixture fixtures/sample/manifest.json \
  --out examples/naive_leak_output.json

uv run healthcare-guardrails-demo run-guarded \
  --fixture fixtures/sample/manifest.json \
  --out examples/guarded_safe_output.json \
  --policy-out examples/policy_decision.json \
  --audit-out examples/audit_trace.json
```
