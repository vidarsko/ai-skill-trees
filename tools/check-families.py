#!/usr/bin/env python3
"""Check that every subject family replaces the same set of sections.

Since 0.26.0 each family under prompts/subjects/ carries its own version of
every section any family replaces, so two families can be read side by side.
A section a family has nothing to add to is a verbatim copy of the general
text. This script fails if the sets differ, and lists the copies that no
longer match the general text they were copied from (which may be intended:
the family then has its own wording).

Usage: python3 tools/check-families.py
"""
import glob
import json
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'prompts')


def main():
    manifest = json.load(open(os.path.join(ROOT, 'manifest.json')))
    modules = {k: json.load(open(os.path.join(ROOT, v['file'])))
               for k, v in manifest['instructions'].items()}
    families = {}
    for path in sorted(glob.glob(os.path.join(ROOT, 'subjects', '*.json'))):
        data = json.load(open(path))
        families[data['family']] = data
    ok = True
    for ins in ['node', 'exam', 'lessonPlan', 'motivation']:
        sets = {fam: list(((d['instructions'].get(ins) or {}).get('sections') or {}))
                for fam, d in families.items()}
        first = next(iter(sets.values()))
        for fam, keys in sets.items():
            if keys != first:
                ok = False
                print(f'{ins}: {fam} has {keys}, expected {first}')
        general = modules[ins]['sections']
        for sid in first:
            same = [fam for fam, d in families.items()
                    if d['instructions'][ins]['sections'].get(sid) == general.get(sid)]
            print(f'{ins}.{sid}: general text in {", ".join(same) or "none"}')
    print('OK: every family has the same sections.' if ok else 'FAILED')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
