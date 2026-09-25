# AI Skill Trees

A skill tree is a graph of the skills and concepts in one school subject, written by a teacher.
Each node carries an instruction that a student copies into an AI chat to practise that skill.

This repository holds the machinery: the rendering engine, the instructions, the interface
languages and the decomposition specification. The trees themselves are published at
[aiskilltrees.com](https://aiskilltrees.com), which builds against a tagged release from here.

Nothing in this repository calls a language model. The engine composes a text instruction; the
student pastes it into whichever chat they already use.

## What is in here

| Path | What it is | Licence |
|---|---|---|
| `engine/` | `engine.js`, `tree.css`, `tokens.css` and the per-tree page template. No user-facing text. | MIT |
| `prompts/` | The instructions, in English. One file per contribution, each separately versioned — including `decomposition.json`, how a subject is broken into nodes, and `authoring.json`, the instruction a teacher pastes into a chat to build one. | CC BY 4.0 |
| `prompts/subjects/` | What is true for one subject family but not another. Adds sections; does not replace them. | CC BY 4.0 |
| `languages/` | Everything that varies with language: interface strings, the words for the person learning (pupil, student, participant — inflected, so a tree only picks a key), and the language layer in the instructions. | CC BY 4.0 |
| `starter/` | `tree.csv` — a tiny working tree that doubles as the format's documentation. | CC BY 4.0 |

Two licences, split by what the file is: `LICENSE` (MIT) covers code, `LICENSE-CONTENT`
(CC BY 4.0) covers the written material. Until 0.13.0 it was CC BY-SA 4.0.

## One file per tree

A skill tree is **one spreadsheet**. `tree.csv` holds the nodes, the settings
and any teaching instruction the teacher chose to rewrite, and the `type`
column says which a row is:

| `type` | The row is | Where its parts go |
|---|---|---|
| `skill` / `concept` | a node in the graph | the columns mean what they always did |
| `config` | a setting | `name` = key, `description` = value |
| `prompt` | an instruction the teacher rewrote | `topic` = which instruction (blank = all), `name` = which section, `instruction` = the text |

Config rows go at the top, before the nodes. `tree.json` is gone as of 0.2.0.

**The names a `prompt` row takes are the ones in `prompts/`**: the instruction's own key from
`manifest.json` — `node`, `exam`, `motivation`, `lessonPlan` — and a section id from that
instruction's `order`. A deployment publishes them all, section by section, at
[aiskilltrees.com/prompts/](https://aiskilltrees.com/prompts/), and a composed instruction prints
each section with its keyword in front of it — `tone: …` — so the name is also readable off the
instruction itself. A section or instruction name
that does not exist is an error, reported with its row and a guess at what was meant — for the
same reason an unknown setting is: in a spreadsheet, silence is the dangerous response.

**An unknown setting is an error, not something ignored.** In a spreadsheet,
silence is the dangerous response: `aids.2.modell` would otherwise simply do
nothing, forever, and no one would know why. The engine reports it, guesses
what was meant, and says so on the page.

**Three settings are worked out rather than asked for.** The storage key comes
from the title, the conversation language's name from the language file, and
the topic order from the graph's own shape — columns are sorted by the lowest
level any of their nodes sits at, then by median level, then alphabetically, so
the tops of the columns form a staircase and the tree reads left to right in
the order the subject can be taken. Any of the three can still be given
explicitly, and an explicit value always wins.

## Where a deployment serves this

The folder names here are the names in the repository. A site that deploys this serves them
under **`/assets/`** — `/assets/engine/engine.js`, `/assets/prompts/manifest.json` and so on —
and the engine asks for exactly those paths. The prefix exists so that a page can be called
`/prompts/` without colliding with the machinery, and it says the useful thing about everything
behind it: these are files the pages load, not pages anyone visits.

## The three layers

Text is split by what it varies with, not by file type.

| File | Varies with | Holds |
|---|---|---|
| `engine/engine.js` | nothing | Layout, the graph, storage, rendering. No user-facing strings. |
| `prompts/*.json` | nothing | The pedagogy. English is the source. |
| `prompts/subjects/<family>.json` | subject family | What applies to mathematics but not to social studies. |
| `languages/<code>.json` | language | Interface strings, and the language layer in the instructions. |
| `<tree>/tree.csv` | one subject | Everything that tree owns: the nodes, its settings, and any instruction the teacher rewrote. |
| `<tree>/exams.csv` | one subject | Optional: past exam questions per node. |

**A new language costs one file.** `languages/<code>.json` — not a copy of the engine, not a new
page template, not a line of JavaScript.

The English core leaves two slots open, `outputLanguage` and `writingStyle`, and the language
file fills them. That matters more than it looks: the most useful advice in an instruction —
write actively, avoid words you would not say out loud to a friend — is advice about prose in a
particular language, and it does not survive translation. It is added rather than translated.

The consequence for contributors is that a tree in a language with no file of its own still works
from day one: the interface falls back to English while the conversation runs in the tree's own
language. Low threshold to enter, a ceiling that rises once someone writes that language file.

## Versioning

Each instruction module in `prompts/` carries its own `version`, because they are cited
separately. All six are the same shape — the decomposition model became one of them in 0.3.0,
having been a markdown file on its own until then — and `audience` in the manifest says whether
an instruction ends up in a student's chat or is for the teacher building the tree. Releases are tagged, and the website pins a tag rather than tracking `main`, so the
version running on the site is always one that can be pointed at.

**`version:` in `CITATION.cff` is the release number, and changing it is what makes a release.**
A push to `main` that bumps it is picked up by `.github/workflows/release.yml`, which creates the
tag `v<version>` and a GitHub Release whose notes are that version's section of `CHANGELOG.md`.
A push that does not bump it does nothing, because the tag is already there. So there is no tag
to remember to create, and no way for the number in the file and the tag in the repository to
drift apart.

That makes the changelog part of the release rather than a note about it. Entries accumulate
under `## [Unreleased]` as work lands; bumping the version renames that heading to
`## [<version>] - <date>` in the same commit. A version with no section of its own fails the run
rather than publishing an unexplained release.

Moving the *website* to a new release stays a deliberate step — `MACHINERY_REF` in its deploy
workflow. Automating that as well would only be the site tracking `main` in a slower disguise,
and the gap between the two is what gives a change somewhere to be looked at before it is live.

## Status

Early, and moving. The engine, instructions and language files were extracted here from the
website's private repository on 2026-09-20, and this is now where they are edited — the site
builds against a tag from here rather than holding its own copy. Still to come: the downloadable
starter folder, the submission forms and the mechanical validator.

Contributions are not open yet. When they are, a tree is submitted through a form rather than a
pull request, and reviewed by hand before publication — the graph is meant to be teacher-written
and defensible, so the reading is the point of the process rather than an obstacle in it.
