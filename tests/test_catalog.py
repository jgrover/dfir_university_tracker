from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from yaml_to_json import convert, normalize_catalog  # noqa: E402


def test_ids_are_unique_and_required() -> None:
    payload = json.loads((ROOT / "universities.json").read_text(encoding="utf-8"))
    ids = [row["id"] for row in payload["universities"]]
    assert ids
    assert all(row.get("name") for row in payload["universities"])
    assert len(ids) == len(set(ids))


def test_seed_ids_refer_to_universities() -> None:
    payload = json.loads((ROOT / "universities.json").read_text(encoding="utf-8"))
    known = {row["id"] for row in payload["universities"]}
    seeds = payload["seed_ids"]
    for key in ("aafs", "dfrws", "fsidi"):
        missing = [uid for uid in seeds[key] if uid not in known]
        assert not missing, missing


def test_yaml_converts_to_json() -> None:
    generated = convert(ROOT / "universities.yaml", ROOT / "universities.json")
    on_disk = json.loads((ROOT / "universities.json").read_text(encoding="utf-8"))
    assert generated == on_disk
    assert generated["version"] == 1
    assert len(generated["universities"]) >= 80
