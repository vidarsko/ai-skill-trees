# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The website pins a tag rather than tracking `main`, so a release here is what makes a change
visible at aiskilltrees.com.

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
