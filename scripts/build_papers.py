"""Build equivalent English and Portuguese PDF editions from Markdown."""
from pathlib import Path
import shutil
import subprocess

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
    output = ROOT / "output/pdf"
    output.mkdir(parents=True, exist_ok=True)
    for language in ("en", "pt"):
        stem = f"quad-dimensional-datamatrix.{language}"
        source = ROOT / "paper" / (stem + ".md")
        tex = ROOT / "paper" / (stem + ".tex")
        subprocess.run([
            "pandoc", str(source), "--standalone", "--from=markdown+tex_math_dollars",
            "--to=latex", "--number-sections", "--include-in-header",
            str(ROOT / "paper/preamble.tex"), "--output", str(tex),
        ], cwd=ROOT, check=True)
        command = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                   "-output-directory=" + str(output), str(tex)]
        for _ in range(2):
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
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

