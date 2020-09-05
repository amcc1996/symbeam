.PHONY: format coverage clean

lint:
	isort --check --color .
	black --check .
	flake8 .

format:
	isort .
	black -l 92 .
	blacken-docs README.md examples/README.md

coverage:
	pytest --cov-report html --cov symbeam

clean:
	@rm -rf *.egg-info/
	@if [ -d "htmlcov" ]; then rm -rf htmlcov; echo Removed hmltcov; fi
	@find . -name *__pycache__ -exec rm -rf {} +
	@echo Removed *.egg-info and __pycache__
