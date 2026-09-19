from __future__ import annotations

from pathlib import Path

from yaml_catalog import yaml_payload

ROOT = Path(__file__).resolve().parents[1]


def test_ids_are_unique_and_required() -> None:
    payload = yaml_payload()
    ids = [str(row["id"]) for row in payload["universities"]]
    assert ids
    assert all(str(row.get("name") or "").strip() for row in payload["universities"])
    assert len(ids) == len(set(ids))
    assert payload["version"] == 1
    assert len(payload["universities"]) >= 80


def test_seed_ids_refer_to_universities() -> None:
    payload = yaml_payload()
    known = {str(row["id"]) for row in payload["universities"]}
    seeds = payload["seed_ids"]
    for key in ("aafs", "dfrws", "fsidi"):
        missing = [uid for uid in seeds[key] if uid not in known]
        assert not missing, missing


def test_json_is_not_published() -> None:
    assert (ROOT / "universities.yaml").is_file()
    assert not (ROOT / "universities.json").exists()
