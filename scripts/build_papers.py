# SPDX-FileCopyrightText: 2026 Cecil-IA Labs
# SPDX-License-Identifier: MIT
#
# Author: João Paulo De Luca Jr.; Jorge Luiz Espanhol
# Organization: Cecil-IA Labs
# Project: Quad-Dimensional DataMatrix
#
# AI-assisted development:
# OpenAI ChatGPT and Codex were used as development tools.
# Human-directed development and integration.
# No OpenAI sponsorship, affiliation, or endorsement is implied.
#
# License: See the repository LICENSE file and SPDX identifier above.

"""Build equivalent English and Portuguese PDF editions from Markdown."""
from pathlib import Path
import shutil
import subprocess

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def check_pdf_tools() -> None:
    missing = [tool for tool in ("pandoc", "pdflatex") if shutil.which(tool) is None]
    if missing:
        raise SystemExit(
            "Cannot build the papers: missing executables on PATH: "
            + ", ".join(missing)
            + ".\nPDF builds require system tools in addition to the Python environment.\n"
            "On Ubuntu/Debian, install them with:\n"
            "  sudo apt update\n"
            "  sudo apt install --no-install-recommends pandoc texlive-latex-extra "
            "texlive-fonts-recommended texlive-lang-portuguese lmodern\n"
            "Then rerun: make PYTHON=.venv/bin/python paper\n"
            "See README.md or README.pt.md for the full PDF setup."
        )


def main():
    check_pdf_tools()
    figures = ROOT / "paper/figures"
    figures.mkdir(parents=True, exist_ok=True)
    with Image.open(ROOT / "docs/media/quad-dimensional-datamatrix-poc.gif") as recording:
        recording.seek(recording.n_frames // 2)
        recording.convert("P", palette=Image.Palette.ADAPTIVE, colors=256).save(
            figures / "concept-app.pdf", resolution=144
        )
    output = ROOT / "output/pdf"
    output.mkdir(parents=True, exist_ok=True)
    for language in ("en", "pt"):
        stem = f"quad-dimensional-datamatrix.{language}"
        for extension in (".aux", ".out", ".toc"):
            (output / (stem + extension)).unlink(missing_ok=True)
        source = ROOT / "paper" / (stem + ".md")
        tex = ROOT / "paper" / (stem + ".tex")
        subprocess.run([
            "pandoc", str(source), "--standalone", "--from=markdown+tex_math_dollars",
            "--to=latex", "--number-sections", "--no-highlight", "--include-in-header",
            str(ROOT / "paper/preamble.tex"), "--output", str(tex),
        ], cwd=ROOT / "paper", check=True)
        command = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                   "-output-directory=" + str(output), str(tex)]
        for _ in range(2):
            result = subprocess.run(command, cwd=ROOT / "paper", capture_output=True, text=True,
                                    encoding="utf-8", errors="replace")
            (output / (stem + ".build.log")).write_text(
                result.stdout + result.stderr, encoding="utf-8")
            if result.returncode:
                raise RuntimeError((result.stdout + result.stderr)[-6000:])
        artifact = output / (stem + ".pdf")
        shutil.copyfile(artifact, ROOT / "paper" / artifact.name)
        print(f"Built {artifact.name}: {artifact.stat().st_size} bytes")

if __name__ == "__main__":
    main()

