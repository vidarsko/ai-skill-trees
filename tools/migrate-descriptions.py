#!/usr/bin/env python3
"""Fjern «Eleven kan …» fra description-kolonnen i tree.csv (0.8.0).

Engangsjobb for formatendringen i 0.8.0: en beskrivelse er fra da av det
noden KREVER og ingenting mer - en bar verbfrase for en ferdighet, en bar
definisjon for et begrep - mens «Eleven kan:» / «Eleven kan forklare:»
settes foran av motoren, på treets eget språk.

    tools/migrate-descriptions.py <trekatalog eller mappe med flere>
    tools/migrate-descriptions.py <mappe> --dry-run
    tools/migrate-descriptions.py <mappe> --report rest.csv

Den mekaniske halvparten er trygg og gjøres her. Resten er en lesejobb, og
det finnes ingen vei utenom: å stryke et prefiks foran en setning som
fortsetter «…, og vet hvorfor det virker» gir noe som fortsatt er galt,
bare mindre synlig. Alt skriptet ikke tør røre, står igjen urørt og listes
med rad, id og grunn - det er den lista man går gjennom etterpå.

Reglene er per språk og per type, og de er bevisst smale: treffer ingen av
dem, gjør skriptet ingenting. Et tre kan kjøres flere ganger.
"""

import argparse
import csv
import pathlib
import re
import sys

HEADER = ['id', 'type', 'topic', 'name', 'description', 'depends_on', 'aids', 'instruction']

# Ordene som innleder en beskrivelse i det GAMLE formatet. De brukes også
# til å kjenne igjen en beskrivelse som allerede er migrert: begynner den
# ikke med et av dem, er det ingenting å gjøre.
LEARNER_WORDS = ['Eleven', 'Studenten', 'Deltakeren', 'Deltagaren', 'The student', 'The pupil']


def cap(text):
    return text[:1].upper() + text[1:] if text else text


def lower_first(text):
    return text[:1].lower() + text[1:] if text else text


# --- Ferdigheter ------------------------------------------------------------
# «Eleven kan X» -> «X». Kommaet etter «kan» i «Eleven kan, ut fra …» ryker
# med: ledeteksten står på linja over, og et innledende komma ville hengt.
SKILL_STRIP = [
    re.compile(r'^(?:Eleven|Studenten|Deltakeren|Deltagaren)\s+kan,?\s+', re.I),
    re.compile(r'^The (?:student|pupil)\s+can,?\s+', re.I),
]

# To påstander i én beskrivelse. «Eleven kan løse …, og vet hvorfor» blir
# til «løse …, og vet hvorfor» under ledeteksten «Eleven kan:» - og da står
# det «kan vet». Ingen regel kan gjette hva læreren mente; den skal leses.
SKILL_SECOND_CLAUSE = re.compile(
    r',?\s+(?:og|men|samt|and|but)\s+'
    r'(?:vet|kjenner|forstår|förstår|behersker|har|skal|kan|know|knows|understands)\b', re.I)


# --- Begreper ---------------------------------------------------------------
# «Eleven vet at X» -> «X.», og «Eleven vet hva X er: Y» -> «Y.». Begge er
# definisjonen skrevet som en påstand om eleven; det som står igjen når
# påstanden fjernes, ER definisjonen.
CONCEPT_RULES = [
    re.compile(r'^(?:Eleven|Studenten|Deltakeren)\s+vet\s+at\s+', re.I),
    re.compile(r'^(?:Eleven|Studenten|Deltagaren)\s+vet\s+att\s+', re.I),
    re.compile(r'^The (?:student|pupil)\s+knows\s+that\s+', re.I),
    re.compile(r'^(?:Eleven|Studenten|Deltakeren)\s+vet\s+hva\s+.+?\s+(?:er|betyr|innebærer)\s*:\s+', re.I),
    re.compile(r'^(?:Eleven|Studenten|Deltagaren)\s+vet\s+vad\s+.+?\s+(?:är|betyder)\s*:\s+', re.I),
    re.compile(r'^The (?:student|pupil)\s+knows\s+what\s+.+?\s+(?:is|means)\s*:\s+', re.I),
    re.compile(r'^(?:Eleven|Studenten|Deltakeren|Deltagaren)\s+(?:kan\s+forklare|forstår|förstår)\s+att?\s+', re.I),
    re.compile(r'^The (?:student|pupil)\s+(?:can explain|understands)\s+that\s+', re.I),
]

# «at» som innleder resten blir hengende igjen: «… er: at en forskjell i
# H+-konsentrasjonen driver …» -> «En forskjell i H+-konsentrasjonen driver …».
LEADING_THAT = re.compile(r'^(?:at|att|that)\s+', re.I)

# Det ANDRE «at» i «Eleven vet at X, og at Y» hang på den samme påstanden om
# eleven, og henger i løse lufta når den er borte: «X, og at Y» -> «X, og Y».
DANGLING_THAT = re.compile(r'(,\s+(?:og|samt|och|and)\s+)(?:at|att|that)\s+', re.I)

# Det som IKKE kan gjøres mekanisk, med grunnen skriptet skal si fra om.
CONCEPT_MANUAL = [
    (re.compile(r'^(?:Eleven|Studenten|Deltakeren|Deltagaren)\s+(?:vet|kjenner|känner)\s+(?:forskjellen|skillnaden)\s+(?:på|mellom)\s+', re.I),
     'forskjell: definer hvert begrep for seg, og legg kontrasten i en egen ferdighet'),
    (re.compile(r'^(?:Eleven|Studenten|Deltakeren|Deltagaren)\s+kan\s+skille\s+', re.I),
     'forskjell: definer hvert begrep for seg, og legg kontrasten i en egen ferdighet'),
    (re.compile(r'^(?:Eleven|Studenten|Deltakeren|Deltagaren)\s+vet\s+(?:hva|vad)\b', re.I),
     'ingen definisjon etter «vet hva X er» - definisjonen må skrives'),
    (re.compile(r'^(?:Eleven|Studenten|Deltakeren|Deltagaren)\s+(?:vet|kjenner|känner)\b', re.I),
     'påstand om eleven, ikke en definisjon - må skrives om'),
    (re.compile(r'^(?:Eleven|Studenten|Deltakeren|Deltagaren)\s+kan\b', re.I),
     'begrep formulert som en ferdighet - definisjonen må skrives'),
    (re.compile(r'^The (?:student|pupil)\b', re.I),
     'påstand om eleven, ikke en definisjon - må skrives om'),
]


def already_migrated(text):
    return not any(text.startswith(word) for word in LEARNER_WORDS)


def migrate_skill(text):
    for rx in SKILL_STRIP:
        m = rx.match(text)
        if not m:
            continue
        rest = text[m.end():].lstrip(', ')
        if SKILL_SECOND_CLAUSE.search(rest):
            return None, 'to påstander i én beskrivelse - én «kan» per node'
        return lower_first(rest), None
    return None, 'ukjent innledning på en ferdighet'


def migrate_concept(text):
    for rx in CONCEPT_RULES:
        m = rx.match(text)
        if not m:
            continue
        rest = LEADING_THAT.sub('', text[m.end():])
        if not rest:
            return None, 'ingenting igjen etter innledningen'
        return cap(DANGLING_THAT.sub(r'\1', rest)), None
    for rx, why in CONCEPT_MANUAL:
        if rx.match(text):
            return None, why
    return None, 'ukjent innledning på et begrep'


def migrate_rows(rows):
    """-> (nye rader, [(rad, id, type, grunn, tekst)])"""
    out, left = [], []
    for i, row in enumerate(rows):
        row = list(row)
        kind = row[1].strip().lower() if len(row) > 1 else ''
        if kind not in ('skill', 'concept'):
            out.append(row)
            continue
        text = row[4].strip()
        if already_migrated(text):
            out.append(row)
            continue
        new, why = migrate_skill(text) if kind == 'skill' else migrate_concept(text)
        if new is None:
            left.append((i + 1, row[0], kind, why, text))
        else:
            row[4] = new
        out.append(row)
    return out, left


def migrate_file(path, dry_run=False):
    with path.open(encoding='utf-8', newline='') as f:
        rows = list(csv.reader(f))
    if not rows or rows[0] != HEADER:
        return None, [(1, '', '', 'uventet kolonnerekke - hoppet over', '')]
    new_rows, left = migrate_rows(rows)
    changed = sum(1 for a, b in zip(rows, new_rows) if a != b)
    if not dry_run and changed:
        with path.open('w', encoding='utf-8', newline='') as f:
            csv.writer(f, lineterminator='\n').writerows(new_rows)
    return changed, left


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('target', help='en trekatalog, eller en mappe med flere')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--report', help='skriv radene som står igjen til en CSV')
    args = ap.parse_args()

    root = pathlib.Path(args.target)
    files = sorted(root.glob('tree.csv')) or sorted(root.glob('*/tree.csv'))
    if not files:
        sys.exit('Fant ingen tree.csv under ' + str(root))

    report, total_changed, total_left = [], 0, 0
    for path in files:
        changed, left = migrate_file(path, dry_run=args.dry_run)
        if changed is None:
            print('%-34s hoppet over' % path.parent.name)
            continue
        total_changed += changed
        total_left += len(left)
        print('%-34s %4d skrevet om, %3d star igjen' % (path.parent.name, changed, len(left)))
        for row, node_id, kind, why, text in left:
            report.append([path.parent.name, row, node_id, kind, why, text])

    print('\n%d beskrivelser skrevet om, %d star igjen til lesing.' % (total_changed, total_left))
    if args.report:
        with open(args.report, 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(['tree', 'row', 'id', 'type', 'why', 'description'])
            w.writerows(report)
        print('Lista star i ' + args.report)


if __name__ == '__main__':
    main()
