# DFIR university tracker

Shared catalog of U.S. universities with digital-forensics programs, NSA CAE designations, public faculty contacts, and related identifiers.

**YAML is the only published catalog file.** This repository does not ship generated JSON. Consumers that must stay on the Python standard library convert the YAML in their own project, then cache JSON locally.

This repository does not fetch literature, match paper affiliations, or render a UI.

## How to contribute

Edit `universities.yaml`.

- **`id` is immutable.** Do not rename an existing school id (`albany`, `gmu`, …). Affiliation matching and seed sets depend on it.
- Add a school with `id`, `name`, `city`, `state`, `site`, and optional `programs`, `cae`, `cdfae`, `aliases`, `poc_name`, and `poc_email`.
- `aliases` are lowercase names used to match literature affiliations. Include common short forms.
- Point-of-contact emails only when they are published on an official university page.
- Seed id lists (`seed_ids.aafs`, `seed_ids.dfrws`, `seed_ids.fsidi`) mark schools with recent AAFS DMS, DFRWS, or FSI:DI involvement even when paper matching has not run yet. Ids in those lists must exist in `universities`.

Then run tests and open a pull request. Do not add a JSON file.

```bat
python -m pip install -r requirements-dev.txt
python -m pytest
```

## Repository layout

| File | Role |
| --- | --- |
| `universities.yaml` | Edit this (source of truth) |
| `schema/universities.schema.json` | Optional schema for the JSON consumers generate |
| `tests/` | Unique ids and seed-id references |

## Using the catalog from another project

Copy or fetch `universities.yaml`. Convert it to JSON **in that project** (PyYAML is only needed for the conversion step). Cache the JSON and keep a bundled snapshot for offline use; do not live-fetch GitHub on every page load.

Default raw URL:

`https://raw.githubusercontent.com/jgrover/dfir_university_tracker/main/universities.yaml`

## License

MIT
