.PHONY: setup install migrate run run-api run-dash run-frontend test lint clean docker-build docker-run help

help:
	@echo "WhoWhyWhen - FastAPI Middleware Analytics"
	@echo ""
	@echo "Available commands:"
	@echo "  setup         - Create virtual environment and install dependencies"
	@echo "  install       - Install dependencies only"
	@echo "  migrate       - Run database migrations"
	@echo "  run           - Run all services (API, Dashboard, Frontend)"
	@echo "  run-api       - Run API server"
	@echo "  run-dash      - Run Dashboard server"
	@echo "  run-frontend  - Run Frontend development server"
	@echo "  test          - Run tests"
	@echo "  lint          - Run linters"
	@echo "  clean         - Remove build artifacts and virtual environment"
	@echo "  docker-build  - Build Docker images"
	@echo "  docker-run    - Run with Docker Compose"

setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	cp -n .env.example .env || true
	@echo "Setup complete. Remember to configure your .env file."

install:
	pip install -r requirements.txt

migrate:
	alembic upgrade head

run:
	@echo "Starting API server on port 8001..."
	@nohup uvicorn app.main_api:app --host 0.0.0.0 --port 8001 > api.log 2>&1 &
	@echo "Starting Dashboard server on port 8000..."
	@nohup uvicorn app.main_dash:app --host 0.0.0.0 --port 8000 > dash.log 2>&1 &
	@echo "Starting Frontend server..."
	@cd who-why-when-landing-page && npm run dev

run-api:
	uvicorn app.main_api:app --host 0.0.0.0 --port 8001 --reload

run-dash:
	uvicorn app.main_dash:app --host 0.0.0.0 --port 8000 --reload

run-frontend:
	cd who-why-when-landing-page && npm run dev

test:
	pytest

lint:
	flake8 app
	black --check app
	isort --check-only app

clean:
	rm -rf __pycache__
	rm -rf *.log
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .tox/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker-compose build

docker-run:
	docker-compose up -d