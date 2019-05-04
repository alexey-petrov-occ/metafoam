.PHONY: test-openfoam-6 test-foam-extend-3.0 clean-artefacts
.PHONY: check-test check-pylint check-flake8 check-code
.PHONY: txt2ref requirements-dev.txt

check: test-foam-extend-3.0 test-openfoam-6 check-code
check-code: check-test check-pylint check-flake8

openfoam-6:
	git clone https://github.com/OpenFOAM/OpenFOAM-6.git openfoam-6

foam-extend-3.0:
	git clone https://git.code.sf.net/p/foam-extend/foam-extend-3.0 foam-extend-3.0

foam = $<
root := $(shell pwd)

test-openfoam-6: openfoam-6
	artefacts/viscosity/foam2models $(foam)
	artefacts/viscosity/models2attributes $(foam)

test-foam-extend-3.0: foam-extend-3.0
	artefacts/viscosity/foam2models $(foam)
	artefacts/viscosity/models2attributes $(foam)

clean: clean-artefacts
	rm -fr foam-extend-* openfoam-*

clean-artefacts:
	find artefacts -name '*.txt' -exec rm -fr {} \;

txt2ref:
	find artefacts -name '*.txt' -exec ${root}/txt2ref {} \;

check-test:
	pytest test

before_install:
	sudo apt-get update
	sudo apt-get install -y coreutils findutils grep

install:
	pip install -r requirements-dev.txt
	python setup.py develop

check-pylint:
	pylint metafoam --rcfile=${root}/.pylintrc
	@diff ${root}/.pylintrc ${root}/.pylintrc.ref > ${root}/.pylintrc.diff || exit 0

check-flake8:
	flake8 metafoam

requirements-dev.txt:
	pipenv run pipenv_to_requirements -d requirements-dev.txt -f
