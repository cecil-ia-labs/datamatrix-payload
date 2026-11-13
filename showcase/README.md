<!--
SPDX-FileCopyrightText: 2026 Cecil-IA Labs
SPDX-License-Identifier: MIT
Author: João Paulo De Luca Jr.; Jorge Luiz Espanhol
Organization: Cecil-IA Labs
Project: Quad-Dimensional DataMatrix
AI-assisted development: OpenAI ChatGPT and Codex were used as development tools.
Human-directed development and integration. No OpenAI endorsement is implied.
-->
# Quad-Dimensional DataMatrix — research showroom

This site communicates the **Request for Discussion** through an interactive scientific narrative, two distinct evidence-backed examples, and links to the original research. It does not modify the encoding protocol or turn its public study into a deployed authentication product.

## Two original examples, two different purposes

1. **State selection:** The original bilingual viewer in `examples/` cycles through 16 synthetic states, allows a module coordinate to be selected, copies its hexadecimal palette value, and demonstrates pasting it into a receiver circle. The showroom embeds this viewer without rewriting its source.
2. **Data transport:** The original 16-frame indexed GIF in `examples/quad-dimensional-datamatrix-16-states.gif` carries 48 KiB of synthetic module choices. The Python case study recovers those bytes exactly, as documented in `results/hex-gif-case-study.json`.

The additional coordinate explorer reads `examples/state-data.js` directly. It displays the actual 64 × 64 indexed module values for a selected state, the palette index, the hexadecimal entry and a six-digit catalogue address. No new experimental data are fabricated.

## Run locally

From the repository root:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/showcase/`. Browser modules and clipboard permissions require a local web server or a secure host.

Run the static checks and existing viewer checks with:

```bash
node --test showcase/tests/smoke.test.cjs
node tests/test_viewer.cjs
```

## Publish the independent SPA

The manual GitHub Pages workflow at `.github/workflows/publish-showcase.yml` builds a static artefact from `showcase/` and copies the existing `examples/` files and the published case-study JSON into it. It does **not** trigger on a push, execute the case-study generator, or publish a new scientific release.

Canonical URL: `https://cecil-ia-labs.github.io/datamatrix-payload/`.

## Scientific scope

- The (64^4) candidate tuple catalogue must not be confused with the available payload capacity, which is 192 KiB in the maximum 64-frame, 64-entry working profile.
- Six visible hexadecimal characters in the app describe a public palette value, not cryptographic authentication strength.
- Indexed GIF recovery in a digital test is not evidence of robust camera scanning, secret management, entropy, security or interoperability.
- The app default cadence and the transport example's 8 frames/s are distinct timing choices.

For authoritative interpretation, read `docs/model.md`, `docs/scope-and-limitations.md`, `docs/app-state-flow.md` and the archived paper.

Authors: **João Paulo De Luca Jr · Jorge Luiz Espanhol**. © 2026 Cecil-IA Labs; MIT licensed. [Cite the archived RfD](https://doi.org/10.5281/zenodo.23968974).
