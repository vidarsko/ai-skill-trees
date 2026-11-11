#!/usr/bin/env python3
"""Check that skill trees downloaded with older versions still import.

A teacher who downloaded a tree as a single HTML file can bring it back
into the builder at aiskilltrees.com/make-your-own/. The builder does not
read the old engine in that file: it takes the spreadsheet out of
`window.AIST_BUNDLE` (key "tree.csv") and builds everything else again
with the current engine. So a change to the engine's look can never break
an import. What can break one is
  1. the marker `window.AIST_BUNDLE = ` or the key "tree.csv" going away,
  2. a change to the tree.csv format the current engine no longer accepts:
     a renamed setting, node type or instruction section, which the engine
     reports as an error rather than ignoring.

For every file in tests/import/, this script
  - takes tree.csv out of the HTML exactly as the builder does
    (extractFromHtml in the site's js/standalone.js), and
  - opens it with the engine in this checkout, in headless Chromium,
    and fails if the engine reports a validation error, a script error,
    or renders no nodes.

Usage:
  python tools/check-import.py              # every fixture
  python tools/check-import.py some.html    # one or more files

Needs Playwright for Python with Chromium:
  pip install playwright && python -m playwright install chromium
"""

import functools
import http.server
import json
import os
import socketserver
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "import"
MARKER = "window.AIST_BUNDLE = "

# Paths the engine asks for, mapped onto this repository. On the site the
# machinery is served under /assets/; here the folders sit at the root.
ASSET_DIRS = {
    "/assets/engine/": ROOT / "engine",
    "/assets/prompts/": ROOT / "prompts",
    "/assets/languages/": ROOT / "languages",
    "/assets/starter/": ROOT / "starter",
}


def extract_tree_csv(html):
    """Mirror of extractFromHtml() in the site's js/standalone.js."""
    start = html.find(MARKER)
    if start == -1:
        raise ValueError("no `window.AIST_BUNDLE = ` in the file")
    begin = start + len(MARKER)
    end = html.find("</script>", begin)
    if end == -1:
        raise ValueError("AIST_BUNDLE is not followed by </script>")
    raw = html[begin:end].rstrip()
    if raw.endswith(";"):
        raw = raw[:-1]
    bundle = json.loads(raw)
    tree = bundle.get("tree.csv")
    if not isinstance(tree, str):
        raise ValueError('the bundle has no "tree.csv" string')
    return tree


class Handler(http.server.SimpleHTTPRequestHandler):
    trees = {}  # fixture name -> tree.csv text

    def log_message(self, *args):
        pass

    def send_bytes(self, body, ctype):
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        # /t/<name>/ is the tree page; /t/<name>/tree.csv is its sheet.
        if path.startswith("/t/"):
            parts = path.split("/")
            name = parts[2] if len(parts) > 2 else ""
            rest = "/".join(parts[3:])
            if name in self.trees and rest in ("", "index.html"):
                return self.send_bytes((ROOT / "engine" / "index.html").read_bytes(), "text/html; charset=utf-8")
            if name in self.trees and rest == "tree.csv":
                return self.send_bytes(self.trees[name].encode("utf-8"), "text/csv; charset=utf-8")
        for prefix, folder in ASSET_DIRS.items():
            if path.startswith(prefix):
                f = (folder / path[len(prefix):]).resolve()
                if folder.resolve() in f.parents and f.is_file():
                    ctype = {
                        ".js": "text/javascript", ".css": "text/css",
                        ".json": "application/json", ".csv": "text/csv",
                    }.get(f.suffix, "application/octet-stream")
                    return self.send_bytes(f.read_bytes(), ctype + "; charset=utf-8")
        # Everything else the page asks for belongs to the website, not the
        # machinery (/css/tokens.css, /trees/vocabulary.json). The engine
        # works without them.
        self.send_error(404)


def main(argv):
    files = [Path(a) for a in argv] or sorted(FIXTURES.glob("*.html"))
    if not files:
        print("no fixtures in", FIXTURES)
        return 1

    failures = []
    trees = {}
    for i, f in enumerate(files):
        try:
            trees[f"f{i}"] = (f, extract_tree_csv(f.read_text(encoding="utf-8")))
        except Exception as err:  # noqa: BLE001 - every reason is a failure
            failures.append(f"{f.name}: could not take tree.csv out of the file: {err}")

    Handler.trees = {k: v[1] for k, v in trees.items()}
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for key, (f, _) in trees.items():
            page = browser.new_page()
            page_errors = []
            page.on("pageerror", lambda e, acc=page_errors: acc.append(str(e)))
            page.goto(f"http://127.0.0.1:{port}/t/{key}/")
            try:
                page.wait_for_function(
                    """() => document.querySelector('.node-box')
                          || (document.getElementById('error-banner') || {classList: {contains: () => false}}).classList.contains('visible')
                          || /tree\\.csv/.test(document.body.textContent || '')""",
                    timeout=20000)
            except Exception:  # noqa: BLE001
                failures.append(f"{f.name}: the tree did not finish loading")
                page.close()
                continue
            errors = page.evaluate(
                "() => (typeof validationErrors === 'undefined' ? ['engine did not start'] : validationErrors.map(errorText))")
            nodes = page.evaluate("() => document.querySelectorAll('.node-box').length")
            problems = list(errors) + [f"script error: {e}" for e in page_errors]
            if nodes == 0:
                problems.append("no nodes were drawn")
            if problems:
                failures.append(f"{f.name}:\n    " + "\n    ".join(problems))
            else:
                print(f"ok   {f.name} ({nodes} nodes)")
            page.close()
        browser.close()
    server.shutdown()

    for msg in failures:
        print("FAIL", msg)
    print(f"\n{len(files) - len(failures)} of {len(files)} imported cleanly")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
