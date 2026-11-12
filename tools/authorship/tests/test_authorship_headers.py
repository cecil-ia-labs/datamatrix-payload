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

"""Regression tests: python3 -m unittest discover -s tests -v."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / "authorship_headers.py"
spec = importlib.util.spec_from_file_location("authorship_headers", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class HeaderTests(unittest.TestCase):
    def make_args(self, root, *extra):
        return mod.parse_args([str(root), "--holder", "Cecil-IA Labs",
                               "--author", "João Paulo De Luca",
                               "--organization", "Cecil-IA Labs",
                               "--license", "MIT", "--year", "2023-2026",
                               *extra])

    def test_formats_and_idempotence(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cases = {
                "app.ts": (b"const x = 2;\n", b"/*\n"),
                "script.sh": (b"#!/bin/bash\necho yes\n", b"#!/bin/bash\n# SPDX"),
                "file.py": (b"#!/usr/bin/python3\n# coding: utf-8\nprint('ok')\n", b"# coding: utf-8\n# SPDX"),
                "README.md": (b"---\ntitle: Test\n---\n# Readme\n", b"---\n<!--\nSPDX"),
                "index.html": (b"<!DOCTYPE html>\n<html></html>\n", b"<!DOCTYPE html>\n<!--\n"),
                "main.css": (b'@charset "UTF-8";\nbody{}\n', b'@charset "UTF-8";\n/*\n'),
                "config.yaml": (b"key: value\r\n", b"# SPDX-FileCopyrightText:"),
                "index.php": (b"<?php\nprint('ok');\n", b"<?php\n/*\n"),
                "vector.svg": (b'<?xml version="1.0"?>\n<svg/>\n', b'<?xml version="1.0"?>\n<!--\n'),
            }
            args = self.make_args(root)
            for filename, (source, expected) in cases.items():
                with self.subTest(filename=filename):
                    p = root / filename
                    p.write_bytes(source)
                    result, reason = mod.prepare(p, args)
                    self.assertEqual(reason, "add")
                    self.assertIn(expected, result)
                    self.assertEqual(result.count(b"SPDX-License-Identifier"), 1)
                    self.assertIn(b"OpenAI ChatGPT and Codex", result)
                    if filename == "config.yaml":
                        self.assertNotIn(b"\n", result.replace(b"\r\n", b""))
                    p.write_bytes(result)
                    second, reason = mod.prepare(p, args)
                    self.assertIsNone(second)
                    self.assertEqual(reason, "existing copyright/SPDX header")

    def test_existing_first_party_annotate_without_changing_license(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            p = root / "src.ts"
            original = "/*\n * SPDX-FileCopyrightText: 2022 Cecil-IA Labs\n * SPDX-License-Identifier: Apache-2.0\n */\nexport const x = 1;\n"
            p.write_text(original)
            result, reason = mod.prepare(p, self.make_args(root, "--annotate-existing"))
            self.assertEqual(reason, "annotate")
            self.assertEqual(result.count(b"SPDX-License-Identifier"), 1)
            self.assertIn(b"Apache-2.0", result)
            self.assertNotIn(b"SPDX-License" + b"-Identifier: MIT", result)
            p.write_bytes(result)
            second, reason = mod.prepare(p, self.make_args(root, "--annotate-existing"))
            self.assertIsNone(second)
            self.assertEqual(reason, "existing AI attribution")

    def test_foreign_copyright_skipped(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            p = root / "vendor.ts"
            p.write_text("// SPDX-FileCopyrightText: 2021 Other Org\n// SPDX-License-Identifier: MIT\n")
            result, reason = mod.prepare(p, self.make_args(root, "--annotate-existing"))
            self.assertIsNone(result)
            self.assertEqual(reason, "pre-existing notice is not demonstrably first-party")

    def test_skips_json_build_constraints_and_yaml_directives(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.assertIsNone(mod.style_for(root / "data.json"))
            p = root / "main.go"
            p.write_text("//go:build linux\n\npackage main\n")
            result, reason = mod.prepare(p, self.make_args(root))
            self.assertIsNone(result)
            self.assertIn("constraints", reason)
            p = root / "example.yaml"
            p.write_text("%YAML 1.2\n---\na: 1\n")
            result, reason = mod.prepare(p, self.make_args(root))
            self.assertIsNone(result)
            self.assertIn("directive", reason)

    def test_cli_preview_apply_check_and_gitignore(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text("ignored.py\n")
            (root / "app.py").write_text("print('hello')\n")
            (root / "ignored.py").write_text("print('ignore')\n")
            base = [sys.executable, str(MODULE), str(root), "--holder", "Cecil-IA Labs",
                    "--author", "João Paulo De Luca", "--organization", "Cecil-IA Labs",
                    "--license", "MIT", "--year", "2026"]
            preview = subprocess.run(base, capture_output=True, text=True, check=True)
            self.assertIn("[PLAN] app.py", preview.stdout)
            self.assertNotIn("ignored.py", preview.stdout)
            self.assertEqual((root / "app.py").read_text(), "print('hello')\n")
            self.assertEqual(subprocess.run(base + ["--check"], capture_output=True).returncode, 1)
            self.assertEqual(subprocess.run(base + ["--apply"], capture_output=True).returncode, 0)
            self.assertEqual(subprocess.run(base + ["--check"], capture_output=True).returncode, 0)
            self.assertNotIn("SPDX", (root / "ignored.py").read_text())


if __name__ == "__main__":
    unittest.main()
