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
	@rm -rf build
	@rm -rf dist
	@rm -rf htmlcov
	@find . -name *__pycache__ -exec rm -rf {} +
	@rm -rf tests/results

img:
	pytest --mpl-generate-path=tests/baseline

tests:
	pytest --mpl --mpl-results-path=tests/results

publish:clean
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*
