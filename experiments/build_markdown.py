#!/usr/bin/env python3
"""Produce a readable GitHub Markdown rendering of the LaTeX manuscript."""
import re
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
paper = root / "paper"
args = ["pandoc", "main.tex", "--from=latex", "--to=gfm+tex_math_dollars", "--citeproc", "--bibliography=references.bib", "--metadata", "reference-section-title=Referências"]
body = subprocess.run(args, cwd=paper, capture_output=True, text=True, check=True).stdout
body = re.sub(r'<div class="otherlanguage">\s*english\s*(.*?)\n</div>', r'\1', body, flags=re.S)
body = body.replace("figures/channel-errors.pdf", "figures/channel-errors.png")
body = body.replace("figures/constellation-capacity.pdf", "figures/constellation-capacity.png")
latex = (paper / "main.tex").read_text()
abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", latex, re.S).group(1)
abstract_md = subprocess.run(["pandoc", "--from=latex", "--to=gfm+tex_math_dollars"], input=abstract, capture_output=True, text=True, check=True).stdout.strip()
header = "# datamatrix-payload: capacidade, geometria de cores e transporte visual autenticado\n\n"
header += "**Juninho De Luca · Cecil-IA Labs**\n\n4 de novembro de 2026 · Manuscrito v0.1 · Circulação privada\n\n"
header += "[PDF completo com equações numeradas](datamatrix-payload-paper-v0.1.pdf) · [Fonte LaTeX](main.tex) · [BibTeX](references.bib)\n\n"
header += "## Resumo\n\n" + abstract_md + "\n\n"
(paper / "paper.md").write_text(header + body)
print("Generated paper/paper.md with figures and bibliography.")
