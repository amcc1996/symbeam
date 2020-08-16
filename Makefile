format:
	black -l 92 symbeam

coverage:
	pytest --cov-report html --cov tests/
