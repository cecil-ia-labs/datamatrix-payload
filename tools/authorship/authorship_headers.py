#!/usr/bin/env python3
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

"""Add transparent SPDX/REUSE authorship and AI-assistance notices to OSS files.

Preview by default; --apply to write. Never replaces existing licenses.
--annotate-existing adds AI credit only to existing, first-party headers.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
from pathlib import Path
import re
import subprocess
import sys

COMMENT_STYLES = {
    # Hash-comment files.
    ".py": "hash", ".sh": "hash", ".bash": "hash", ".zsh": "hash",
    ".rb": "hash", ".pl": "hash", ".ps1": "hash",
    ".yaml": "hash", ".yml": "hash", ".toml": "hash", ".ini": "hash",
    ".tf": "hash", ".graphql": "hash",
    # C-family syntax (also used in TS/JS).
    ".js": "block", ".jsx": "block", ".ts": "block", ".tsx": "block",
    ".mjs": "block", ".cjs": "block", ".mts": "block", ".cts": "block",
    ".c": "block", ".cc": "block", ".cpp": "block", ".h": "block",
    ".hpp": "block", ".hxx": "block", ".java": "block", ".kt": "block",
    ".kts": "block", ".swift": "block", ".php": "block",
    ".css": "block", ".scss": "block", ".less": "block",
    ".go": "slash", ".rs": "slash", ".proto": "slash",
    # Document formats.
    ".md": "html", ".mdx": "html", ".html": "html", ".htm": "html",
    ".vue": "html", ".svelte": "html", ".xml": "html", ".svg": "html",
    ".sql": "sql",
}
NAME_STYLES = {
    "Dockerfile": "hash", "Containerfile": "hash", "Makefile": "hash",
    "GNUmakefile": "hash", "CMakeLists.txt": "hash",
}
IGNORE_DIRS = {
    ".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules",
    "dist", "build", "coverage", ".next", ".nuxt", ".cache", ".tox",
    ".mypy_cache", "__pycache__", "vendor", "target", "out", ".turbo",
    "generated", ".generated", "output", "tmp", ".initial",
}
SKIP_NAMES = {
    "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock",
    "Cargo.lock", "LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING",
    "COPYRIGHT", "NOTICE", "CHANGELOG.md", "AI_DEVELOPMENT.md",
}
COPYRIGHT_LINE = re.compile(
    r"(?im)^\s*(?:[#*/<!\- ]*)?(?:SPDX-FileCopyrightText:|"
    r"Copyright\s*(?:\(c\)|©|\d{4}))"
)
PREEXISTING = re.compile(
    r"(?im)^\s*(?:[#*/<!\- ]*)?(?:SPDX-(?:License-Identifier|FileCopyrightText):|"
    r"Copyright\s*(?:\(c\)|©|\d{4}))"
)
SPDX_TOKEN = re.compile(r"[A-Za-z0-9.+-]+\Z")
ENCODING = re.compile(r"coding\s*[:=]\s*[-\w.]+")
AI_MARKER = re.compile(r"(?i)AI-assisted development\s*:")



def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("root", nargs="?", type=Path, default=Path("."),
                   help="Project root or subdirectory")
    p.add_argument("--holder", required=True,
                   help="Actual copyright holder (person or company holding rights)")
    p.add_argument("--author", required=True,
                   help="Human developer/author, e.g. João Paulo De Luca")
    p.add_argument("--organization", default=None,
                   help="Developer organization (does not by itself claim copyright)")
    p.add_argument("--ai-tools", default="OpenAI ChatGPT and Codex",
                   help="Factually used AI coding tools; set to empty to omit AI notes")
    p.add_argument("--license", required=True, dest="license_id",
                   help="Existing project SPDX license ID, e.g. MIT or Apache-2.0")
    p.add_argument("--year", required=True,
                   help="Actual copyright year or range, e.g. 2023-2026")
    p.add_argument("--project", default=None, help="Optional project label")
    p.add_argument("--exclude", action="append", default=[], metavar="GLOB",
                   help="Extra relative-path ignore glob; repeatable")
    p.add_argument("--policy", type=Path, default=None,
                   help="JSON file defining ordered per-path metadata/skip rules")
    p.add_argument("--all-files", action="store_true",
                   help="Walk filesystem instead of respecting Git ignored files")
    p.add_argument("--annotate-existing", action="store_true",
                   help="Add AI credit to existing first-party copyright headers without touching license")
    p.add_argument("--max-bytes", type=int, default=1_000_000,
                   help="Skip unusually large files")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="Modify eligible files")
    mode.add_argument("--check", action="store_true",
                      help="Exit 1 when eligible files still need headers (for CI)")
    args = p.parse_args(argv)
    for field in ("holder", "author", "organization", "ai_tools", "year", "project"):
        value = getattr(args, field, None)
        if value and ("\r" in value or "\n" in value):
            p.error(f"--{field} cannot contain newlines")
    if not SPDX_TOKEN.fullmatch(args.license_id):
        p.error("--license must be one SPDX ID or LicenseRef-* (not a full expression)")
    if not re.fullmatch(r"\d{4}(?:-\d{4})?", args.year):
        p.error("--year must look like YYYY or YYYY-YYYY")
    dates = [int(part) for part in args.year.split("-")]
    if len(dates) == 2 and dates[0] > dates[1]:
        p.error("--year range must be increasing")
    if args.annotate_existing and not args.ai_tools.strip():
        p.error("--annotate-existing requires --ai-tools")
    if args.max_bytes < 1:
        p.error("--max-bytes must be positive")
    if not args.root.exists() or not args.root.is_dir():
        p.error("root must be an existing directory")
    args.root = args.root.resolve()
    args.policy_rules = []
    if args.policy is not None:
        policy_file = args.policy if args.policy.is_absolute() else args.root / args.policy
        try:
            policy = json.loads(policy_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            p.error(f"invalid --policy file: {exc}")
        if not isinstance(policy, dict) or policy.get("version") != 1 or not isinstance(policy.get("rules"), list):
            p.error("--policy must have version=1 and a rules array")
        allowed = {"glob", "skip", "holder", "author", "organization", "project",
                   "ai_tools", "license", "year"}
        for i, rule in enumerate(policy["rules"]):
            if not isinstance(rule, dict) or set(rule) - allowed:
                p.error(f"invalid policy rule #{i + 1}: unsupported attributes")
            if not isinstance(rule.get("glob"), str) or not rule["glob"]:
                p.error(f"invalid policy rule #{i + 1}: glob is required")
            if "skip" in rule and not isinstance(rule["skip"], bool):
                p.error(f"invalid policy rule #{i + 1}: skip must be a boolean")
            for key, value in rule.items():
                if key in ("glob", "skip"):
                    continue
                if not isinstance(value, str) or "\n" in value or "\r" in value:
                    p.error(f"invalid policy rule #{i + 1}: {key} must be single-line text")
                if key == "license" and not SPDX_TOKEN.fullmatch(value):
                    p.error(f"invalid policy rule #{i + 1}: invalid license ID")
                if key == "year" and not re.fullmatch(r"\d{4}(?:-\d{4})?", value):
                    p.error(f"invalid policy rule #{i + 1}: invalid year")
        args.policy_rules = policy["rules"]
    return args


def scoped_args(path: Path, args: argparse.Namespace) -> argparse.Namespace | None:
    """Last matching policy rule wins per attribute; skip rules are explicit."""
    scoped = argparse.Namespace(**vars(args))
    relative = path.relative_to(args.root).as_posix()
    skipped = False
    for rule in args.policy_rules:
        if fnmatch.fnmatchcase(relative, rule["glob"]):
            if "skip" in rule:
                skipped = rule["skip"]
            for key, value in rule.items():
                if key in ("glob", "skip"):
                    continue
                setattr(scoped, "license_id" if key == "license" else key, value)
    return None if skipped else scoped


def style_for(path: Path) -> str | None:
    return NAME_STYLES.get(path.name, COMMENT_STYLES.get(path.suffix.lower()))


def git_files(root: Path) -> list[Path] | None:
    try:
        repo = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
        if repo.stdout.strip() != b"true":
            return None
        files = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-c", "-o", "--exclude-standard", "-z", "--"],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return sorted({root / os.fsdecode(p) for p in files.split(b"\0") if p})


def walk_files(root: Path) -> list[Path]:
    results: list[Path] = []
    for base, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for name in files:
            results.append(Path(base) / name)
    return sorted(results)


def eligible(path: Path, root: Path, excluded: list[str]) -> bool:
    if not path.is_file() or path.is_symlink() or not style_for(path):
        return False
    rel = path.relative_to(root).as_posix()
    if any(part in IGNORE_DIRS for part in path.relative_to(root).parts[:-1]):
        return False
    if path.name in SKIP_NAMES or path.name.endswith((".min.js", ".min.css", ".generated.ts")):
        return False
    if rel.startswith("LICENSES/") or rel.endswith(".license"):
        return False
    return not any(fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(path.name, pat)
                   for pat in excluded)


def header(args: argparse.Namespace, style: str, newline: str,
           *, ai_only: bool = False) -> str:
    text: list[str] = []
    if not ai_only:
        text = [f"SPDX-FileCopyrightText: {args.year} {args.holder}",
                f"SPDX-License-Identifier: {args.license_id}", ""]
    text.append(f"Author: {args.author}")
    if args.organization:
        text.append(f"Organization: {args.organization}")
    if args.project:
        text.append(f"Project: {args.project}")
    if args.ai_tools.strip():
        text.extend(["", "AI-assisted development:",
                     f"{args.ai_tools} were used as development tools.",
                     "Human-directed development and integration.",
                     "No OpenAI sponsorship, affiliation, or endorsement is implied."])
    if not ai_only:
        text.extend(["", "License: See the repository LICENSE file and SPDX identifier above."])
    if style == "hash":
        result = "\n".join("# " + line if line else "#" for line in text)
    elif style == "sql":
        result = "\n".join("-- " + line if line else "--" for line in text)
    elif style == "slash":
        result = "\n".join("// " + line if line else "//" for line in text)
    elif style == "html":
        result = "<!--\n" + "\n".join(text) + "\n-->"
    else:
        result = "/*\n" + "\n".join(" * " + line if line else " *" for line in text) + "\n */"
    return result.replace("\n", newline)


def insertion_point(content: str, path: Path) -> tuple[int, str | None]:
    lines = content.splitlines(keepends=True)
    if not lines:
        return 0, None
    idx = 0
    ext = path.suffix.lower()
    if lines[0].startswith("#!"):
        idx = 1
    if ext in (".yaml", ".yml") and lines[0].startswith("%YAML"):
        return 0, "YAML directive requires manual review"
    if ext == ".go" and any(line.startswith("//go:build") for line in lines[:10]):
        return 0, "Go build constraints require manual review"
    if ext == ".py":
        if idx < min(len(lines), 2) and ENCODING.search(lines[idx]):
            idx += 1
        elif idx == 0 and ENCODING.search(lines[0]):
            idx = 1
    if ext in (".xml", ".svg") and lines[0].lstrip().startswith("<?xml"):
        idx = 1
    if ext in (".html", ".htm") and lines[0].lstrip().lower().startswith("<!doctype"):
        idx = 1
    if ext in (".css", ".scss", ".less") and lines[0].lstrip().lower().startswith("@charset"):
        idx = 1
    if ext == ".php":
        if lines[0].strip() != "<?php":
            return 0, "PHP file does not start with standalone <?php"
        idx = 1
    if ext in (".md", ".mdx") and lines[0].strip() == "---":
        for i in range(1, min(len(lines), 200)):
            if lines[i].strip() in ("---", "..."):
                idx = i + 1
                break
        else:
            return 0, "Unclosed Markdown front matter"
    return sum(len(line) for line in lines[:idx]), None


def prepare(path: Path, args: argparse.Namespace) -> tuple[bytes | None, str]:
    if path.stat().st_size > args.max_bytes:
        return None, "large"
    data = path.read_bytes()
    if b"\0" in data:
        return None, "binary"
    bom = b"\xef\xbb\xbf" if data.startswith(b"\xef\xbb\xbf") else b""
    try:
        content = data[len(bom):].decode("utf-8")
    except UnicodeDecodeError:
        return None, "not UTF-8"
    existing_head = "\n".join(content.splitlines()[:80])
    if PREEXISTING.search(existing_head):
        if not args.annotate_existing:
            return None, "existing copyright/SPDX header"
        if AI_MARKER.search(existing_head):
            return None, "existing AI attribution"
        # We only annotate files whose existing first-party copyright notice
        # names the supplied holder. Merely finding the author's name in code
        # (or a third-party license elsewhere in the file) is not sufficient.
        copyright_lines = [line for line in existing_head.splitlines()
                           if COPYRIGHT_LINE.match(line)]
        if not any(args.holder.casefold() in line.casefold()
                   for line in copyright_lines):
            return None, "pre-existing notice is not demonstrably first-party"
        ai_only = True
    else:
        ai_only = False
    # Original EOL convention is retained, including CRLF source files.
    newline = "\r\n" if "\r\n" in content else "\n"
    at, problem = insertion_point(content, path)
    if problem:
        return None, problem
    # A header must be placed after a line boundary, not after inline code.
    if at and content[at - 1] not in ("\n", "\r"):
        return None, "unsafe insertion boundary"
    notice = header(args, style_for(path), newline, ai_only=ai_only) + newline + newline
    return bom + (content[:at] + notice + content[at:]).encode("utf-8"), (
        "annotate" if ai_only else "add")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    paths = walk_files(args.root) if args.all_files else git_files(args.root)
    if paths is None:
        print("[INFO] Not a Git worktree; scanning filesystem with built-in exclusions.")
        paths = walk_files(args.root)
    counts = {"added": 0, "missing": 0, "skipped": 0, "errors": 0}
    for path in paths:
        if not eligible(path, args.root, args.exclude):
            continue
        relative = path.relative_to(args.root).as_posix()
        try:
            effective = scoped_args(path, args)
            if effective is None:
                counts["skipped"] += 1
                print(f"[SKIP] {relative}: policy marks path as external")
                continue
            update, reason = prepare(path, effective)
            if update is None:
                counts["skipped"] += 1
                print(f"[SKIP] {relative}: {reason}")
                continue
            if args.apply:
                path.write_bytes(update)
                counts["added"] += 1
                print(f"[{'AI' if reason == 'annotate' else 'ADD'}]  {relative}")
            else:
                counts["missing"] += 1
                print(f"[PLAN] {relative}")
        except (OSError, ValueError) as exc:
            counts["errors"] += 1
            print(f"[ERROR] {relative}: {exc}", file=sys.stderr)
    label = "APPLY" if args.apply else ("CHECK" if args.check else "PREVIEW")
    print(f"\n{label}: added={counts['added']} pending={counts['missing']} "
          f"skipped={counts['skipped']} errors={counts['errors']}")
    return 1 if counts["errors"] or (args.check and counts["missing"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())