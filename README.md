# DFIR university tracker

Shared catalog of U.S. universities with digital-forensics programs, NSA CAE designations, public faculty contacts, and related identifiers.

**YAML is the editable source of truth.** `universities.json` is generated for consumers that stay on the Python standard library (for example a local dashboard that fetches this file about once a day).

This repository does not fetch literature, match paper affiliations, or render a UI.

## How to contribute

Edit `universities.yaml`, not the JSON.

- **`id` is immutable.** Do not rename an existing school id (`albany`, `gmu`, …). Affiliation matching and seed sets depend on it.
- Add a school with `id`, `name`, `city`, `state`, `site`, and optional `programs`, `cae`, `cdfae`, `aliases`, `poc_name`, and `poc_email`.
- `aliases` are lowercase names used to match literature affiliations. Include common short forms.
- Point-of-contact emails only when they are published on an official university page.
- Seed id lists (`seed_ids.aafs`, `seed_ids.dfrws`, `seed_ids.fsidi`) mark schools with recent AAFS DMS, DFRWS, or FSI:DI involvement even when paper matching has not run yet. Ids in those lists must exist in `universities`.

Then regenerate JSON and run tests:

```bat
python -m pip install -r requirements-dev.txt
python tools/yaml_to_json.py
python -m pytest
```

Open a pull request with the YAML change and the generated JSON.

## Repository layout

| File | Role |
| --- | --- |
| `universities.yaml` | Edit this |
| `universities.json` | Generated; what dashboards should fetch or vendor |
| `tools/yaml_to_json.py` | YAML → JSON converter (needs PyYAML) |
| `schema/universities.schema.json` | Optional JSON Schema |
| `tests/` | Unique ids, seed-id references, convert round-trip |

## Using the catalog from another project

Fetch or copy `universities.json`. Do not live-fetch GitHub on every page load — cache it (this dashboard caches for about a day) and keep a bundled snapshot for offline use.

Default raw URL:

`https://raw.githubusercontent.com/jgrover/dfir_university_tracker/main/universities.json`

## License

MIT
