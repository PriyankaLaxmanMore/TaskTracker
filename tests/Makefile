APP=main:app

run:
	python -m uvicorn main:app --reload

test:
	PYTHONPATH=. pytest --cov=. --cov-report=term-missing

lint:
	flake8 .

format:
	black .

install:
	pip install -r requirements.txt