all: test-foam-extend-3.0 test-openfoam-6 test

.PHONY: test-openfoam-6 test-foam-extend-3.0 clean-artefacts test update-refs

openfoam-6:
	git clone https://github.com/OpenFOAM/OpenFOAM-6.git openfoam-6

foam-extend-3.0:
	git clone https://git.code.sf.net/p/foam-extend/foam-extend-3.0 foam-extend-3.0

foam = $<
artefacts := $(shell pwd)/artefacts
include artefacts/viscosity.mk

test-openfoam-6: openfoam-6
	artefacts/viscosity/foam2models.sh $(foam)
	artefacts/viscosity/models2attributes.sh $(foam)

test-foam-extend-3.0: foam-extend-3.0
	- $(viscosity_generate)
	$(viscosity_check)
	artefacts/viscosity/models2attributes.sh $(foam)

clean: clean-artefacts
	rm -fr foam-extend-* openfoam-*

clean-artefacts:
	find artefacts -name '*.txt' -exec rm -fr {} \;

update-refs:
	find artefacts -name '*.txt' -exec ${artefacts}/txt2ref.sh {} \;

test:
	pytest test

install:
	sudo apt-get install -y coreutils findutils grep

requirements:
	pipenv run pipenv_to_requirements -d requirements-dev.txt
