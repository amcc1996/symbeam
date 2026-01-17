# Read code version
VERSION=$(shell cat ./VERSION)

# Data for communication with Github
GIT_BRANCH=$(shell git rev-parse --abbrev-ref HEAD)
TOKEN=$(shell cat ~/.github-access-token)
API_JSON=$(shell printf '{"tag_name": "v%s","target_commitish": "master","name": "v%s","body": "Release of version %s","draft": false,"prerelease": false}' $(VERSION) $(VERSION) $(VERSION))
URL=https://api.github.com/repos/amcc1996/symbeam/releases

.PHONY: format coverage clean img tests deploy

lint:
	uv tool run isort --check .
	uv tool run black --check .
	uv tool run flake8 .
	uv tool run codespell .

format:
	uv tool run isort .
	uv tool run black .

coverage:
	uv run pytest --cov-report html --cov symbeam

clean:
	@rm -rf *.egg-info/
	@rm -rf build
	@rm -rf dist
	@rm -rf htmlcov
	@find . -name *__pycache__ -exec rm -rf {} +
	@rm -rf tests/results

baseline:
	uv run pytest --mpl-generate-path=tests/baseline
	uv run --script symbeam/utils/generate_output_baseline.py

tests:
	uv run 	pytest --mpl --mpl-results-path=tests/results

deploy:
	uv build
	uv publish


