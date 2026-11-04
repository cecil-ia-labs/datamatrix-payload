"""Check the current RfD tree, both PDF editions, links, and hex-GIF evidence."""
from __future__ import annotations
import json
import os
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
IGNORE={".git",".venv","__pycache__","tmp","output","build","dist"}
AUTHORS=("João Paulo De Luca Jr","Jorge Luiz Espanhol")
TITLE="Quad-Dimensional DataMatrix"

def public_files():
    """Scan tracked checkout files, or visible source files in an archive."""
    if (ROOT / ".git").exists():
        try:
            tracked = subprocess.check_output(
                ["git", "ls-files", "--cached", "-z", "--"], cwd=ROOT
            )
        except FileNotFoundError:
            raise SystemExit("Git is required to list files in a repository checkout.")
        paths = {ROOT / os.fsdecode(name) for name in tracked.split(b"\0") if name}
        return sorted(path for path in paths if path.is_file())

    files = []
    for directory, subdirectories, names in os.walk(ROOT):
        subdirectories[:] = [
            name for name in subdirectories
            if not name.startswith(".") and name not in IGNORE
            and not name.endswith(".egg-info")
        ]
        files.extend(
            path for name in names
            if not name.startswith(".") and (path := Path(directory) / name).is_file()
        )
    return sorted(files)

def main():
    files=public_files()
    forbidden_words=tuple(bytes.fromhex(v).decode() for v in ("524742","504e47","4a504547"))
    forbidden_suffixes=tuple("."+bytes.fromhex(v).decode() for v in ("706e67","6a7067","6a706567"))
    for path in files:
        if path.suffix.lower() in forbidden_suffixes:
            raise ValueError(f"Unexpected format: {path}")
        if path.suffix in (".md",".py",".tex",".cff",".toml",".json",".html",".css",".cjs",".js"):
            text=path.read_text(encoding="utf-8")
            if path.name!="state-data.js":
                for word in forbidden_words:
                    if re.search(r"\b"+word+r"\b",text,re.IGNORECASE):
                        raise ValueError(f"Retired representation in {path}")
            if path.suffix==".md":
                for target in re.findall(r"\]\(([^)]+)\)",text):
                    if target.startswith(("https:","http:","#")): continue
                    target=target.split("#")[0]
                    if target and not (path.parent/target).exists():
                        raise ValueError(f"Broken local link {path}: {target}")
    for language,heading in (("en","Scope and Limitations"),("pt","Escopo e limitações")):
        source=ROOT/f"paper/quad-dimensional-datamatrix.{language}.md"
        assert source.read_text().count("# "+heading)==1
        pdf=ROOT/f"paper/quad-dimensional-datamatrix.{language}.pdf"
        text=subprocess.check_output(["pdftotext",str(pdf),"-"],text=True)
        for author in AUTHORS: assert author in text,(pdf,author)
        assert TITLE in text
        assert heading in text
        assert not any(re.search(r"\b"+word+r"\b",text,re.IGNORECASE) for word in forbidden_words)
    report=json.loads((ROOT/"results/hex-gif-case-study.json").read_text())
    assert tuple(report["authors"])==AUTHORS
    assert report["case_study"]["frames"]==16
    assert report["case_study"]["payload_bytes"]==49152
    assert report["case_study"]["exact_recovery"]
    assert report["catalogue"]["full_tuple_count"]==16777216
    assert report["catalogue"]["full_cycle_payload_bytes"]==196608
    assert report["catalogue"]["candidate_tuples_per_second"]==2097152
    assert report["catalogue"]["payload_bytes_per_second_at_8_fps"]==24576
    print(f"Verified {len(files)} RfD files, two PDF editions, local links, and hexadecimal GIF results.")

if __name__=="__main__":
    main()

