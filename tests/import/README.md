# Old downloads, kept to test imports

Each file here is a skill tree as a teacher downloaded it from aiskilltrees.com, unchanged, named
by the date it was downloaded. `tools/check-import.py` takes `tree.csv` out of each one, the way the
builder does on import, and opens it with the current engine. The workflow
`.github/workflows/import-test.yml` runs it on every push.

| File | Downloaded | Prompt manifest | What it covers |
|---|---|---|---|
| `2026-09-21-example-skill-tree.html` | 2026-09-21 | 2.0.0 | the starter tree, with `meta.json` still in the bundle |
| `2026-09-23-mathematics-2p.html` | 2026-09-23 | 2.0.0 | `features.exams` from before 0.22.0, an English tree |
| `2026-10-21-biologi-1.html` | 2026-10-21 | 3.0.0 | a large tree (120 nodes) with resource rows |
| `2026-11-10-naturfag-8-10-trinn.html` | 2026-11-10 | 3.0.0 | a recent download |

**Add a file when a release changes what a download looks like**, or changes the tree.csv format:
download a tree from the site after the release and drop it in here with its date. Never edit a file
here to make the test pass. If an old file stops importing, the engine is what has to accept it
again, or tell the teacher exactly what to change.

```bash
pip install playwright && python -m playwright install chromium
python tools/check-import.py
```
