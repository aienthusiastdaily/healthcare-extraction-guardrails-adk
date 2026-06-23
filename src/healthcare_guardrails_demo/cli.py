"""CLI for the healthcare guardrails demo."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from healthcare_guardrails_demo.fixture_loader import load_fixture_bundle
from healthcare_guardrails_demo.guarded_flow import run_guarded_flow
from healthcare_guardrails_demo.naive_flow import run_naive_flow

app = typer.Typer(no_args_is_help=True)
console = Console(stderr=True)


@app.command("generate-fixtures")
def generate_fixtures_command(
    template: Annotated[str, typer.Option("--template")] = "healthcare/prior_auth",
    count: Annotated[int, typer.Option("--count", min=1)] = 3,
    out: Annotated[Path, typer.Option("--out")] = Path("fixtures/generated"),
    seed: Annotated[int, typer.Option("--seed")] = 42,
    variants: Annotated[str, typer.Option("--variants")] = "text-layer,scanned",
) -> None:
    """Generate deterministic synthetic fixtures with the branded package."""

    try:
        from aienthusiastdaily_fixtures.generate import generate_fixtures
    except ImportError as exc:  # pragma: no cover - exercised only without dependency install
        raise typer.BadParameter(
            "Install aienthusiastdaily-fixtures before generating fixtures."
        ) from exc

    manifest = generate_fixtures(
        template=template,
        count=count,
        out_dir=out,
        seed=seed,
        variants=tuple(part.strip() for part in variants.split(",") if part.strip()),
    )
    console.print(f"[green]Generated fixtures:[/green] {out / manifest['manifest_path']}")


@app.command("run-naive")
def run_naive_command(
    fixture: Annotated[Path, typer.Option("--fixture")],
    out: Annotated[Path, typer.Option("--out")] = Path("outputs/naive_leak_output.json"),
    fixture_id: Annotated[str | None, typer.Option("--fixture-id")] = None,
) -> None:
    """Run the intentionally unsafe extraction path."""

    bundle = load_fixture_bundle(fixture, fixture_id=fixture_id)
    _write_json(out, run_naive_flow(bundle))
    console.print(f"[yellow]Naive output written:[/yellow] {out}")


@app.command("run-guarded")
def run_guarded_command(
    fixture: Annotated[Path, typer.Option("--fixture")],
    out: Annotated[Path, typer.Option("--out")] = Path("outputs/guarded_safe_output.json"),
    policy_out: Annotated[Path, typer.Option("--policy-out")] = Path(
        "outputs/policy_decision.json"
    ),
    audit_out: Annotated[Path, typer.Option("--audit-out")] = Path("outputs/audit_trace.json"),
    fixture_id: Annotated[str | None, typer.Option("--fixture-id")] = None,
) -> None:
    """Run the guarded extraction path."""

    bundle = load_fixture_bundle(fixture, fixture_id=fixture_id)
    result = run_guarded_flow(bundle)
    _write_json(out, result)
    _write_json(policy_out, result["policy_decision"])
    _write_json(audit_out, result["audit_events"])
    console.print(f"[green]Guarded output written:[/green] {out}")


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    app()
