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

PYTHON ?= python3

.PHONY: test viewer-test case-study paper verify publication all
test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

viewer-test:
	node tests/test_viewer.cjs

case-study:
	PYTHONPATH=src $(PYTHON) experiments/case_study.py

paper:
	$(PYTHON) scripts/build_papers.py

verify:
	$(PYTHON) scripts/verify_repository.py

publication: verify
	$(PYTHON) scripts/prepare_publication.py

all: test viewer-test case-study paper verify
