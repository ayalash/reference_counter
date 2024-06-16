default: test

test: env
	.venv/bin/pytest tests

env: .venv/.up-to-date

.venv/.up-to-date: setup.py Makefile test_requirements.txt doc_requirements.txt
	python -m venv .venv
	.venv/bin/pip install -e .
	.venv/bin/pip install -r test_requirements.txt
	.venv/bin/pip install -r doc_requirements.txt
	touch $@

