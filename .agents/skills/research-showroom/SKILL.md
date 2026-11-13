---
name: research-showroom
description: Explain DataMatrix four-coordinate concepts with the original 16-state application and evidence-backed GIF recovery, without overselling experimental claims.
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
# DataMatrix research showroom

Use for `showcase/`, page narratives, case-study demonstrations, author metadata, accessibility, i18n and manual Pages deployment.

1. Treat `examples/index.html`, `examples/viewer.js`, `examples/state-data.js` and the real indexed GIF as authoritative. Reuse these assets; never generate a different data set and call it the reproduced study.
2. Show X, Y, palette dimension C and temporal state T. The coordinate inspector must compute `d` from `module_indices_hex`, select `palette_hex[d]` and calculate the catalogue address using the paper's definition.
3. Explain what the code-selection app proves versus the indexed transport recovery. The code is public; no authentication-security claim is established.
4. Mark other potential use cases as prospective research. Do not imply interoperability, verified key management, capture tolerance or byte/s speed beyond the measured digital case.
5. Run `node --test showcase/tests/smoke.test.cjs` and `node tests/test_viewer.cjs`, then review focus order, labels, mobile frame sizing, actual viewer embedding and fallback links in a browser.
6. The deploy is manual, with GitHub Pages staged at the project path. Include the original `examples/`, report JSON, root sitemap and robots file. No automatic Actions, new DOI or external processing.
7. Preserve original authorship/AI-assisted header policy, including when updating new files.
