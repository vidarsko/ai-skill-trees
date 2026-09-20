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
| `prompts/` | The instructions, in English. One file per contribution, each separately versioned. | CC BY-SA 4.0 |
| `prompts/subjects/` | What is true for one subject family but not another. Adds sections; does not replace them. | CC BY-SA 4.0 |
| `languages/` | Everything that varies with language: interface strings, and the language layer in the instructions. | CC BY-SA 4.0 |
| `spec/` | `decomposition.md` — how a subject is broken into nodes. | CC BY-SA 4.0 |

Two licences, split by what the file is: `LICENSE` (MIT) covers code, `LICENSE-CONTENT`
(CC BY-SA 4.0) covers the written material.

## The three layers

Text is split by what it varies with, not by file type.

| File | Varies with | Holds |
|---|---|---|
| `engine/engine.js` | nothing | Layout, the graph, storage, rendering. No user-facing strings. |
| `prompts/*.json` | nothing | The pedagogy. English is the source. |
| `prompts/subjects/<family>.json` | subject family | What applies to mathematics but not to social studies. |
| `languages/<code>.json` | language | Interface strings, and the language layer in the instructions. |
| `<tree>/tree.json` | one subject | Topic order, storage key, feature switches, slot values. |
| `<tree>/nodes.csv` | subject + language | The graph itself. |

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
separately. Releases are tagged, and the website pins a tag rather than tracking `main`, so the
version running on the site is always one that can be pointed at.

## Status

Early, and moving. The engine, instructions and language files were extracted here from the
website's private repository on 2026-09-20 and this is now where they are edited. Still to come:
the downloadable starter folder, the submission forms and the mechanical validator.

Contributions are not open yet. When they are, a tree is submitted through a form rather than a
pull request, and reviewed by hand before publication — the graph is meant to be teacher-written
and defensible, so the reading is the point of the process rather than an obstacle in it.
