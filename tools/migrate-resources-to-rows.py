#!/usr/bin/env python3
"""Move a tree's resources.csv into its tree.csv as `resource` rows (engine 0.34.0).

    python3 tools/migrate-resources-to-rows.py path/to/trees/*/

For every tree folder that has a resources.csv:

  - each distinct resource (same group, label and url) becomes ONE row,
    `,resource,<group>,<label>,<url>,<node1;node2>,,`, with every node it
    was listed under in depends_on, in the order they first appeared;
  - the rows are appended after the last row of tree.csv, in the order the
    resources first appear in resources.csv, so the groups keep their order;
  - the `features.resources` config row is removed;
  - resources.csv is deleted.

Every other line of tree.csv is left exactly as it was, so the diff of a
migrated tree is the removed config row and the added resource rows.
A folder without resources.csv is left alone.
"""

import csv
import io
import os
import re
import sys

FEATURE_ROW = re.compile(r'^,config,,features\.resources,[^\r\n]*\r?\n?$')


def read_resources(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    merged = {}
    order = []
    for row in rows:
        node = (row.get('node_id') or '').strip()
        group = (row.get('group') or '').strip()
        label = (row.get('label') or '').strip()
        url = (row.get('url') or '').strip()
        if not node or not (label or url):
            continue
        key = (group, label, url)
        if key not in merged:
            merged[key] = []
            order.append(key)
        if node not in merged[key]:
            merged[key].append(node)
    return [(k, merged[k]) for k in order], len(rows)


def migrate(folder):
    tree_path = os.path.join(folder, 'tree.csv')
    res_path = os.path.join(folder, 'resources.csv')
    if not (os.path.isfile(tree_path) and os.path.isfile(res_path)):
        return None

    with open(tree_path, encoding='utf-8', newline='') as f:
        text = f.read()
    newline = '\r\n' if '\r\n' in text else '\n'
    bom = text.startswith('﻿')
    body = text[1:] if bom else text

    lines = body.splitlines(keepends=True)
    header = next(csv.reader([lines[0]]))
    header = [h.strip() for h in header]
    for col in ('type', 'topic', 'name', 'description', 'depends_on'):
        if col not in header:
            raise SystemExit('%s: the header has no column %s' % (tree_path, col))

    kept = [line for line in lines if not FEATURE_ROW.match(line)]
    if kept and not kept[-1].endswith(('\n', '\r')):
        kept[-1] += newline

    resources, before = read_resources(res_path)
    out = io.StringIO()
    writer = csv.writer(out, lineterminator=newline)
    for (group, label, url), nodes in resources:
        cells = [''] * len(header)
        cells[header.index('type')] = 'resource'
        cells[header.index('topic')] = group
        cells[header.index('name')] = label
        cells[header.index('description')] = url
        cells[header.index('depends_on')] = ';'.join(nodes)
        writer.writerow(cells)

    with open(tree_path, 'w', encoding='utf-8', newline='') as f:
        f.write(('﻿' if bom else '') + ''.join(kept) + out.getvalue())
    os.remove(res_path)
    return before, len(resources)


def main(folders):
    total_before = total_after = trees = 0
    for folder in folders:
        result = migrate(folder)
        if result is None:
            continue
        before, after = result
        trees += 1
        total_before += before
        total_after += after
        print('%s: %d rows in resources.csv -> %d resource rows' % (folder.rstrip('/'), before, after))
    print('%d trees, %d rows -> %d resource rows' % (trees, total_before, total_after))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    main(sys.argv[1:])
