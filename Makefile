default: test

test: env
	.venv/bin/pytest tests

lint: env
	.venv/bin/ruff check .
	.venv/bin/ruff format --check .

env: .venv/.up-to-date

.venv/.up-to-date: pyproject.toml Makefile
	uv venv .venv
	uv pip install -e '.[testing]'
	touch $@

