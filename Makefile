install:
	pip install -r requirements.txt

format:
	black **/*.py

test:
	pytest

start:
	python main.py