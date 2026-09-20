# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The website pins a tag rather than tracking `main`, so a release here is what makes a change
visible at aiskilltrees.com.

## [Unreleased]

### Added

- `engine/tokens.css` — the engine's default palette and type. Until now every custom property
  `tree.css` uses was defined by the host website, so the engine could not render anywhere else;
  dropped into a folder it came out unstyled. The values are the ones aiskilltrees.com was using
  at extraction, so nothing changed visually there — the engine simply stopped being tied to one
  site. Includes `--aid-1` through `--aid-5`, which are read from `engine.js` rather than from
  the stylesheet and would be missed by a search of the CSS.

### Changed

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
