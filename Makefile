.PHONY: format coverage clean img tests

lint:
	isort --check --color .
	black -l 92 --check .
	flake8 .

format:
	isort --color .
	black -l 92 .

coverage:
	pytest --cov-report html --cov symbeam

clean:
	@rm -rf *.egg-info/
	@if [ -d "htmlcov" ]; then rm -rf htmlcov; echo Removed hmltcov; fi
	@find . -name *__pycache__ -exec rm -rf {} +
	@echo Removed *.egg-info and __pycache__
	@if [ -d "tests/results" ]; then rm -rf tests/results; echo Removed tests/results; fi

img:
	@pytest --mpl-generate-path=tests/baseline

tests:
	@pytest --mpl --mpl-results-path=tests/results
