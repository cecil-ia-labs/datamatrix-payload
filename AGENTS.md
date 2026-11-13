<!--
SPDX-FileCopyrightText: 2026 Cecil-IA Labs
SPDX-License-Identifier: MIT
Author: João Paulo De Luca Jr.; Jorge Luiz Espanhol
Organization: Cecil-IA Labs
Project: Quad-Dimensional DataMatrix
AI-assisted development: OpenAI ChatGPT and Codex were used as development tools.
Human-directed development and integration. No OpenAI endorsement is implied.
-->
# AGENTS.md — Quad-Dimensional DataMatrix

## Mission
Maintain the research, evidence, protocol discussion, synthetic examples, published documents and independent SPA showroom for Quad-Dimensional DataMatrix. This repository is an RfD, **not** a production authorization service.

## Read before editing
- `README.md`, `README.pt.md`, `README.it.md` and `CITATION.cff`
- `docs/model.md`, `docs/scope-and-limitations.md`, `docs/app-state-flow.md`
- `src/qddm/`, `examples/`, `experiments/case_study.py`, `results/hex-gif-case-study.json`
- `tools/authorship/attribution-policy.json`, `LICENSE`, `REUSE.toml`

## Invariants: scientific meaning
1. Candidate catalogue cardinality `64^4=16,777,216` differs from selected module count and actual gross payload (192 KiB per full 64-frame profile).
2. One of up to 64 palette entries is selected per effective module. Each dimension choice represents at most 6 bits; hexadecimal *display width* is not entropy.
3. Distinguish the data-bearing 16-state indexed GIF, which recovers 48 KiB exactly, from the separate recording of the state-selection app.
4. The original app copies a **public** six-character hexadecimal value, not a validated secret or accepted authentication token. Don't claim encryption, anti-replay, strong authentication or camera tolerance.
5. App state cadence (default one minute) differs from the transport study's nominal 8 frames/s. Never conflate candidate tuples/s with throughput of data bytes.
6. Proposed use cases (including Unicode transport or service verification) must be marked **discussion candidates** until independently implemented and evaluated.

## Authorship and provenance
The human authors are João Paulo De Luca Jr and Jorge Luiz Espanhol, and the archive citation is DOI `10.5281/zenodo.23968974`. Preserve both names, repository attribution notices, MIT licensing, Zenodo version metadata, and AI-assisted development disclosure. Do not silently rewrite published PDF evidence.

## Agent skills
- `.agents/skills/encoded-gif-integrity/SKILL.md`: use for data encoding, modules, payload arithmetic, recovery, tests and reproducibility.
- `.agents/skills/research-showroom/SKILL.md`: use for interactive scientific communication, viewer integration, SEO, responsiveness and Pages.
Choose the smallest relevant set; skills add workflow guidance without overruling repository evidence or higher-priority instructions.

## Work and release protocol
Work in scoped branches; prefer a reviewed PR. Preserve unrelated work. For algorithm changes run `make test`, `make viewer-test`, `make case-study` and compare exact SHA-256 reports. For the public site run `node tests/test_viewer.cjs` and `node --test showcase/tests/smoke.test.cjs`. Run `make authorship-test`, `make authorship-check`, `make reuse-check` and `make verify` when dependencies are present; document unavailable checks rather than claiming success.

The verification policy prohibits retired representation names and unexpected image formats. Do not introduce incompatible formats or unsupported scientific claims for cosmetic purposes.

## Publishing
The research showroom is published only by `workflow_dispatch` using SHA-pinned official Actions; never trigger on push or independently publish a new DOI or npm package. Require maintainer approval before merging/publishing. Keep `examples/` as the canonical viewer and generated data source; the site stages those exact assets instead of reproducing them.
