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

# Quad-Dimensional DataMatrix: Zenodo deposit preparation

[Português](pt/publication.md) · [Project](../README.md) · [Release notes](release-notes.md)

**Published record:** [RfD 0.2.0](https://doi.org/10.5281/zenodo.23968974). Version DOI: `10.5281/zenodo.23968974`. All-version DOI: `10.5281/zenodo.23968973`. The steps below document the original preparation; updates to published files use a new Zenodo version. The deposited source archive preserves commit `b7d7ec5c93fc5445b49a40964ad4724244a6a6a4`. A package generated from the current checkout includes citation metadata added after publication; the exact archived files are available from the Zenodo record.

## Record identity

The primary research object is **RfD 0.2.0**, a technical report accompanied by a working implementation and reproducible examples. Prepare one record containing the two language editions and supporting material.

| Field | Prepared value |
|---|---|
| Title | Quad-Dimensional DataMatrix: Request for Discussion |
| Resource type | Publication / Report |
| Version | 0.2.0; proposed Git tag `v0.2.0` |
| Report date | 2026-11-04 |
| First creator | João Paulo De Luca Jr; family name `De Luca Jr`, given names `João Paulo` |
| Second creator | Jorge Luiz Espanhol; family name `Espanhol`, given names `Jorge Luiz` |
| Primary language | English (`eng`); complete Portuguese edition included |
| Report publisher | Cecil-IA Labs |
| Access | Open |
| License | MIT, as currently provided in the repository |
| DOI | [10.5281/zenodo.23968974](https://doi.org/10.5281/zenodo.23968974) |
| Source repository | [cecil-ia-labs/datamatrix-payload](https://github.com/cecil-ia-labs/datamatrix-payload) |

No ORCID, ROR, funding, or individual institutional affiliation has been supplied in the project's citation metadata. Those optional fields are omitted. Cecil-IA Labs is the project and report-publisher identity shown in the manuscripts.

## Metadata files

- [.zenodo.json](../.zenodo.json) supplies the technical-report metadata in Zenodo's documented deposit format. Its description includes an English abstract and a Portuguese summary. The package copies it to `zenodo-metadata.json`; uploading that JSON as an attachment alone does not fill the web form.
- [CITATION.cff](../CITATION.cff) supplies GitHub's citation information. The top-level `software` type describes the implementation; `preferred-citation.type: report` selects the RfD as the preferred scholarly citation. The same two creators and version occur in both files.
- [Release notes](release-notes.md) describe the contents and evidence of the prepared version.

Zenodo gives `.zenodo.json` precedence over `CITATION.cff` during GitHub release archiving. Keep both files synchronized. The publication packaging command checks their title, author order, version, date, and license against the project and study metadata.

## Build a reviewable deposit package

With the dependencies from the [README](../README.md) installed:

```bash
make PYTHON=.venv/bin/python test viewer-test case-study paper verify
# In a Git checkout, stage intentionally added release files before packaging.
make PYTHON=.venv/bin/python publication
```

The preparation script includes files from the Git index and reads their current working-tree bytes. It does not collect untracked files. In an extracted source archive it uses the supplied source manifest. It excludes repository internals, local environments, caches, build output, and `.initial/`. It creates:

| File inside `dist/zenodo-v0.2.0/` | Deposit role |
|---|---|
| `quad-dimensional-datamatrix.en.pdf` | English technical report; select as the default preview |
| `quad-dimensional-datamatrix.pt.pdf` | Equivalent Portuguese technical report |
| `quad-dimensional-datamatrix-0.2.0-source.zip` | Source snapshot, figures, data-bearing GIF, app, results, tests, documentation, and both presentation recordings |
| `quad-dimensional-datamatrix-poc.webm` | Separately playable interface walkthrough |
| `zenodo-metadata.json` | Prepared record fields |
| `release-notes.en.md`, `release-notes.pt.md` | Bilingual contents and evidence |
| `publication-guide.en.md`, `publication-guide.pt.md` | Copies of the deposit instructions |
| `source-manifest.json` | Source paths, sizes, hashes, and base-commit provenance |
| `SHA256SUMS` | Checksums of all other files in this deposit folder |

The outer `dist/quad-dimensional-datamatrix-0.2.0-zenodo.zip` is a convenient download of the whole preparation folder. Extract it before selecting the individual deposit files. It is distinct from the inner source archive.

Check the preparation folder before upload:

```bash
cd dist/zenodo-v0.2.0
sha256sum --check SHA256SUMS
```

The source archive includes the same `source-manifest.json`. It identifies the base commit, whether working files differed from that commit at packaging time, and every included file's SHA-256. Its byte-level manifest remains the source identity even when a commit is made after preparation. Unzip the source archive and run `make verify` to check it without Git metadata; the Python dependencies and `pdftotext` must be available.

## Save a draft and reserve a DOI

1. Sign in to Zenodo and choose **New upload** from the dashboard.
2. Select the two PDFs, source archive, WebM, notes, metadata, source manifest, and checksum file from the preparation folder.
3. Enter the title, resource type, version, ordered creators, language, license, abstract, and remaining fields from `zenodo-metadata.json`. Preserve accents and the coauthor order. The report date is 4 November 2026; ensure the form's publication date describes the object's actual first public availability.
4. Choose **No** for an existing DOI. If a DOI is needed inside the PDFs before publication, use **Get a DOI now!** and retain the actual reserved DOI.
5. Save the draft. Set the English PDF as the default preview, check both reports, and verify the filenames and metadata in Preview.
6. If a DOI was reserved, add it to both manuscript editions and the main and preferred citations, regenerate the PDFs, rebuild the package, and replace the draft files. Do not put a DOI belonging to a different work into these files.
7. Keep the completed draft for the authors' publication decision. The preparation command does not upload, reserve an identifier, create a Git tag or GitHub release, or publish.

A reserved DOI becomes registered when the record is published. Do not delete a draft whose reserved DOI has already been inserted into the reports. After publication, copy the actual version DOI and record URL into the citation metadata and README links.

## GitHub release route

The proposed release tag is `v0.2.0`. If the repository is enabled in Zenodo's GitHub integration, publishing a GitHub release triggers archiving. Choose that route or the manual report deposit deliberately so that the same release does not acquire duplicate records accidentally. A draft GitHub release does not replace a completed Zenodo deposit.

## Official guidance

- [Create an upload, save a draft, and reserve a DOI](https://help.zenodo.org/docs/deposit/create-new-upload/).
- [Describe software and metadata precedence](https://help.zenodo.org/docs/github/describe-software/).
- [Zenodo JSON metadata](https://help.zenodo.org/docs/github/describe-software/zenodo-json/).
- [Deposit metadata API fields](https://developers.zenodo.org/#deposit-metadata).
- [Archive a GitHub release](https://help.zenodo.org/docs/github/archive-software/github-upload/).
