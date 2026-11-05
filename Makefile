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
