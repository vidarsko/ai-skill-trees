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

Note: this version has not been tagged yet. Tag it only after the Zenodo webhook is switched on —
a tag created beforehand gets no DOI, and the paper cites the tag rather than the branch.
