---
name: encoded-gif-integrity
description: Preserve four-coordinate catalogue mathematics, indexed GIF payload profiles, exact synthetic recovery and scientific reproducibility.
---
<!--
SPDX-FileCopyrightText: 2026 Cecil-IA Labs
SPDX-License-Identifier: MIT
Author: João Paulo De Luca Jr.; Jorge Luiz Espanhol
Organization: Cecil-IA Labs
Project: Quad-Dimensional DataMatrix
AI-assisted development: OpenAI ChatGPT and Codex were used as development tools.
Human-directed development and integration. No OpenAI endorsement is implied.
-->
# Encoded GIF integrity and reproducibility

Use this skill for work in `src/qddm/`, `experiments/`, `examples/state-data.js`, data-bearing GIF, `results/`, testing or numerical claims.

1. Read `docs/model.md`, `docs/scope-and-limitations.md`, `CITATION.cff` and the reproduction report before editing.
2. Keep the effective matrix 64 × 64, 4 × 4 repeated stored pixels per module, max 64 palette entries, max 64 frames, and original payload length semantics explicit.
3. Separate candidate coordinate tuples from selected bytes. At 64 palette entries a module carries six bits; the 64-frame maximum is 192 KiB, nominally 24 KiB/s at eight frames/s.
4. When the encoded state or decoder changes, regenerate with documented seed and pinned environment. Verify original and recovered SHA-256; compare the GIF artifact hash.
5. Run `make test`, `make viewer-test`, `make case-study`, `make verify`, authorship checks and REUSE checks when available. Never assert run results without evidence.
6. Maintain authors' names, MIT attribution, published DOI and scholarly qualifications. Do not claim security or physical-scanning validation from a digital recovery experiment.
