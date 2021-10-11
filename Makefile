.PHONY: quality release update serve clean

quality:
	black --check .
	flake8

release:
	fullrelease
	pip install -e ".[dev]"

update:
	pip install --upgrade pip
	pip install --upgrade --upgrade-strategy eager -e ".[dev]"

clean:
	rm -rf dist
	rm -rf .pytest_cache
