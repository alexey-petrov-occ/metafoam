.PHONY: requirements-dev.txt
.PHONY: $(wildcard x-*)

x-build: x-check-artefacts x-check-code x-check-docs
x-check-artefacts: x-openfoam-6 x-foam-extend-3.0
x-check-code: x-check-cov x-check-style
x-check-style: x-check-pylint x-check-flake8 x-check-black

openfoam-6:
	git clone https://github.com/OpenFOAM/OpenFOAM-6.git openfoam-6

foam-extend-3.0:
	git clone https://git.code.sf.net/p/foam-extend/foam-extend-3.0 foam-extend-3.0

foam = $<
root := $(shell pwd)
artefacts := $(root)/artefacts

x-openfoam-6: openfoam-6
	artefacts/viscosity/foam2models $(foam)
	artefacts/viscosity/models2attributes $(foam)

x-foam-extend-3.0: foam-extend-3.0
	artefacts/viscosity/foam2models $(foam)
	artefacts/viscosity/models2attributes $(foam)

clean: x-clean-artefacts
	rm -fr foam-extend-* openfoam-*

x-clean-artefacts:
	find artefacts -name '*.txt' -exec rm -fr {} \;

x-update-refs:
	find ${artefacts} -name '*.txt' -exec ${artefacts}/txt2ref {} \;

x-check-test:
	pytest --no-cov --numprocesses=0 test

x-check-cov:
	pytest --cov=metafoam --cov-fail-under=100 --cov-report term-missing --cov-branch --numprocesses=auto -p no:warnings test

travis-before_install:
	sudo apt-get update
	sudo apt-get install -y coreutils findutils grep python3-sphinx

travis-install:
	pip install -r requirements-dev.txt
	python setup.py develop

x-check-pylint:
	pylint metafoam --rcfile=${root}/.pylintrc
	@diff ${root}/.pylintrc ${root}/.pylintrc.ref > ${root}/.pylintrc.diff || exit 0

x-check-flake8:
	flake8 metafoam
	flake8 test

x-check-black:
	black --check --config pyproject.toml metafoam

x-black-run:
	black --config pyproject.toml metafoam

requirements-dev.txt:
	pipenv run pipenv_to_requirements -d requirements-dev.txt -f

x-docker-env:
	docker build --tag metafoam:python --file env/python.dockerfile env

x-docker-run:
	docker run --rm -it -v $$(pwd):/code -w /code metafoam:python bash

x-pip-env:
	pipenv install --dev

x-pip-run:
	pipenv shell

x-check-docs:
	cd docs && make html

x-check-shell:
	shellcheck artefacts/*
