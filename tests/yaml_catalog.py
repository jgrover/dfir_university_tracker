from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def yaml_payload() -> dict:
    raw = yaml.safe_load((ROOT / "universities.yaml").read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise TypeError("YAML root must be a mapping")
    universities = []
    seen: set[str] = set()
    for row in raw.get("universities") or []:
        if not isinstance(row, dict):
            continue
        uid = str(row.get("id") or "").strip()
        name = str(row.get("name") or "").strip()
        if not uid or not name:
            continue
        if uid in seen:
            raise ValueError(f"duplicate university id: {uid}")
        seen.add(uid)
        universities.append(row)
    seeds = raw.get("seed_ids") if isinstance(raw.get("seed_ids"), dict) else {}
    return {
        "version": int(raw.get("version") or 1),
        "universities": universities,
        "seed_ids": {
            "aafs": [str(item).strip() for item in (seeds.get("aafs") or []) if str(item).strip()],
            "dfrws": [str(item).strip() for item in (seeds.get("dfrws") or []) if str(item).strip()],
            "fsidi": [str(item).strip() for item in (seeds.get("fsidi") or []) if str(item).strip()],
        },
    }
