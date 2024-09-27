default: test

test:
	uv run --extra testing pytest tests

lint:
	uv run --extra testing ruff check .
	uv run --extra testing ruff format --check .

env:
	uv venv
