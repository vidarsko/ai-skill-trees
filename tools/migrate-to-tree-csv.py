#!/usr/bin/env python3
"""Slå tree.json + noder.csv sammen til én tree.csv, og døp om eksamensfila.

Engangsjobb for formatendringen i 0.3.0. Kjøres på en trekatalog eller på
en mappe som inneholder flere:

    tools/migrate-to-tree-csv.py ../website_aiskilltrees_com_builder/trees
    tools/migrate-to-tree-csv.py <mappe> --dry-run

Config-radene legges ØVERST i fila, før nodene: det er der en lærer som
åpner regnearket først ser etter hva treet heter og hvilket språk det er
på.

To felter skrives eksplisitt selv om motoren kan utlede dem:

  storageKey   Utledes den på nytt, MISTER hver elev avhukingene sine.
               En publisert nøkkel er ikke en detalj, den er data.
  languageName Bare når den avviker fra språkfilas eget `name`, slik at
               den sammensatte KI-instruksen blir ord for ord den samme.

topicOrder skrives IKKE: fra 0.3.0 utledes kolonnerekkefølgen av dybden.
Det er et bevisst valg (Vidar, 2026-09-20), og det flytter noen kolonner
på noen av de publiserte trærne.
"""

import argparse
import csv
import json
import pathlib
import sys

HEADER = ['id', 'type', 'topic', 'name', 'description', 'depends_on', 'aids', 'instruction']
SCHEMA_VERSION = '3'


def language_name_of(code, machinery):
    path = machinery / 'languages' / (code + '.json')
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding='utf-8')).get('name')


def config_rows(cfg, machinery, has_exams=False):
    """tree.json → [(nøkkel, verdi)], i den rekkefølgen de skal stå."""
    rows = [('schemaVersion', SCHEMA_VERSION)]
    for key in ('title', 'description', 'language'):
        if cfg.get(key):
            rows.append((key, str(cfg[key])))

    derived = language_name_of(cfg.get('language', ''), machinery)
    if cfg.get('languageName') and cfg['languageName'] != derived:
        rows.append(('languageName', cfg['languageName']))

    if cfg.get('subjectFamily'):
        rows.append(('subjectFamily', cfg['subjectFamily']))
    if cfg.get('storageKey'):
        rows.append(('storageKey', cfg['storageKey']))

    for name, value in (cfg.get('features') or {}).items():
        rows.append(('features.' + name, 'true' if value else 'false'))
    if has_exams:
        rows.append(('features.exams', 'true'))
    for name, value in (cfg.get('slots') or {}).items():
        rows.append(('slots.' + name, str(value)))

    aids = cfg.get('aids') or {}
    if aids.get('label'):
        rows.append(('aids.label', aids['label']))
    for level in aids.get('levels') or []:
        n = level.get('level')
        for field in ('name', 'student', 'model'):
            if level.get(field):
                rows.append(('aids.%s.%s' % (n, field), level[field]))

    for name, value in (cfg.get('layoutOverrides') or {}).items():
        rows.append(('layout.' + name, str(value)))

    return rows


def migrate(tree_dir, machinery, dry_run=False):
    tree_json = tree_dir / 'tree.json'
    nodes_csv = tree_dir / 'noder.csv'
    if not tree_json.exists() or not nodes_csv.exists():
        return None

    cfg = json.loads(tree_json.read_text(encoding='utf-8'))
    with nodes_csv.open(encoding='utf-8-sig', newline='') as fh:
        nodes = list(csv.DictReader(fh))
    if nodes and [c for c in nodes[0].keys() if c] != HEADER:
        raise SystemExit('%s: uventede kolonner %s' % (nodes_csv, list(nodes[0].keys())))

    exams = tree_dir / 'eksamensoppgaver.csv'
    # En fil med bare header-linja bærer ingen informasjon; da er det
    # riktigere at fila ikke finnes, siden den nå er valgfri og må meldes
    # med features.exams for i det hele tatt å bli hentet.
    has_exams = exams.exists() and len(
        [l for l in exams.read_text(encoding='utf-8').splitlines() if l.strip()]) > 1

    out = [HEADER]
    for key, value in config_rows(cfg, machinery, has_exams):
        out.append(['', 'config', '', key, value, '', '', ''])
    for node in nodes:
        out.append([(node.get(c) or '') for c in HEADER])

    if dry_run:
        return len(out) - 1 - len(nodes), len(nodes)

    with (tree_dir / 'tree.csv').open('w', encoding='utf-8', newline='') as fh:
        csv.writer(fh, lineterminator='\n').writerows(out)
    tree_json.unlink()
    nodes_csv.unlink()

    if exams.exists():
        exams.rename(tree_dir / 'exams.csv') if has_exams else exams.unlink()

    return len(out) - 1 - len(nodes), len(nodes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('target', help='en trekatalog, eller en mappe med flere')
    ap.add_argument('--machinery', default=str(pathlib.Path(__file__).resolve().parent.parent),
                    help='sjekkout av ai-skill-trees (for languages/)')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    target = pathlib.Path(args.target)
    machinery = pathlib.Path(args.machinery)
    dirs = [target] if (target / 'tree.json').exists() else sorted(
        d for d in target.iterdir() if d.is_dir())

    total = 0
    for d in dirs:
        result = migrate(d, machinery, args.dry_run)
        if result is None:
            continue
        config_count, node_count = result
        total += 1
        print('%-32s %2d config-rader, %3d noder' % (d.name, config_count, node_count))
    print('\n%d tre(r) %s.' % (total, 'ville blitt migrert' if args.dry_run else 'migrert'))
    if not total:
        sys.exit('Fant ingen trær med tree.json under %s' % target)


if __name__ == '__main__':
    main()
