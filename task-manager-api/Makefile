.PHONY: run dev install format lint test

run:
	uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8002 --reload

install:
	pip install -r backend/requirements.txt -r backend/requirements-dev.txt

format:
	ruff format backend

lint:
	ruff check backend

test:
	pytest -q backend/app/tests


