all: test-foam-extend-3.0 test-openfoam-6 test

.PHONY: test-openfoam-6 test-foam-extend-3.0 clean-artefacts test txt2ref

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

test:
	pytest test

install:
	sudo apt-get install -y coreutils findutils grep

requirements:
	pipenv run pipenv_to_requirements -d requirements-dev.txt
