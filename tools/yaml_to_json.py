#!/usr/bin/env python3
"""Convert universities.yaml (editable source) to universities.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "PyYAML is required for this converter. Install dev deps:\n"
        "  python -m pip install -r requirements-dev.txt\n"
    )
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_YAML = ROOT / "universities.yaml"
DEFAULT_JSON = ROOT / "universities.json"


def _str(value: object) -> str:
    return "" if value is None else str(value)


def normalize_catalog(raw: dict) -> dict:
    if not isinstance(raw, dict):
        raise TypeError("YAML root must be a mapping")
    universities = []
    seen: set[str] = set()
    for row in raw.get("universities") or []:
        if not isinstance(row, dict):
            raise TypeError("universities entries must be mappings")
        uid = _str(row.get("id")).strip()
        name = _str(row.get("name")).strip()
        if not uid or not name:
            continue
        if uid in seen:
            raise ValueError(f"duplicate university id: {uid}")
        seen.add(uid)
        programs = []
        for program in row.get("programs") or []:
            if not isinstance(program, dict):
                continue
            pname = _str(program.get("name")).strip()
            if not pname:
                continue
            programs.append(
                {
                    "name": pname,
                    "url": _str(program.get("url")).strip(),
                    "level": _str(program.get("level")).strip(),
                }
            )
        universities.append(
            {
                "id": uid,
                "name": name,
                "city": _str(row.get("city")).strip(),
                "state": _str(row.get("state")).strip(),
                "site": _str(row.get("site")).strip(),
                "programs": programs,
                "cae": [_str(item).strip() for item in (row.get("cae") or []) if _str(item).strip()],
                "cdfae": bool(row.get("cdfae")),
                "aliases": [_str(item).strip() for item in (row.get("aliases") or []) if _str(item).strip()],
                "poc_name": _str(row.get("poc_name")).strip(),
                "poc_email": _str(row.get("poc_email")).strip(),
            }
        )
    seeds = raw.get("seed_ids") if isinstance(raw.get("seed_ids"), dict) else {}
    return {
        "version": int(raw.get("version") or 1),
        "universities": universities,
        "seed_ids": {
            "aafs": sorted({_str(item).strip() for item in (seeds.get("aafs") or []) if _str(item).strip()}),
            "dfrws": sorted({_str(item).strip() for item in (seeds.get("dfrws") or []) if _str(item).strip()}),
            "fsidi": sorted({_str(item).strip() for item in (seeds.get("fsidi") or []) if _str(item).strip()}),
        },
    }


def convert(yaml_path: Path, json_path: Path) -> dict:
    raw = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    payload = normalize_catalog(raw)
    json_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--yaml", type=Path, default=DEFAULT_YAML)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    args = parser.parse_args()
    payload = convert(args.yaml, args.json)
    print(f"Wrote {args.json} ({len(payload['universities'])} universities)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
