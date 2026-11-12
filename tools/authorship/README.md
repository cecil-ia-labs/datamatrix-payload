<!--
SPDX-FileCopyrightText: 2026 Cecil-IA Labs
SPDX-License-Identifier: MIT

Author: João Paulo De Luca Jr.; Jorge Luiz Espanhol
Organization: Cecil-IA Labs
Project: Quad-Dimensional DataMatrix

AI-assisted development:
OpenAI ChatGPT and Codex were used as development tools.
Human-directed development and integration.
No OpenAI sponsorship, affiliation, or endorsement is implied.

License: See the repository LICENSE file and SPDX identifier above.
-->

> **Quad-Dimensional DataMatrix trial:** This kit is staged for evaluation only; it does not rewrite existing project files. The repository keeps its MIT license and coauthors João Paulo De Luca Jr. and Jorge Luiz Espanhol. For a first run, use the project-specific preview command at the end of this document. Review ownership and contributor attribution before applying to any file.

# Open-source authorship & AI transparency kit

**Goal:** identify the human author, project/organization and factual use of AI
coding tools without restricting an existing open-source license.

- Author: **João Paulo De Luca**
- Organization: **Cecil-IA Labs**
- AI tools (where actually used): **OpenAI ChatGPT and Codex**
- License: **the existing SPDX license of each repository**, not one universal license

The tool **does not relicense** a repository, change an existing `LICENSE`, or overwrite
third-party copyright declarations. It requires Python 3.10+ and has no external dependencies.
It previews changes by default; use `--apply` after reviewing the preview.

## 1. Inspect a repository's actual license

```bash
cd /path/to/repository
ls -la LICENSE* COPYING* 2>/dev/null || true
head -40 LICENSE 2>/dev/null || true
git status --short
```

Do **not** automatically use MIT if the project already uses Apache-2.0, GPL, LGPL,
MPL or another license. If some directories/files have different licenses, run on
separate directories using the correct identifiers, and/or exclude third-party code.
Never claim copyright in code you don't own.

## 2. Preview

```bash
python3 /path/to/authorship_headers.py . \
  --holder 'Cecil-IA Labs' \
  --author 'João Paulo De Luca' \
  --organization 'Cecil-IA Labs' \
  --year '2023-2026' \
  --license 'MIT' \
  --project 'Example Open Source Project' \
  --exclude 'third_party/**'
```

The year range and MIT license above are **examples**. Verify actual years and rights.
If the copyright is legally owned by João Paulo rather than Cecil-IA Labs, use
`--holder 'João Paulo De Luca'` and keep `--organization 'Cecil-IA Labs'`.

## 3. Apply and validate

Repeat the preview command with `--apply`:

```bash
python3 /path/to/authorship_headers.py . \
  --holder 'Cecil-IA Labs' --author 'João Paulo De Luca' \
  --organization 'Cecil-IA Labs' --year '2023-2026' \
  --license 'MIT' --apply

git diff --check
git diff --stat
git diff
```

`--check` exits 1 if candidate source files still lack notices; it exits 0 when
complete. Existing copyright/SPDX headers are skipped by default.

## 4. Existing first-party headers

Use `--annotate-existing` to add **AI credit only**, without adding a second
SPDX-License-Identifier or changing an existing license:

```bash
python3 /path/to/authorship_headers.py . \
  --holder 'Cecil-IA Labs' --author 'João Paulo De Luca' \
  --organization 'Cecil-IA Labs' --year '2023-2026' \
  --license 'MIT' --annotate-existing
```

After reviewing, repeat with `--apply`. This option only affects headers whose
copyright line contains the selected copyright holder. If the file shows other
copyright holders, review it manually. It leaves third-party headers untouched.
The `--license` argument is required for new headers; when adding AI-only notices
it does not overwrite existing SPDX license IDs.

## 5. What gets processed

The script supports Python, shell, JavaScript, TypeScript, HTML, CSS, Markdown,
YAML, TOML, C/C++, Rust, Go, SQL, and other commentable source files.
It preserves shebangs, Python encoding declarations, Markdown front matter,
XML declarations, HTML doctypes, UTF-8 BOM and CRLF line endings. It skips
JSON, binary assets, lockfiles, most generated files, `node_modules`, `vendor`,
`dist`, etc. In a Git repo it honors `.gitignore` by default.

Use `--exclude 'dir/**'` to omit more paths. For binary assets and
non-commentable files, use REUSE `.license` sidecar files or `REUSE.toml`.
A complete REUSE setup needs full license texts in `LICENSES/`.

## 6. Repository-level disclosure

Use `templates/AI_DEVELOPMENT.md` as a starting point for a single, transparent
repository-wide record of AI-assisted development. For a README badge, a simple
text link is safer than a product logo or endorsement claim.

## Important limits

- This script cannot infer legal rights, copyright ownership, original creation dates,
  whether a file was AI-assisted, or the correct license of every file.
- Do not use it on source code or other files belonging exclusively to third parties.
- An AI-assistance notice is descriptive, **not** a license condition.
- Tool names are nominative references; no OpenAI sponsorship/partnership is implied.
- The licenses and permissions already granted to recipients remain in force.

Reference: https://reuse.software/spec/ , https://spdx.org/licenses/ .

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Quad-Dimensional DataMatrix: scoped attribution and reproducible builds

The **current experimental branch** already contains first-party SPDX headers
in source, documentation, examples, and manuscripts. The purpose of subsequent
runs is to check **future files**; existing notices are not silently rewritten.

From the repository root:

```bash
python3 tools/authorship/authorship_headers.py . \
  --holder 'Cecil-IA Labs' \
  --author 'João Paulo De Luca Jr.; Jorge Luiz Espanhol' \
  --organization 'Cecil-IA Labs' \
  --year '2026' \
  --license 'MIT' \
  --project 'Quad-Dimensional DataMatrix' \
  --policy tools/authorship/attribution-policy.json \
  --check
```

`--check` covers commentable source. The JSON policy defines ordered
first-party overrides and explicit opt-outs for generated files and third-party
directories; **last matching rule wins per attribute**. It is not a tool for
asserting copyright ownership. For new files with uncertain ownership, stop and
review their provenance. Use `--apply` only after checking the preview.

### Generated artifacts

- `examples/state-data.js` is reproduced by `make case-study`, using the
  dedicated, versioned `templates/generated-state-data.header.txt` file.
  Regeneration preserves its SPDX notice and the authors credited in the
  published RfD. Do **not** run a separate post-build header injector.
- `paper/*.tex` are generated by Pandoc; their licensing is declared in the
  root `REUSE.toml` so that LaTeX regeneration cannot erase their metadata.
  `paper/preamble.tex` is maintained manually and contains a native TeX header.
- `paper/*.pdf` contain human author attribution supplied by the manuscripts.
  The PDF, visual media, synthetic GIF, and JSON results are additionally
  covered by `REUSE.toml` without rewriting any binary bytes or hashes.
- `output/` and `dist/` are transient/ignored build directories. The output
  of a build must inherit the corresponding source attribution. Archives
  published from `dist/` must carry the license and relevant notice files.

### REUSE compliance

`REUSE.toml` declares MIT coverage for non-commentable, generated and binary
first-party artifacts. `LICENSES/MIT.txt` is the verbatim license text;
the top-level `LICENSE` remains in place. All REUSE metadata reflects the
current project's MIT terms, **not a new license**.

For local validation, install the independent REUSE command-line tool and run:

```bash
make authorship-test
# Install REUSE inside the project's existing virtual environment:
.venv/bin/python -m pip install reuse
make reuse-check
```

If .venv does not exist yet, run `python3 -m venv .venv` first.
Ubuntu's system Python uses PEP 668, which blocks installing Python packages
into the externally managed system environment. Do not use
`--break-system-packages`. An alternative is `pipx install reuse`, followed
by `make reuse-check` when `reuse` is available on PATH. The Makefile chooses
`.venv/bin/reuse` automatically when present; override with
`make reuse-check REUSE=/path/to/reuse` if needed.

The REUSE installation is optional for using the header script. The
branch's CI workflow runs the same lint and unit checks. The CI check
does not replace review of rights, author lists or embedded third-party code.

### Contributors and third-party licensing

Cecil-IA Labs is the copyright holder indicated by the existing `LICENSE`.
The RfD's publication credits list **João Paulo De Luca Jr. and Jorge Luiz
Espanhol**. For individual files whose human contributors cannot be
established, a neutral *project contributors* attribution is preferable to
inventing per-file coauthorship. **Do not remove, replace or relabel any
third-party license or copyright notice.** Keep third-party code out of bulk
first-party annotation; when redistributed, retain the upstream notices and
their license texts. An AI-assistance acknowledgement is a process disclosure,
not a copyright assignment or a source-code license condition.
