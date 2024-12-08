.PHONY: help clean test install all init dev cli go today day_% inputs reports
.DEFAULT_GOAL := today

.PRECIOUS: src/day_%.py inputs/day_%.txt

HOOKS=$(.git/hooks/pre-commit)
REQS=$(shell python -c 'import tomllib;[print(f"requirements.{k}.txt") for k in tomllib.load(open("pyproject.toml", "rb"))["project"]["optional-dependencies"].keys()]')

BINPATH=$(shell which python | xargs dirname | xargs realpath --relative-to=".")
SYSTEM_PYTHON_VERSION:=$(shell ls /usr/bin/python* | grep -Eo '[0-9]+\.[0-9]+' | sort -V | tail -n 1)
PYTHON_VERSION:=$(shell python --version | cut -d " " -f 2)
PIP_PATH:=$(BINPATH)/pip
WHEEL_PATH:=$(BINPATH)/wheel
PRE_COMMIT_PATH:=$(BINPATH)/pre-commit
UV_PATH:=$(BINPATH)/uv

ALLDAYS=$(wildcard src/day_*.py)
ALLINPUTS=$(subst src/,inputs/,$(subst .py,.txt,$(ALLDAYS)))
CURRENT_DAY=$(shell date +%d)
CURRENT_YEAR=2024
COOKIEFILE=cookies.txt

inputs: $(ALLINPUTS)
	@echo $^

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

requirements.%.txt: $(UV_PATH) pyproject.toml
	@echo "Builing $@"
	python -m uv pip compile --generate-hashes --extra $* $(filter-out $<,$^) > $@

requirements.txt: $(UV_PATH) pyproject.toml
	@echo "Builing $@"
	python -m uv pip compile --generate-hashes $(filter-out $<,$^) > $@

.git/hooks/pre-commit: $(PRE_COMMIT_PATH) .pre-commit-config.yaml .git
	pre-commit install

.envrc:
	@echo "Setting up .envrc then stopping"
	@echo "layout python python$(SYSTEM_PYTHON_VERSION)" > $@
	@touch -d '+1 minute' $@
	@false

$(PIP_PATH):
	@python -m ensurepip
	@python -m pip install --upgrade pip
	@touch $@

$(WHEEL_PATH): $(PIP_PATH)
	@python -m pip install wheel
	@touch $@

$(UV_PATH): $(PIP_PATH) $(WHEEL_PATH)
	python -m pip install uv
	@touch $@

$(PRE_COMMIT_PATH): $(PIP_PATH) $(WHEEL_PATH)
	@python -m pip install pre-commit
	@touch $@

init: .direnv .git/hooks/pre-commit $(UV_PATH) requirements.dev.txt ## Initalise a enviroment

clean: ## Remove all build files
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf .pytest_cache .testmondata
	rm -rf report

.direnv: .envrc $(UV_PATH) requirements.txt $(REQS)
	@echo "Installing $(filter %.txt,$^)"
	@python -m uv pip sync $(filter %.txt,$^)
	@touch $@ $^

install: .direnv ## Install requirements (default)

$(COOKIEFILE):
	@echo "Please visit https://adventofcode.com, login and copy the session cookie to $@"
	@echo "format: session=xxxxxxxxxxxxxxxxx"
	@false

inputs/day_%.txt: $(COOKIEFILE)
	curl -H 'User-Agent: Makefile - curl : bengosney@googlemail.com' --cookie "$(shell cat $^)" -s -L -o $@ https://adventofcode.com/$(CURRENT_YEAR)/day/$(shell echo "$@" | egrep -o "[0-9]+" | sed 's/^0*//')/input

src/day_%.py:
	cp template.py.template $@

src/aoc.py: $(wildcard src/day_*.py)
	cog -cr $@

mypy: $(ALLDAYS)
	mypy --check-untyped-defs $^

pytest: src/*.py
	pytest $^

test: pytest mypy

pytest.ini: # this is a hack, otherwise ptw will try to read toml and fail
	touch $@

day_%: .direnv src/day_%.py inputs/day_%.txt pytest.ini ## Setup day and start runing test monitor
	ptw --runner "pytest --testmon" --onfail "notify-send \"Failed\"" --onpass "notify-send \"Passed\"" src/$@.py

today: day_$(CURRENT_DAY) ## Setup current day and start runing test monitor

cli: src/aoc.py .direnv
	@python -m pip install -e .

report/day_%.html: src/day_%.py inputs/day_%.txt
	specialist --output report --targets $< -m pytest $<

reports: $(patsubst src/day_%.py,report/day_%.html,$(ALLDAYS))
