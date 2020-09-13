# Read code version
VERSION=$(shell cat ./VERSION)

# Data for communication with Github
GIT_BRANCH=$(shell git rev-parse --abbrev-ref HEAD)
TOKEN=$(shell cat ~/.github-access-token)
API_JSON=$(shell printf '{"tag_name": "v%s","target_commitish": "master","name": "v%s","body": "Release of version %s","draft": false,"prerelease": false}' $(VERSION) $(VERSION) $(VERSION))
URL=https://api.github.com/repos/amcc1996/symbeam/releases

.PHONY: format coverage clean img tests deploy

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

deploy: clean
	if [ "$(GIT_BRANCH)" != "master" ]; then echo "Not in master branch"; exit 1; fi
	curl -H "Authorization: token $(TOKEN)" --data '$(API_JSON)' $(URL)
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*


