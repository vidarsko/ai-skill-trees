# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The website pins a tag rather than tracking `main`, so a release here is what makes a change
visible at aiskilltrees.com.

## [0.3.0] - 2026-09-21

### Changed

- **The decomposition model is a prompt module now, and `spec/` is gone.** It was
  `spec/decomposition.md`: the one contribution out of five that had a different shape, a
  different kind of version and a different home. It is now `prompts/decomposition.json`
  (**v2.0.0**), sectioned like the other four, and the folder that held it no longer exists.

  The version is a major bump because the model's output changed with the format: it described
  `nodes.csv`, and a tree is now one `tree.csv` with its settings at the top. Section 3 gained
  the settings table and an example with the `config` and `prompt` rows in it; the checklist
  gained the step of opening the file in the builder.

- **`audience` in the manifest** says who an instruction is for. `student` for the four the
  engine composes, `teacher` for the two a person building a tree uses. The engine loads only
  the first kind — fetching the others on every tree page would cost every reader 20 kB of text
  no student will ever see.

### Added

- **`prompts/authoring.json`** — the instruction a teacher pastes into an AI chat to build a
  tree. It wraps the decomposition model with what the method cannot assume the model knows:
  what the teacher actually wants, what the site does with the file, that the teaching
  instructions themselves may be overruled with a `prompt` row, how to come back later with the
  file and change one thing, what each error message means, and that a tree where almost every
  node has no prerequisites means the work was not done.

  It exists because a teacher should do exactly what a student does — paste one instruction into
  whichever chat they already use, and be taken through the work. That makes the method
  self-similar, and it is why the text is a versioned module here rather than prose on one
  website.

  `spec/authoring-prompt.md` from 0.2.0 is replaced by it.

## [0.2.0] - 2026-09-20

The file format changed: a tree is now one spreadsheet. This breaks every
existing tree, which is what the leading zero in the version number is for —
it is cheap to do now and expensive after 1.0.

### Changed

- **`tree.json` is gone. `tree.csv` is the whole tree.** Settings ride in the
  same table as the nodes, as rows with `config` in the `type` column, `name`
  as the key and `description` as the value; they sit at the top of the file,
  before the nodes. `noder.csv` is renamed `tree.csv` and
  `eksamensoppgaver.csv` to `exams.csv` — English, like the columns and the
  `skill`/`concept` values have always been, and because this is now the file
  a teacher downloads rather than an internal name.

  The reason is the teacher, not tidiness. A tree that arrives as one file can
  be written in a spreadsheet, mailed to a colleague, handed to an AI chat as a
  worked example, and dropped into the builder — all as one thing. Two files
  with different shapes, one of them JSON, is a format for people who already
  know what JSON is.

- **`prompt` rows let a teacher rewrite the teaching instructions** from the
  same spreadsheet: `topic` names the instruction (blank means all of them),
  `name` the section, and the text goes in `instruction`. They resolve above
  everything that comes from a file, because that is the one the teacher edits.

  Only the sections they change — the defaults stay shared and versioned. The
  alternative, baking whole instructions into each tree, would recreate the
  problem this project spent its first release escaping: a fix that reaches
  nobody because everyone has a copy. It is also better evidence: you can say
  exactly what a teacher changed relative to a cited version.

- **An unknown setting is an error.** `aids.2.modell` is reported, with a guess
  at what was meant and the row number, rather than silently doing nothing. In
  a spreadsheet, silence is the dangerous response.

- **The topic order is worked out from the graph** when it is not given:
  lowest level in the column, then median level, then alphabetically. The tops
  of the columns then form a staircase, and the tree reads left to right in the
  order the subject can be taken. `topicOrder` still wins where it is given.
  **This moves columns on existing trees** — Vidar's call, 2026-09-20, on the
  grounds that a derived order is the one a new contributor gets for free.

- **The storage key and the conversation language's name are derived too**, from
  the title and from the language file. The migration writes the storage key
  out explicitly all the same: deriving a new one would throw away every
  student's ticked-off progress, and a published key is data, not a detail.

- **Validation messages moved into the language files.** They were hardcoded
  Norwegian, which was invisible while only Norwegian trees had them and
  obvious the moment an English tree reported a cycle in Norwegian.

### Added

- **`engine/standalone.html` and `window.AIST_BUNDLE`** — the single-file
  edition. Everything the engine would fetch can instead be handed to it as
  data by a `<script>` tag, which is the only way a tree can work from
  `file://`: a page opened from disk has the origin `null`, and `fetch()` is
  refused for it. A script tag is not, because it does not hand the page
  readable bytes, it runs code. Two lines in `fetchJson()`/`fetchText()`; on the
  web the variable does not exist and nothing changes.

- **`starter/tree.csv`** — eight nodes, two topics, one concept, one
  cross-topic prerequisite and one `prompt` row, so every feature appears
  exactly once. It exists to be the format's documentation in working form:
  a filled-in example is worth more to a language model than a schema, and
  it is what a teacher should attach when asking an AI for a tree.

- **`spec/authoring-prompt.md`** — contribution 1 written for a teacher rather
  than for an agent. The full decomposition model stays in `decomposition.md`;
  this is the paste-into-a-chat entry step, and it insists on the part that is
  usually skipped: the prerequisites.

- **`engine/vendor/papaparse.min.js`** — PapaParse now ships with the engine
  instead of coming from a CDN. A downloaded tree cannot depend on a file on
  someone else's machine, and the site stops making a third-party request to
  draw a graph. MIT, v5.7.0.

- **`tools/migrate-to-tree-csv.py`** — the one-off that converted all 19
  published trees.

- `.github/workflows/release.yml` — a push to `main` that bumps `version:` in `CITATION.cff` now
  creates the tag `v<version>` and the GitHub Release by itself, with this file's section for
  that version as the release notes. Creating the tag by hand was the only step in the chain
  that had to happen somewhere other than where the work was done, and it was the one step with
  no judgement in it: the version number is the decision, and the tag follows from it. A version
  with no section here fails the run rather than publishing an unexplained release, which is the
  check that was previously nobody's job. It creates a release and not merely a tag because
  Zenodo archives releases.

## [0.1.2] - 2026-09-20

### Changed

- The student may now ask the AI to switch language, and get it. Every instruction carried an
  absolute prohibition — `languages/<code>.json` → `outputLanguage` said, in so many words, not
  to change language at any point — so a model that was asked directly refused. The prohibition
  was written against a real failure, a model drifting into English halfway through a Norwegian
  conversation, but it was aimed at the model's own initiative and caught the student's request
  along with it. A student who reads the subject in Norwegian but is more comfortable in another
  language was told no by a tool whose whole point is that it adapts.

  The rule is now split the way the layers are split. `prompts/shared.json` gains a
  **`languageSwitch`** section — English source, no language content of its own: an explicit
  request from the reader is honoured at once and holds for the rest of the conversation, while
  a message merely written in another language, a quotation or a borrowed word is not a request,
  so the model still never changes language on its own. Node, skill and concept names keep the
  spelling the tree gives them, with the translation alongside, so the student can still find
  them in the graph after a switch.

  `languages/en.json`, `nb.json` and `sv.json` lose the absolute prohibition from
  `outputLanguage` and keep the rest: which language to start in, that the instruction being
  partly English is not an invitation to answer in English, and the address forms. A `_comment`
  in each says why, so the next language file is not written with the prohibition restored — the
  two would contradict each other, and the model follows the prohibition.

  `practice-tutor.json`, `test-generator.json`, `motivation.json` and `lesson-plan.json` each
  name `languageSwitch` in `order`, directly after `outputLanguage`, and are now **v1.1.0**;
  `shared.json` is **v1.1.0**. No engine change: the section resolves through the fallback to
  `shared.json` that was already there.

## [0.1.1] - 2026-09-20

### Fixed

- `engine/engine.js`: a drag can start on a node box. `.node-box` was excluded from the
  `mousedown` guard in `setupPanning()`, so a quarter of the visible surface — and much more than
  that inside a dense column — refused to pan at all. Clicking a node still opens the detail
  panel: the capture-phase click handler already suppresses that after a real drag. The mastery
  checkbox and the aid-level tag are still excluded. The drag flag is now also cleared on a
  timeout after `mouseup`, so a drag released outside the window cannot swallow the next click.

- `engine/tree.css`: drag-to-pan now works vertically, not only sideways. `main` asks for
  `flex: 1; min-height: 0`, but nothing ever made `<body>` a flex container, so `main` took its
  content height instead. `#graph-scroll` grew to the full height of the graph — 2638px on a
  900px screen — which left it with no vertical scroll range at all, and the window scrolled
  instead. `setupPanning()` sets `scrollTop` on every move; it simply had nowhere to go. `<body>`
  is now the column it was written to be. The same rule was missing in the stylesheet this file
  was ported from, so it was never right, on any tree.

### Changed

- `engine/engine.js`: an institution's display name is read as a single string rather than a
  per-language lookup. Institution names are not translated — an institution has a name, the same
  way a tree is written in one language. Interface headings around it still are. Requires
  `vocabulary.json` with `institution.<key>.label` as a string; the site publishes that file, so
  the two have to move together.

### Added

- `engine/tokens.css` — the engine's default palette and type. Until now every custom property
  `tree.css` uses was defined by the host website, so the engine could not render anywhere else;
  dropped into a folder it came out unstyled. The values are the ones aiskilltrees.com was using
  at extraction, so nothing changed visually there — the engine simply stopped being tied to one
  site. Includes `--aid-1` through `--aid-5`, which are read from `engine.js` rather than from
  the stylesheet and would be missed by a search of the CSS.

### Changed

- `spec/decomposition.md` is now **v1.2.0**. Section 8's licensing argument was written as
  though every tree ends up in the published catalogue, and told every teacher not to copy
  source text because the CSVs are released under an open licence. Most teachers are building a
  tree for their own classroom, where nothing is relicensed and that reason simply does not
  apply — leaving the rule looking like a rule without a reason. The section now says what the
  copyright question actually turns on, which is what is done with the finished tree: licensing
  is marked as applying only to a published tree, the "it is the wrong output anyway" reason is
  marked as applying either way, and a note points out that a private tree can become a
  published one and is cheaper to write correctly than to retrofit. What does *not* depend on
  publication is section 7 — handing a source document to a model is copying regardless — and
  both sections now say so. Checklist step 1 asks for the own-use-or-publication decision along
  with the cohort.
- `spec/decomposition.md` is now **v1.1.0**. Section 7 previously said, without qualification,
  to hand the specification to an agent together with the curriculum. Section 8 governed what
  may go into a published `nodes.csv` but nothing governed what may be handed to a model in
  the first place, which is a separate act of copying. Section 7 now requires that question to
  be settled first, notes that a curriculum is a regulation and free of copyright in Norway
  and Sweden while a private examination body's syllabus is not, and gives the alternative:
  the agent needs the specification and a topic list, not the source document. Section 8's
  licensing point no longer names one organisation as its example.
- Extracted from the private website repository `vidarsko/website_aiskilltrees_com_builder`,
  which is now downstream of this one: `engine/`, `prompts/`, `languages/` and `spec/` are edited
  here and synced to the site.
- `engine/index.html`, the per-tree page template, no longer loads the site's analytics script.
  That tag is specific to one deployment and does not belong in the engine; the site adds it back
  when it publishes.
- The engine's files are served from `/engine/` rather than `/js/` and `/css/`, so the template
  in this repository and the one published on the site differ by exactly one line.

## [0.1.0] - 2026-09-20

First contents. The engine, the instruction modules, the three language files and the
decomposition specification, moved here from the website repository.

This repository is public from the start. That was decided rather than drifted into: the website
fetches a tag from here at deploy time, and a public repository needs no access token for that —
so there is no credential with an expiry sitting between the two, and the failure mode of an
expired token (a red workflow and a site that quietly stops updating) does not exist.

**The tag has to be created before the site can deploy**, since the workflow pins `MACHINERY_REF`
and a missing ref fails the run. Any tag will do for that purpose.

Zenodo is a separate matter and not a prerequisite here. It archives GitHub *releases* rather than
tags, so pushing a tag triggers nothing regardless of whether the webhook is on, and it only picks
up releases created after it is enabled. Switch it on before cutting the release the paper cites —
not before this one.
