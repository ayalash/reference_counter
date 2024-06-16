default: test

test: env
	.venv/bin/pytest tests

env: .venv/.up-to-date

.venv/.up-to-date: pyproject.toml Makefile
	python -m venv .venv
	.venv/bin/pip install -e '.[testing]'
	touch $@

