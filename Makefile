install:
	pip install -r requirements.txt
test:
	pip install -r requirements.txt && pytest -v -W ignore tests
run:
	python3 server.py

.PHONY: install test
