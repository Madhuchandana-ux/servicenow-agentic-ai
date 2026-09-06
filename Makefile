.PHONY: deps test lint format build-image run-local train

deps:
	pip install --upgrade pip
	pip install -e .[dev]

test:
	PYTHONPATH=. pytest --cov=src --cov-report=term-missing

lint:
	ruff check src
	black --check .
	mypy src

format:
	black .
	ruff check --fix src

build-image:
	docker build -t servicenow-agentic-ai:latest .

run-local:
	streamlit run app.py

train:
	python src/train_category_model.py
	python src/train_priority_model.py
	python src/build_vector_db.py
