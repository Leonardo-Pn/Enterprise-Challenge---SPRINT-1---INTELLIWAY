.PHONY: install run test
install:
	python -m pip install -r requirements.txt
run:
	uvicorn src.main:app --reload

test:
	pytest -q
