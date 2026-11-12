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

"""Prepare and verify local Zenodo upload files; no network or publishing actions."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tomllib
import zipfile
from datetime import date
from pathlib import Path

from verify_repository import ROOT, public_files


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def cff_value(text: str, key: str, indent: str = "") -> str:
    """Read an explicit scalar from this project's quoted CFF metadata."""
    match = re.search(rf"^{indent}{re.escape(key)}: (.+)$", text, re.MULTILINE)
    if match is None:
        raise ValueError(f"Missing citation field: {indent}{key}")
    return match.group(1).strip().strip('"')


def validate_metadata() -> dict:
    metadata = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    report = json.loads((ROOT / "results/hex-gif-case-study.json").read_text())
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    preferred = citation.split("preferred-citation:\n", 1)[1].split("\nkeywords:", 1)[0]
    version = project["version"]
    title = report["title"] + ": Request for Discussion"
    for name, text, indent in (("citation", citation, ""), ("preferred citation", preferred, "  ")):
        if cff_value(text, "title", indent) != title or cff_value(text, "version", indent) != version:
            raise ValueError(f"Inconsistent {name} title/version")
    if metadata["title"] != title or metadata["version"] != version or report["version"] != version:
        raise ValueError("Inconsistent project/report/deposit title or version")
    if metadata["upload_type"] != "publication" or metadata["publication_type"] != "report":
        raise ValueError("The prepared primary object must be a publication/report")
    if cff_value(preferred, "type", "  ") != "report":
        raise ValueError("The preferred citation must describe the report")
    release_date = metadata["publication_date"]
    date.fromisoformat(release_date)
    if release_date != cff_value(citation, "date-released") or release_date != cff_value(preferred, "date-published", "  "):
        raise ValueError("Inconsistent report dates")
    pairs = re.findall(r'family-names: "([^"]+)"\s+given-names: "([^"]+)"', citation)
    count = len(report["authors"])
    if len(pairs) != 2 * count or pairs[:count] != pairs[count:]:
        raise ValueError("Citation author order differs between implementation and report")
    if [given + " " + family for family, given in pairs[:count]] != report["authors"]:
        raise ValueError("Citation and study authors differ")
    if [author["name"] for author in project["authors"]] != report["authors"]:
        raise ValueError("Project and study authors differ")
    if [creator["name"] for creator in metadata["creators"]] != [family + ", " + given for family, given in pairs[:count]]:
        raise ValueError("Deposit creator names or order differ")
    if metadata["license"] != "mit" or cff_value(citation, "license") != "MIT" or not (ROOT / "LICENSE").read_text().startswith("MIT License"):
        raise ValueError("Inconsistent project license")
    if metadata["access_right"] != "open" or metadata["language"] != "eng":
        raise ValueError("Unexpected access or primary language")
    for key in ("description", "notes", "method", "keywords", "references", "related_identifiers"):
        if not metadata.get(key):
            raise ValueError(f"Missing deposit metadata: {key}")
    publisher = preferred.split("  publisher:\n", 1)[1]
    if metadata["imprint_publisher"] != cff_value(publisher, "name", "    "):
        raise ValueError("Deposit and preferred-citation report publishers differ")
    citation_doi = re.search(r'^doi: "([^"]+)"$', citation, re.MULTILINE)
    preferred_doi = re.search(r'^  doi: "([^"]+)"$', preferred, re.MULTILINE)
    if len({metadata.get("doi"), citation_doi.group(1) if citation_doi else None,
            preferred_doi.group(1) if preferred_doi else None}) != 1:
        raise ValueError("Deposit, citation, and preferred-citation DOI differ")
    media = json.loads((ROOT / "docs/media/manifest.json").read_text())
    for entry in media["outputs"].values():
        data = (ROOT / "docs/media" / entry["file"]).read_bytes()
        if len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
            raise ValueError(f"Media checksum differs: {entry['file']}")
    study = report["case_study"]
    if digest((ROOT / study["artifact"]).read_bytes()) != study["gif_sha256"]:
        raise ValueError("Case-study GIF checksum differs")
    return metadata


def source_files() -> tuple[list[Path], dict]:
    if (ROOT / ".git").exists():
        files = public_files()
        provenance = {
            "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "working_tree_differs_from_base": bool(subprocess.check_output(
                ["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT, text=True).strip()),
            "selection": "Git index paths; bytes from the current working tree",
        }
    else:
        previous = json.loads((ROOT / "source-manifest.json").read_text())
        files = [ROOT / item["path"] for item in previous["files"]]
        provenance = {"selection": "Source manifest paths; bytes from the extracted source tree",
                      "original_provenance": previous["provenance"]}
    for path in files:
        relative = path.relative_to(ROOT)
        if path.is_symlink() or not path.is_file() or any(
            part in {".git", ".venv", ".initial", "dist", "output", "tmp", "__pycache__"}
            for part in relative.parts
        ):
            raise ValueError(f"Unexpected source archive entry: {relative}")
    return files, provenance


def add_bytes(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    entry = zipfile.ZipInfo(name, (2026, 11, 4, 0, 0, 0))
    entry.compress_type = zipfile.ZIP_DEFLATED
    entry.external_attr = 0o100644 << 16
    archive.writestr(entry, data)


def main() -> None:
    metadata = validate_metadata()
    version = metadata["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Unexpected version format")
    folder = ROOT / "dist" / f"zenodo-v{version}"
    if folder.is_symlink():
        raise ValueError("Refusing a linked publication output directory")
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)
    files, provenance = source_files()
    required = {".zenodo.json", "CITATION.cff", "scripts/prepare_publication.py", "paper/figures/concept-app.pdf",
                "docs/publication.md", "docs/pt/publication.md", "docs/release-notes.md", "docs/pt/release-notes.md"}
    selected = {path.relative_to(ROOT).as_posix() for path in files}
    if missing := required - selected:
        raise ValueError(f"Required source files are missing from the index or manifest: {sorted(missing)}")
    manifest = {"title": metadata["title"], "version": version, "provenance": provenance, "files": []}
    prefix = f"quad-dimensional-datamatrix-{version}/"
    source = folder / f"quad-dimensional-datamatrix-{version}-source.zip"
    with zipfile.ZipFile(source, "w") as archive:
        for path in sorted(files):
            data = path.read_bytes()
            relative = path.relative_to(ROOT).as_posix()
            manifest["files"].append({"path": relative, "bytes": len(data), "sha256": digest(data)})
            add_bytes(archive, prefix + relative, data)
        manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        add_bytes(archive, prefix + "source-manifest.json", manifest_bytes)
    (folder / "source-manifest.json").write_bytes(manifest_bytes)
    for language in ("en", "pt"):
        shutil.copyfile(ROOT / "paper" / f"quad-dimensional-datamatrix.{language}.pdf",
                        folder / f"quad-dimensional-datamatrix.{language}.pdf")
        document_dir = ROOT / "docs" / ("pt" if language == "pt" else "")
        shutil.copyfile(document_dir / "release-notes.md", folder / f"release-notes.{language}.md")
        shutil.copyfile(document_dir / "publication.md", folder / f"publication-guide.{language}.md")
    shutil.copyfile(ROOT / "docs/media/quad-dimensional-datamatrix-poc.webm", folder / "quad-dimensional-datamatrix-poc.webm")
    shutil.copyfile(ROOT / ".zenodo.json", folder / "zenodo-metadata.json")
    checksums = "".join(f"{digest(path.read_bytes())}  {path.name}\n" for path in sorted(folder.iterdir()))
    (folder / "SHA256SUMS").write_text(checksums, encoding="utf-8")
    bundle = ROOT / "dist" / f"quad-dimensional-datamatrix-{version}-zenodo.zip"
    with zipfile.ZipFile(bundle, "w") as archive:
        for path in sorted(folder.iterdir()):
            add_bytes(archive, folder.name + "/" + path.name, path.read_bytes())
    with zipfile.ZipFile(source) as archive:
        if archive.testzip() is not None:
            raise ValueError("Source ZIP integrity check failed")
        for item in manifest["files"]:
            if digest(archive.read(prefix + item["path"])) != item["sha256"]:
                raise ValueError(f"Source archive checksum mismatch: {item['path']}")
    with zipfile.ZipFile(bundle) as archive:
        if archive.testzip() is not None:
            raise ValueError("Deposit bundle integrity check failed")
    print(f"Validated report metadata, ordered creators, MIT license, study and recording checksums.")
    print(f"Prepared {len(manifest['files'])} source files and {len(list(folder.iterdir()))} deposit files.")
    print(f"Deposit folder: {folder}")
    print(f"Review bundle: {bundle} ({bundle.stat().st_size} bytes)")
    print("Local preparation only. No upload, DOI reservation, tag, release, or publication performed.")


if __name__ == "__main__":
    main()
