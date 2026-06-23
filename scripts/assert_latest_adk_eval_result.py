"""Fail when the latest ADK eval result contains failed cases."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

PASSED_STATUSES = {1, "PASSED", "passed", "EvalStatus.PASSED"}


def _status_label(status: Any) -> str:
    if status == 1:
        return "PASSED"
    if status == 2:
        return "FAILED"
    if status == 3:
        return "NOT_EVALUATED"
    return str(status)


def main() -> int:
    history_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("app/.adk/eval_history")
    result_files = sorted(
        history_dir.glob("*.evalset_result.json"),
        key=lambda path: path.stat().st_mtime,
    )
    if not result_files:
        print(f"No ADK eval result files found in {history_dir}", file=sys.stderr)
        return 2

    latest_result = result_files[-1]
    with latest_result.open(encoding="utf-8") as result_file:
        result = json.load(result_file)

    failed_cases = []
    for case in result.get("eval_case_results", []):
        status = case.get("final_eval_status")
        if status not in PASSED_STATUSES:
            failed_cases.append((case.get("eval_id", "<unknown>"), _status_label(status)))

    if failed_cases:
        print(f"ADK eval failed: {latest_result}", file=sys.stderr)
        for eval_id, status in failed_cases:
            print(f"- {eval_id}: {status}", file=sys.stderr)
        return 1

    case_count = len(result.get("eval_case_results", []))
    print(f"ADK eval passed: {case_count} case(s) in {latest_result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
