"""Load fixture package manifests and expected contracts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class FixtureBundle:
    manifest_path: Path
    root: Path
    manifest: dict[str, Any]
    fixture: dict[str, Any]
    source_path: Path
    expected_path: Path
    source: dict[str, str]
    expected: dict[str, Any]

    @property
    def fixture_id(self) -> str:
        return str(self.fixture["fixture_id"])

    @property
    def document_type(self) -> str:
        return str(self.expected.get("document_type") or self.fixture.get("document_type"))


def load_fixture_bundle(manifest_path: str | Path, fixture_id: str | None = None) -> FixtureBundle:
    path = Path(manifest_path)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    root = path.parent
    fixtures = manifest.get("fixtures")
    if not isinstance(fixtures, list) or not fixtures:
        raise ValueError(f"manifest has no fixtures: {path}")

    selected = _select_fixture(fixtures, fixture_id)
    source_path = root / str(selected["source"])
    expected_path = root / str(selected["expected"])
    if not source_path.exists():
        raise FileNotFoundError(f"fixture source not found: {source_path}")
    if not expected_path.exists():
        raise FileNotFoundError(f"expected contract not found: {expected_path}")

    return FixtureBundle(
        manifest_path=path,
        root=root,
        manifest=manifest,
        fixture=selected,
        source_path=source_path,
        expected_path=expected_path,
        source=_read_flat_yaml(source_path),
        expected=json.loads(expected_path.read_text(encoding="utf-8")),
    )


def disallowed_values(bundle: FixtureBundle) -> list[str]:
    """Return raw values that guarded public outputs must not expose."""

    fields = set(bundle.expected.get("sensitive_fields", [])) | set(
        bundle.expected.get("expected_withheld_fields", [])
    )
    values = [
        str(bundle.source[field])
        for field in sorted(fields)
        if field in bundle.source and str(bundle.source[field]).strip()
    ]
    values.extend(str(value) for value in bundle.expected.get("sensitive_canaries", []))
    return sorted(set(values), key=values.index)


def _select_fixture(fixtures: list[dict[str, Any]], fixture_id: str | None) -> dict[str, Any]:
    if fixture_id is None:
        return fixtures[0]
    for fixture in fixtures:
        if fixture.get("fixture_id") == fixture_id:
            return fixture
    raise ValueError(f"fixture_id not found in manifest: {fixture_id}")


def _read_flat_yaml(path: Path) -> dict[str, str]:
    """Read the flat YAML emitted by the fixture package without extra dependencies."""

    values: dict[str, str] = {}
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"unsupported YAML line {line_number} in {path}: {raw_line!r}")
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values
