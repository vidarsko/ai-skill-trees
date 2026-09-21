# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The website pins a tag rather than tracking `main`, so a release here is what makes a change
visible at aiskilltrees.com.

## [0.9.0] - 2026-09-21

### Added

- **`slots.courseSpecifics` — one setting that reaches every instruction a student is given.**
  Until now a teacher could rewrite ONE section of ONE instruction with a `prompt` row, or add to
  ONE node with the `instruction` column. What there was no way to say was something true of the
  whole course: that its skills are practised on real people and cannot be drilled in a chat, that
  a tick means the reader has tried something rather than answered a question about it, that a
  tool the course forbids must not be suggested. Saying it four times, once per instruction, is
  four things to keep in step, and a teacher who writes it in only two gets a tree that
  contradicts itself depending on which button the reader pressed.

  The setting is **empty by default**, and a tree that does not set it composes exactly the text
  it composed before — this is an addition to the schema, not a change to any existing tree.
  Where it is set, the text is carried unchanged into the practice tutor, the test generator, the
  motivation dialogue and the lesson-plan generator, under the keyword `courseSpecifics`, and it
  says in so many words that it wins over the default where the two disagree.

  It is a **shared section**, held once in `prompts/shared.json`, for the reason that file exists:
  the wording around the teacher's own text is identical in all four instructions, so there is
  nothing for a module to say differently. Its place in `order` is directly after
  `languageSwitch`, before each instruction's own substance, so the model reads what is true of
  the course before it is told what to do in it.

  A `prompt` row aimed at `courseSpecifics` switches the section on too, not only the setting.
  Without that, a teacher who found the keyword on aiskilltrees.com/prompts/ and wrote the row
  rather than the setting would have had it read, echoed back as a setting, and then silently do
  nothing — which is the failure `validatePromptRows()` exists to prevent, and it would have
  been reintroduced by the one section most likely to be written that way.

  `prompts/shared.json` 1.1.0 → 1.2.0, `practice-tutor.json` 1.2.0 → 1.3.0,
  `test-generator.json`, `motivation.json` and `lesson-plan.json` 1.1.0 → 1.2.0, and
  `decomposition.json` 2.4.0 → 2.5.0 for the settings table.

## [0.8.1] - 2026-09-21

### Changed

- **The line at the top left is shorter**: «Matematikk 2P. Lag ditt eget tre: aiskilltrees.com».
  Vidar's wording again. The question it used to open with — «Liker du treet?» — asked the reader
  for an opinion before telling them the one thing the line is there for, and a reader who does
  *not* like the tree is not the reader the invitation is aimed at anyway. All three language
  files changed; the mechanism is untouched.

- **5px rather than 2px** between that line and the first column label, so the sentence reads as
  its own line instead of as a caption on the labels below it. The canvas still has its own 12px,
  so the change is in the negative margin that pulls the line back down over it.

## [0.8.0] - 2026-09-21

### Changed

- **The `description` column no longer carries «The student can».** It was presentation stored
  as data: the same three words in front of every row in every tree, untranslatable,
  unstyleable, and in the way of the one thing the column is for. A description is now the bare
  requirement — a verb phrase for a skill (`add two multi-digit numbers, including cases that
  carry`), a definition for a concept (`The position of a digit decides what the digit is
  worth.`) — and the engine prints the lead-in in front of it, in the tree's own language.

  The two types get **different lead-ins**, because a definition is not a verb phrase and «The
  student can: The position of a digit decides what the digit is worth» does not parse. A skill
  gets «The student can:», a concept «The student can explain:», each on its own line above the
  description and in the primary colour, so it reads as the tool's words rather than the
  teacher's.

  **This is a breaking change to the data format.** A tree written before this renders as «The
  student can: The student can …». `tools/migrate-descriptions.py` does the mechanical half and
  names every row it did not dare touch; the rest is a reading job, and there is no way around
  that — stripping a prefix off a sentence that continues «…, and knows why it works» produces
  something that is still wrong, just less visibly.

- **Every concept is written `Term: definition`**, one line per concept, whether the node
  defines one or four. A node may define several - `Intron and exon` is one box in the map and
  two definitions, written on two lines with a real line break inside the quoted field. The
  engine splits on the line break and on nothing else, so a definition may contain colons and
  semicolons: only what stands before the first colon on a line is read as the term, and it is
  printed in bold.

  The label was optional for a single definition at first, on the argument that the node's name
  already carries the term. Seeing it on the page settled it the other way (Vidar, same day):
  a node with one definition and a node with three then looked like two different formats to
  anyone reading them one after the other, and it is that reading the format exists for. The
  word is repeated; the page is consistent.

  The matching rule in the specification: **a difference between two concepts is a skill, not
  part of a definition.** Knowing two definitions and being able to say what separates them are
  different things, and the second is work — the same argument that sends procedural work out of
  a concept node and into a skill that depends on it.

- **`goal` in the practice tutor is now three sections**, `goal`, `goalSkill` and `goalConcept`,
  with `goalConceptMultiple` added when the node really does hold several definitions. The
  instruction has to complete the same sentence the panel does, and it cannot do that in one
  text that has to serve both types. A `prompt` row naming `goal` still works and now replaces
  the framing only.

### Added

- **`learner`: `pupil`, `student` or `participant`** — what the person learning is *called*. A
  pupil at school and a student at university are the same thing in the tree and different in
  every sentence about it, and Norwegian will not let one word cover both. Only the key goes in
  `tree.csv`; the inflected forms and both lead-ins live in `languages/<code>.json`, because
  inflection is something that varies with language and a teacher should not have to write
  grammar in a spreadsheet. Each language has its own default — school in Norwegian and Swedish,
  university in English — and an unknown value is reported with its row and a guess, like any
  other setting.

  The word reaches the instructions as `{learner}`, `{learnerDefinite}`, `{learners}` and
  `{learnersDefinite}`, available in the language layer and in a `prompt` row — but **not** in
  `prompts/`, which is English and would end up saying «helping eleven practise».

## [0.7.2] - 2026-09-21

### Fixed

- **The gap under the top line, once more, tighter.** What was left after 0.7.1 was
  `LAYOUT.padding` — the canvas's own 12px, which applies to all four sides and is not the place
  to fix one of them. The line is pulled closer instead, with a negative bottom margin and a
  slightly tighter line-height, so the canvas keeps the padding it needs everywhere else.

## [0.7.1] - 2026-09-21

### Fixed

- **The gap between the new top line and the first column label was twice what it should be.**
  Reported by Vidar with a screenshot. Two separate bits of air sat on top of each other:
  `#graph-scroll` kept a 12px padding-top from when nothing was above the graph, and
  `.made-with` added its own below the text — with `LAYOUT.padding` (another 12px, inside the
  canvas) underneath both. The scroll container's top padding is gone and the line's bottom
  padding with it; the canvas padding is what separates them now, which is the one that was
  always meant to.

## [0.7.0] - 2026-09-21

### Added

- **A tree now says what it is and where it came from, on one line at the top left**: «Matematikk
  2P. Liker du treet? Lag ditt eget: aiskilltrees.com». Vidar's wording. It sits in the flex
  column before `<main>`, so the graph loses exactly the height the line takes and nothing
  overlaps; the left margin is `#graph-scroll`'s, so it stands directly above the first column
  label, at that label's size but without the caps and letter-spacing — it is a sentence, not a
  tag.

  **The point is the downloaded single file.** A tree a teacher builds and mails to a class is
  one HTML file with no catalogue around it and no back link anywhere; until now it said nothing
  about where it came from or that the reader could build one. That is why the line is in
  `engine/standalone.html` as well as `engine/index.html`, and why the address is absolute.

  The text is `ui.makeYourOwn` in `languages/<code>.json` like every other string the engine
  shows, so it stands in the tree's own language. The domain is not part of it: an address is
  not a translation, so the engine appends it as the link text, pointing at
  aiskilltrees.com/make-your-own/ — the page the sentence promises.

  A deployment's per-tree pages are copies of `engine/index.html`, so they need re-copying;
  `tools/sync-engine.sh --check` in the website repository reports the drift by name.

## [0.6.0] - 2026-09-21

### Changed

- **Every composed instruction now names its parts: `role: …`, `tone: …`, `mastery: …`.** One
  line in `composePrompt()`, and it does two jobs at once. The model gets the structure XML tags
  would have given it, without the instruction looking like code to the teacher or student
  pasting it in — Vidar's call, and the reason the tags were rejected. And the teacher can read
  the keyword for a `prompt` row straight off the instruction their own students are given,
  rather than looking it up anywhere.

  The keywords are English and camelCase, like everything else under `prompts/`, so a Norwegian
  student sees `writingStyleGeneral:` in front of Norwegian prose. That is the same English
  keyword the `name` column of a `prompt` row already takes, so the two agree; it is new that a
  student sees them. Sections the subject family adds are prefixed the same way, since they are
  sections like any other.

  `/prompts/` does **not** show the prefix: the keyword is already the left-hand column of the
  half-table there, and the prefix is added when the instruction is composed rather than stored
  in the section text, so the page needed no exception.

- **`prompts/decomposition.json` (v2.2.0) has the same shape as every other module now**:
  `order` and `sections`, nothing else. Its `intro` is a section called `about`, first in
  `order`, and its `titles` table is gone. It was the last asymmetry left over from
  `spec/decomposition.md` — the one module with a preamble and a parallel table of human names
  for its sections, which nothing else had and which had to be kept in step by hand.

  The eighteen cross-references inside it went with the titles: `section 4` meant the fourth
  numbered heading, and there are no numbered headings any more. They now name the keyword —
  «the central rule in `whichConcepts`», «This is why `cohort` comes first» — which is both
  stable under reordering and the same name the reader sees in front of the section.

- `prompts/authoring.json` (**v1.3.0**) says that the keyword is printed in front of each part
  of the instruction, so the teacher knows the name is there to be read. The decomposition
  model's data-model section says the same where it explains a `prompt` row.

## [0.5.0] - 2026-09-21

### Added

- **A `prompt` row that does not hit anything is an error now.** Until this release it was read,
  listed back to the teacher as a setting, and then never used — the one place this format was
  silent where it should not have been, and the one 0.4.2 had just finished writing into the
  instructions as a caveat. It is the same failure as an unknown `config` key, with a worse
  outcome: the teacher who asked for "no emoji" believes they got it, and the class gets the
  default.

  Two errors, both naming the row and both guessing at what was meant, the way an unknown
  setting already did:

  - `errorUnknownPromptSection` — the `name` column names a section the instruction does not
    have. `withholdAnswer` is reported with *did you mean `withholdAnswers`?*
  - `errorUnknownPromptTarget` — the `topic` column names something that is not an instruction
    this tree composes. That includes `decomposition` and `authoring`: they are the teacher's
    own, the engine never loads them on a tree page, and a row aimed at one of them does
    nothing.

  What counts as a known section is the instruction's own `order` **plus whatever the subject
  family adds** — that is `sectionOrder()`, the same list composition walks, so the check cannot
  drift from what actually gets used. A row with an empty `topic` applies to every instruction,
  so it passes if any one of them has the section. Validation therefore runs from `bootstrap()`
  after the modules and the family file are loaded, not from `splitRows()`, which is also why
  `splitRows()` now keeps each prompt row's line number.

  Both messages live in `languages/*.json` like every other string the engine shows, in all
  three languages. The offline single-file build gets this for free — it goes through the same
  `bootstrap()` — and the builder at aiskilltrees.com/make-your-own/ lists these errors with its
  existing copy button, so the fix is a paste back into the chat.

### Changed

- `prompts/authoring.json` (**v1.2.0**) and `prompts/decomposition.json` (**v2.1.1**) no longer
  tell a teacher that a mistyped section name goes unreported — it was true for one release.
  They now say it is caught, with the row and a guess, and that looking the name up on
  aiskilltrees.com/prompts/ still saves the round trip. The authoring instruction's list of
  error messages a teacher might paste back gained this pair. The README says the same.

## [0.4.2] - 2026-09-21

### Changed

- **Both teacher instructions now point at the published instructions.** `prompts/authoring.json`
  is **v1.1.0** and `prompts/decomposition.json` is **v2.1.0**.

  The gap was specific. Both told a teacher that any section of the default instruction can be
  overruled with a `prompt` row, and the data model said which columns the row uses — but
  neither said where the instruction and section names come from. The only example was the one
  in the schema (`,prompt,node,tone,…`), so a teacher, or the model helping them, had to guess
  `node`, `exam`, `motivation`, `lessonPlan` and every section id from it. Those names are
  published in full at aiskilltrees.com/prompts/, one card per instruction with every section
  listed under the keyword that names it, which is exactly the keyword the row takes.

  Both files now say so, and say the thing that makes it matter: **a `prompt` row naming a
  section that does not exist is read, reported back as a setting, and then never used — no
  error anywhere.** That is the one place this format is silent where it should not be, and the
  reason is worth knowing rather than fixing blind: the engine only ever looks up section ids
  that an instruction's `order` names, so an unknown id is never consulted. Reporting it would
  mean validating the CSV against every instruction's section list at load time. Not done here.

  The decomposition model also gained a step 11 in the checklist — read what your students will
  actually be told — and the README gained the same pointer next to the row table.

## [0.4.1] - 2026-09-21

### Fixed

- `prompts/decomposition.json` is **v2.0.1**: eight sections ended with a stray `---`. They were
  the horizontal rules that separated the sections while this was a markdown file, and the
  conversion in 0.3.0 carried them into the section bodies, where they mean nothing. They showed
  up on aiskilltrees.com/prompts/ and, worse, in the middle of the instruction a teacher pastes
  into a chat.

## [0.4.0] - 2026-09-21

### Changed

- **The machinery is published under `/assets/`.** `/assets/engine/`,
  `/assets/prompts/`, `/assets/languages/`, `/assets/starter/`. The folder names in this
  repository are unchanged — only the URLs a deployment serves them at — so nothing that cites
  `prompts/decomposition.json` moves.

  The reason is a collision: aiskilltrees.com wants `/prompts/` for a page that shows the
  instructions to a teacher, and that path was the machinery's. The general fix is a prefix that
  says *files the pages load, rather than pages you visit*, which is what `assets` has meant on
  the web for twenty years. Putting all four directories behind it means the next page name
  cannot collide either.

  Two names were rejected. `_assets/` reads as "internal" to a developer, but GitHub Pages runs
  Jekyll, which **drops** directories beginning with an underscore — the machinery would have
  vanished from the published site with no error anywhere. `/method/` describes the contents
  well and is exactly wrong for the purpose: it reads like a page, which is the confusion being
  fixed.

  A deployment that serves the machinery from the old paths needs to move it, or to serve
  `/assets/` as an alias. The engine asks for the new paths and nothing else.

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
