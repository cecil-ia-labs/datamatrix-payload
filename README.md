# Quad-Dimensional DataMatrix

**Request for Discussion (RfD), version 0.2.0.**

**João Paulo De Luca Jr · Jorge Luiz Espanhol**

Cecil-IA Labs · 4 November 2026

[Português](README.pt.md) · [English paper](paper/quad-dimensional-datamatrix.en.pdf) · [Portuguese paper](paper/quad-dimensional-datamatrix.pt.pdf)

Quad-Dimensional DataMatrix explores a catalogue with four logical coordinates: horizontal position, vertical position, temporal state, and hexadecimal dimension. An indexed GIF carries the corresponding sequence. English is the default language; Portuguese is the alternative.

## Working profile

| Property | Current discussion profile |
|---|---|
| Container | Indexed GIF |
| Stored frame | 256 × 256 pixels |
| Effective matrix | 64 × 64 modules |
| Module | 4 × 4 identical indexed pixels |
| Palette | Up to 64 distinct hexadecimal entries |
| Sequence | Up to 64 frames |
| Transport example | 8 frames per second |
| App interaction example | One state per minute; click to pause and copy |

The public mapping is:

**dimension ↔ palette index ↔ hexadecimal value**

The prototype uses complete frames and power-of-two palettes. Its colour values are written exclusively as six-digit hexadecimal entries such as `#12ABEF`.

## Catalogue and payload

For the maximum profile:

$$|\Omega|=64\cdot64\cdot64\cdot64=16{,}777{,}216.$$

This counts candidate four-coordinate tuples. At an eight-second nominal cycle, it gives **2,097,152 candidate tuples per second**. There are 262,144 selected modules per cycle; each selects one of 64 entries and carries six bits.

| Quantity | Maximum profile at 8 fps |
|---|---:|
| Candidate catalogue entries | 16,777,216 |
| Selected modules per cycle | 262,144 |
| Raw payload per frame | 3 KiB |
| Raw payload per 64-frame cycle | 192 KiB |
| Nominal raw payload rate | 24 KiB/s |

See [the mathematical model](docs/model.md) for the derivation and [Scope and Limitations](docs/scope-and-limitations.md) for the interpretation.

## State selection in the app

The sequence resides in the **app**. A user, service, or website consumes a selected state. The app can advance at one state per minute, independently of the transport example. Clicking the matrix pauses the displayed state and copies its hexadecimal code.

The [local viewer](examples/index.html) implements this interaction in English and Portuguese. It starts at one state per minute and includes faster study cadences. The demonstration copies the complete state payload as hexadecimal text.

From the repository root:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://localhost:8000/examples/`. [Interaction model](docs/app-state-flow.md).

## Reproduce the case study

Python 3.11 or newer. The recorded environment uses Python 3.12.14.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.lock.txt
.venv/bin/pip install --no-deps -e .
make PYTHON=.venv/bin/python test
make PYTHON=.venv/bin/python case-study
```

The [16-state GIF](examples/quad-dimensional-datamatrix-16-states.gif) contains **48 KiB** of synthetic payload in a 256 × 256 pixel animation. The decoder recovers the original hexadecimal payload exactly. [Machine-readable results](results/hex-gif-case-study.json).

The app event checks can be run with `make viewer-test` (Node.js).

Tests also exercise the 64-frame boundary, repeated states, palette order, truncated input, inconsistent modules, one-frame-per-minute timing, catalogue addresses, and Unicode scalar mappings.

### Build and verify the PDFs

Both PDF editions are already available in `paper/`. Regenerating them additionally requires **Pandoc** and **pdfLaTeX (TeX Live)** as system tools, installed separately from the Python dependencies. On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install --no-install-recommends pandoc texlive-latex-extra \
  texlive-fonts-recommended texlive-lang-portuguese lmodern poppler-utils
```

These packages provide the document converter, LaTeX engine, packages, fonts, and Portuguese language support. `poppler-utils` provides `pdftotext` for repository verification. See the [Pandoc installation guide](https://pandoc.org/installing.html).

Then, from the repository root with the Python environment prepared above:

```bash
make PYTHON=.venv/bin/python paper
make PYTHON=.venv/bin/python verify
```

The build checks that `pandoc` and `pdflatex` are on `PATH` before generating files. It builds both languages, writes compilation logs to `output/pdf/`, and copies the resulting PDFs to `paper/`.

## Discussion and papers

- [English manuscript](paper/quad-dimensional-datamatrix.en.md) and [PDF](paper/quad-dimensional-datamatrix.en.pdf).
- [Portuguese manuscript](paper/quad-dimensional-datamatrix.pt.md) and [PDF](paper/quad-dimensional-datamatrix.pt.pdf).
- [Open questions](docs/discussion.md), including the proposed one-to-one Unicode-to-hexadecimal mapping.
- [Technical references](docs/technical-references.md).
- [Scope and Limitations](docs/scope-and-limitations.md).

The text and code are discussion material. A later stage may propose a specification. The authors' names and contribution record are provided in [CITATION.cff](CITATION.cff). Implementation and editorial assistance by ChatGPT/Codex is acknowledged in both papers. The repository retains its [license](LICENSE).
