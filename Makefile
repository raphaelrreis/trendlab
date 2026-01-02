.PHONY: setup test lint format clean run-pipeline build up down run-local

setup:
	poetry install
	poetry run pre-commit install

test:
	poetry run pytest tests/ -v --cov=trendlab

lint:
	poetry run ruff check .
	poetry run mypy .

format:
	poetry run ruff format .
	poetry run ruff check . --fix

clean:
	rm -rf dist build .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

run-pipeline:
	poetry run trendlab run --assets bitcoin ethereum solana --days 365

# Docker / Platform Engineering Targets
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

run-local:
	curl -X POST http://localhost:8080/run \
		-H "Content-Type: application/json" \
		-d '{"assets": ["btc", "eth"], "days": 365, "horizon": 1}'
